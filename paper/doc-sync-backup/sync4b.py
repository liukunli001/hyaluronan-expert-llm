import json, subprocess

DOC = "1v399829q_K0kmgRU5NurgFow6HczZEkQcSQNrKdchz8"
BACKUP = "/home/hatch/workspace/hyaluronan-expert-llm/paper/doc-sync-backup"
URI = "https://raw.githubusercontent.com/liukunli001/hyaluronan-expert-llm/32d5f9a049541278da43a65358055cf7bf6a5c4d/paper/figs/fig2-results.png"

def gws(args, inp=None):
    r = subprocess.run(["hatch_gws_cli"] + args, input=inp, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{args[:3]} -> {r.stderr[:400]}")
    return r.stdout

doc = json.loads(gws(["docs", "documents", "get", "--params", json.dumps({"documentId": DOC})]))
content = doc["body"]["content"]

# locate caption paragraph and the image element in the paragraph just before it
cap_idx = None
for i, e in enumerate(content):
    p = e.get("paragraph")
    if p:
        txt = "".join(el.get("textRun", {}).get("content", "") for el in p.get("elements", []))
        if txt.startswith("Figure 2. HA-Expert-Bench results"):
            cap_idx = i
            break
assert cap_idx is not None, "caption not found"

img = None
for j in range(cap_idx - 1, max(cap_idx - 4, -1), -1):
    p = content[j].get("paragraph")
    if not p:
        continue
    for el in p.get("elements", []):
        if "inlineObjectElement" in el or "inlineImage" in el:
            img = (el["startIndex"], el["endIndex"])
    if img:
        break
assert img, "no figure image found before caption"
print("old image range:", img)

REV = doc["revisionId"]
reqs = [
    {"deleteContentRange": {"range": {"startIndex": img[0], "endIndex": img[1]}}},
    {"insertInlineImage": {
        "uri": URI,
        "location": {"index": img[0]},
        "objectSize": {"height": {"magnitude": 336, "unit": "PT"},
                       "width": {"magnitude": 468, "unit": "PT"}}}},
]
body = json.dumps({"requests": reqs, "writeControl": {"requiredRevisionId": REV}})
out = gws(["docs", "documents", "batchUpdate", "--params", json.dumps({"documentId": DOC}),
           "--json", body])
json.dump(json.loads(out), open(f"{BACKUP}/round4-fig2-resp.json", "w"), ensure_ascii=False, indent=1)
print("fig2 replaced OK")
