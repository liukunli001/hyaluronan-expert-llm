#!/usr/bin/env python3
import json, subprocess, sys
sys.path.insert(0, '/home/hatch/workspace/hyaluronan-expert-llm/paper/doc-sync-backup')
import segs2, segs2b
S = dict(segs2.S); S.update(segs2b.S)

DOC = '1v399829q_K0kmgRU5NurgFow6HczZEkQcSQNrKdchz8'
BASE = '/home/hatch/workspace/hyaluronan-expert-llm/paper/doc-sync-backup'
DELETE = [10, 11, 12, 13, 14, 17, 18, 19, 20, 25, 32, 44, 53, 54, 55, 81, 82, 92]

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

def build_requests(indices, orig):
    reqs = []
    for i in sorted(indices, reverse=True):
        s, e = orig[i]
        segs = S[i]
        full = ''.join(t for _, t in segs)
        reqs.append({'deleteContentRange': {'range': {'startIndex': s, 'endIndex': e - 1}}})
        reqs.append({'insertText': {'location': {'index': s}, 'text': full}})
        reqs.append({'updateTextStyle': {
            'range': {'startIndex': s, 'endIndex': s + len(full)},
            'textStyle': {'bold': False, 'italic': False}, 'fields': 'bold,italic'}})
        off = s
        for style, text in segs:
            if style:
                field = 'bold' if style == 'B' else 'italic'
                reqs.append({'updateTextStyle': {
                    'range': {'startIndex': off, 'endIndex': off + len(text)},
                    'textStyle': {field: True}, 'fields': field}})
            off += len(text)
    return reqs

def phase_replace():
    orig_doc = json.load(open(f'{BASE}/doc-r2-pre-full.json'))
    orig = {}
    for i, el in enumerate(orig_doc['body']['content']):
        if 'paragraph' in el:
            orig[i] = (el['startIndex'], el['endIndex'])
    keys = sorted(S.keys(), reverse=True)
    print(f"{len(keys)} paragraphs to update")
    batches = [keys[k:k + 8] for k in range(0, len(keys), 8)]
    for bi, batch in enumerate(batches):
        reqs = build_requests(batch, orig)
        out = gws('batchUpdate', '--params', json.dumps({'documentId': DOC}), '--json', json.dumps({'requests': reqs}))
        doc = fetch()
        content = doc['body']['content']
        assert len(content) == len(orig_doc['body']['content']), "structural element count changed!"
        bad = []
        for i in batch:
            expected = ''.join(t for _, t in S[i]) + '\n'
            got = para_text(content[i])
            if got != expected:
                bad.append(i)
                print(f"  MISMATCH P{i:03d}:\n    exp {expected[:140]!r}\n    got {(got or '')[:140]!r}")
        if bad:
            print(f"batch {bi+1} verification FAILED for {bad}; stopping")
            sys.exit(1)
        print(f"batch {bi+1}/{len(batches)} paras {batch}: verified OK")

def phase_delete():
    doc = fetch()
    content = doc['body']['content']
    n0 = len(content)
    reqs = []
    for i in sorted(DELETE, reverse=True):
        el = content[i]
        assert 'paragraph' in el, f"element {i} is not a paragraph"
        reqs.append({'deleteContentRange': {'range': {'startIndex': el['startIndex'], 'endIndex': el['endIndex']}}})
    gws('batchUpdate', '--params', json.dumps({'documentId': DOC}), '--json', json.dumps({'requests': reqs}))
    doc2 = fetch()
    n1 = len(doc2['body']['content'])
    print(f"deleted {len(DELETE)} paragraphs: elements {n0} -> {n1}")
    assert n1 == n0 - len(DELETE), "element count after deletion mismatch"
    json.dump(doc2, open(f'{BASE}/doc-r2-post-full.json', 'w'))

def phase_verify():
    pre = json.load(open(f'{BASE}/doc-r2-pre-full.json'))
    post = fetch()
    expected = []
    for i, el in enumerate(pre['body']['content']):
        if i in DELETE:
            continue
        if 'paragraph' in el:
            if i in S:
                expected.append(''.join(t for _, t in S[i]) + '\n')
            else:
                expected.append(para_text(el))
        elif 'table' in el:
            expected.append('<TABLE>')
        else:
            expected.append('<OTHER>')
    got = []
    for el in post['body']['content']:
        if 'paragraph' in el:
            got.append(para_text(el))
        elif 'table' in el:
            got.append('<TABLE>')
        else:
            got.append('<OTHER>')
    assert len(expected) == len(got), f"length mismatch exp {len(expected)} got {len(got)}"
    bad = 0
    for j, (e, g) in enumerate(zip(expected, got)):
        if e != g:
            bad += 1
            print(f"FINAL MISMATCH slot {j}:\n  exp {e[:160]!r}\n  got {(g or '')[:160]!r}")
    if bad:
        print(f"FINAL VERIFY FAILED: {bad} mismatches")
        sys.exit(1)
    words = sum(len(e.split()) for e in expected if e not in ('<TABLE>', '<OTHER>'))
    print(f"FINAL VERIFY OK: {len(got)} elements, ~{words} words of paragraph text")
    texts = [e for e in got if e]
    open(f'{BASE}/doc-r2-post-text.txt', 'w').write('\n'.join(texts))

if __name__ == '__main__':
    phase = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if phase in ('all', 'replace'):
        phase_replace()
    if phase in ('all', 'delete'):
        phase_delete()
    if phase in ('all', 'verify'):
        phase_verify()
