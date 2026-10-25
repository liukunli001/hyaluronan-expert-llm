#!/usr/bin/env python3
import json, subprocess, sys
sys.path.insert(0, '/home/hatch/workspace/hyaluronan-expert-llm/paper/doc-sync-backup')
from segs import S

DOC = '1v399829q_K0kmgRU5NurgFow6HczZEkQcSQNrKdchz8'
BASE = '/home/hatch/workspace/hyaluronan-expert-llm/paper/doc-sync-backup'

def gws(*args):
    r = subprocess.run(['hatch_gws_cli', 'docs', 'documents', *args],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"gws failed: {r.stderr[:500]} / {r.stdout[:300]}")
    return r.stdout

def fetch():
    out = gws('get', '--params', json.dumps({'documentId': DOC}))
    return json.loads(out)

def para_text(el):
    if 'paragraph' not in el:
        return None
    return ''.join(pe.get('textRun', {}).get('content', '')
                   for pe in el['paragraph'].get('elements', []) if 'textRun' in pe)

def para_runs(el):
    runs = []
    for pe in el['paragraph'].get('elements', []):
        if 'textRun' in pe:
            tr = pe['textRun']; st = tr.get('textStyle', {})
            f = ('B' if st.get('bold') else '') + ('I' if st.get('italic') else '')
            runs.append((f, tr['content']))
    return runs

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

def main():
    orig_doc = json.load(open(f'{BASE}/doc-pretrim-full.json'))
    orig = {}
    for i, el in enumerate(orig_doc['body']['content']):
        if 'paragraph' in el:
            orig[i] = (el['startIndex'], el['endIndex'])
    keys = sorted(S.keys(), reverse=True)
    print(f"{len(keys)} paragraphs to update")
    batches = [keys[k:k + 8] for k in range(0, len(keys), 8)]
    for bi, batch in enumerate(batches):
        reqs = build_requests(batch, orig)
        body = json.dumps({'requests': reqs})
        out = gws('batchUpdate', '--params', json.dumps({'documentId': DOC}), '--json', body)
        print(f"batch {bi+1}/{len(batches)} paras {batch}: applied, {len(reqs)} requests")
        # verify this batch
        doc = fetch()
        content = doc['body']['content']
        assert len(content) == len(orig_doc['body']['content']), "structural element count changed!"
        bad = []
        for i in batch:
            expected = ''.join(t for _, t in S[i]) + '\n'
            got = para_text(content[i])
            if got != expected:
                bad.append(i)
                print(f"  MISMATCH P{i:03d}:\n    exp {expected[:120]!r}\n    got {(got or '')[:120]!r}")
        if bad:
            print(f"batch {bi+1} verification FAILED for {bad}; stopping")
            sys.exit(1)
        print(f"batch {bi+1} verified OK")

if __name__ == '__main__':
    main()
