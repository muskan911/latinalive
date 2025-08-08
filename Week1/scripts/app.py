import streamlit as st
import stanza


nlp = stanza.Pipeline(lang='la', processors='tokenize,pos,lemma')

st.set_page_config(page_title="LatinAlive Parser Demo", layout="wide")
st.title("LatinAlive — Latin Sentence Parser")
st.write("Enter a Latin sentence to see POS tags, lemmas, and morphological features.")

text = st.text_area("Latin Sentence", "Puella panem emit in foro.")

if st.button("Parse"):
    if text.strip():
        doc = nlp(text)
        rows = []
        for sent in doc.sentences:
            for w in sent.words:
                rows.append({
                    "Token": w.text,
                    "Lemma": w.lemma,
                    "POS": w.pos,
                    "Features": w.feats
                })
        st.table(rows)
    else:
        st.warning("Please enter a Latin sentence.")
