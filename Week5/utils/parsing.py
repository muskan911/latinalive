import stanza

_nlp = None
def nlp():
    global _nlp
    if _nlp is None:
        _nlp = stanza.Pipeline(lang="la", processors="tokenize,pos,lemma")
    return _nlp

def analyze(text: str):
    if not text.strip():
        return []
    doc = nlp()(text)
    rows = []
    for sent in doc.sentences:
        for w in sent.words:
            rows.append({"token": w.text, "lemma": w.lemma, "pos": w.pos, "feats": w.feats})
    return rows
