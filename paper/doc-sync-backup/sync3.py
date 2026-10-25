#!/usr/bin/env python3
# Round-3 Doc sync: email swap, USD-50 removal (3 spots), Future Work
# expansion, and insertion of the Sec. 3 sample-inputs block.
import json, subprocess, sys
sys.path.insert(0, '/home/hatch/workspace/hyaluronan-expert-llm/paper/doc-sync-backup')
import segs2, segs2b

DOC = '1v399829q_K0kmgRU5NurgFow6HczZEkQcSQNrKdchz8'
BASE = '/home/hatch/workspace/hyaluronan-expert-llm/paper/doc-sync-backup'

def gws(*args):
    r = subprocess.run(['hatch_gws_cli', 'docs', 'documents', *args],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gws failed: {r.stderr[:500]} / {r.stdout[:300]}")
    return r.stdout

def fetch():
    return json.loads(gws('get', '--params', json.dumps({'documentId': DOC})))

def para_text(el):
    if 'paragraph' not in el:
        return None
    return ''.join(pe.get('textRun', {}).get('content', '')
                   for pe in el['paragraph'].get('elements', []) if 'textRun' in pe)

def find(content, pred):
    hits = [i for i, el in enumerate(content)
            if 'paragraph' in el and pred(para_text(el) or '')]
    assert len(hits) == 1, f"expected 1 hit, got {hits}"
    return hits[0]

def replace_para(content, idx, segs):
    el = content[idx]
    s, e = el['startIndex'], el['endIndex']
    full = ''.join(t for _, t in segs)
    reqs = [{'deleteContentRange': {'range': {'startIndex': s, 'endIndex': e - 1}}},
            {'insertText': {'location': {'index': s}, 'text': full}},
            {'updateTextStyle': {'range': {'startIndex': s, 'endIndex': s + len(full)},
             'textStyle': {'bold': False, 'italic': False}, 'fields': 'bold,italic'}}]
    off = s
    for style, text in segs:
        if style:
            field = 'bold' if style == 'B' else 'italic'
            reqs.append({'updateTextStyle': {'range': {'startIndex': off, 'endIndex': off + len(text)},
                         'textStyle': {field: True}, 'fields': field}})
        off += len(text)
    gws('batchUpdate', '--params', json.dumps({'documentId': DOC}), '--json', json.dumps({'requests': reqs}))
    doc = fetch()
    got = para_text(doc['body']['content'][idx])
    assert got == full + '\n', f"replace verify failed at {idx}: {got[:100]!r}"
    print(f"replaced element {idx} OK ({len(full)} chars)")

def patched(segs, old, new):
    out = []
    for st, tx in segs:
        out.append((st, tx.replace(old, new)))
    return out

def main():
    doc = fetch()
    content = doc['body']['content']
    n0 = len(content)

    abstract = patched(segs2.S[4], 'can go, on under USD 50 of cloud compute, toward a ', 'can go toward a ')
    intro = patched(segs2.S[8], 'rented GPU, total compute under USD 50;', 'rented GPU;')
    replic = patched(segs2b.S[93], 'ablation, under USD 50): a template', 'ablation): a template')
    future = [
        ('', 'One fix per mechanism (Section 7): '),
        ('I', 'retrieval-formatted SFT data'),
        ('', ' for the format mismatch — examples in the exact inference format (question + retrieved excerpts + cited answer), predicted to move the combined cell above base+RAG; '),
        ('I', 'repetition filtering'),
        ('', ' of teacher outputs for the inheritance, screening pairs by the failure\'s operational definition. Evaluation-side: re-grade with an external judge and settle the 28 uncertain keys. Beyond hyaluronan, three directions follow. '),
        ('I', 'Other domains:'),
        ('', ' the pipeline is domain-agnostic apart from the corpus query (Section 8), so the same recipe applies to other literature-bound fields — heparin and other glycosaminoglycans, or bioconjugation chemistry. '),
        ('I', 'Ideation:'),
        ('', ' the released model already proposes novel research ideas and expands them into structured plans with hypotheses and experimental methods; adding corpus-scale novelty checking against the literature would turn that capability into a research tool. '),
        ('I', 'Review:'),
        ('', ' a model with verified command of a field\'s literature could serve as a first-pass reviewer of new submissions, checking claims against that literature — a use that, like ideation, needs evidence-checked evaluation before it can be trusted.'),
    ]
    author = [('', 'Kunli Liu — Independent Researcher, San Francisco Bay Area, USA — liukunli@msu.edu')]

    targets = [
        (find(content, lambda t: 'liukunli001@gmail.com' in t), author),
        (find(content, lambda t: t.startswith('General-purpose LLMs handle specialized fields')), abstract),
        (find(content, lambda t: t.startswith('We address them with the standard toolkit')), intro),
        (find(content, lambda t: t.startswith('Replicability.')), replic),
        (find(content, lambda t: t.startswith('One fix per mechanism')), future),
    ]
    for idx, segs in sorted(targets, reverse=True):
        replace_para(content, idx, segs)

    # --- insertion: sample-inputs block after the "DAPT sets." paragraph ---
    doc = fetch()
    content = doc['body']['content']
    anchor = find(content, lambda t: t.startswith('DAPT sets.'))
    el = content[anchor]
    insert_at = el['endIndex'] - 1
    L1 = 'What the model reads. Two samples from the released artifacts show the actual inputs. A corpus record (PMC10000474, Foods, 2023) begins:'
    L2 = 'Hyaluronic acid (HA) is now widely known for its ability to bind water and impart texture. The combined effects of HA and kappa-carrageenan (KC) have not yet been investigated, though. In this study, we looked at the synergistic effects of HA and KC (concentrations of 0.1 and 0.25%, and ratios of 85:15, 70:30, and 50:50 for each concentration) on the rheological properties, heat stability, protein phase separation, water-holding capacity, emulsification …'
    L3 = 'Retrieval chunks are ≈900-character windows cut across sentence boundaries; a chunk from the same paper begins mid-word:'
    L4 = 'ser protein phase separation and a higher water-holding capacity than when HA and KC were utilized separately. Similarly, for the sample with a 0.1% concentration, the combination of HA + KC blends demonstrated a synergistic impact with greater emulsifying activity and stability. The samples with a concentration of 0.25% did not exhibit this synergistic effect …'
    L5 = 'DAPT consumes record text like the first sample; SFT pairs are generated from such passages (Section 4.2); at inference, chunks like the second are prepended to the question (Section 4.4). Full readable samples are in examples/sample-data.md in the repository.'
    text = '\n' + '\n'.join([L1, L2, L3, L4, L5])
    reqs = [{'insertText': {'location': {'index': insert_at}, 'text': text}}]
    base = insert_at + 1  # start of L1
    reqs.append({'updateTextStyle': {'range': {'startIndex': base, 'endIndex': base + len('What the model reads.')},
                 'textStyle': {'bold': True}, 'fields': 'bold'}})
    foods_off = base + L1.index('Foods')
    reqs.append({'updateTextStyle': {'range': {'startIndex': foods_off, 'endIndex': foods_off + 5},
                 'textStyle': {'italic': True}, 'fields': 'italic'}})
    gws('batchUpdate', '--params', json.dumps({'documentId': DOC}), '--json', json.dumps({'requests': reqs}))

    # --- final verification ---
    doc = fetch()
    content = doc['body']['content']
    print(f"elements {n0} -> {len(content)} (expect {n0 + 5})")
    assert len(content) == n0 + 5
    texts = [para_text(el) or '' for el in content]
    joined = '\n'.join(texts)
    assert 'liukunli@msu.edu' in joined and 'gmail' not in joined
    assert 'USD' not in joined
    assert 'heparin and other glycosaminoglycans' in joined
    assert 'What the model reads.' in joined and 'begins mid-word' in joined
    ai = next(i for i, t in enumerate(texts) if t.startswith('DAPT sets.'))
    assert texts[ai + 1].startswith('What the model reads.'), texts[ai + 1][:80]
    assert texts[ai + 2].startswith('Hyaluronic acid (HA) is now widely known')
    assert texts[ai + 4].startswith('ser protein phase separation')
    json.dump(doc, open(f'{BASE}/doc-r3-post-full.json', 'w'))
    open(f'{BASE}/doc-r3-post-text.txt', 'w').write(joined)
    print('FINAL VERIFY OK')

if __name__ == '__main__':
    main()
