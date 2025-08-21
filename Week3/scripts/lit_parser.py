import json, stanza

nlp = stanza.Pipeline(lang="la", processors="tokenize,pos,lemma")

with open("Week3/data/texts.json", encoding="utf-8") as f:
    texts = json.load(f)["stories"]

for s in texts:
    print(f"\n== {s['title']} ==")
    doc = nlp(s["latin"])
    for sent in doc.sentences:
        for w in sent.words:
            print(w.text, w.lemma, w.pos, w.feats)
