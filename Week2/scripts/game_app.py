import json, random
import streamlit as st
import stanza

# ---------- Setup ----------
st.set_page_config(page_title="LatinAlive — Week 2 Games", layout="wide")
@st.cache_resource
def load_pipeline():
    return stanza.Pipeline(lang='la', processors='tokenize,pos,lemma')
nlp = load_pipeline()

@st.cache_data
def load_exercises(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["exercises"]

exs = load_exercises("Week2/data/exercises.json")
ex_by_id = {e["id"]: e for e in exs}

# ---------- UI ----------
st.title("LatinAlive — Week 2: Syntax & Sentence Building")
ex_ids = [e["id"] for e in exs]
choice = st.sidebar.selectbox("Choose exercise", ex_ids, format_func=lambda x: f'{x} — {ex_by_id[x]["scene"]}')

ex = ex_by_id[choice]
st.subheader(ex["scene"])
st.caption(f'English: {ex["translation"]}')
st.markdown("**Focus:** " + ", ".join(ex["focus"]))

tab1, tab2 = st.tabs(["🧩 Unscramble", "✅ Grammar MCQs"])

# ---------- Helpers ----------
def normalize(s):
    return " ".join(s.replace(" ."," .").replace(" ,"," ,").split()).strip()

def parse_table(sentence: str):
    doc = nlp(sentence)
    rows = []
    for sent in doc.sentences:
        for w in sent.words:
            rows.append({"Token": w.text, "Lemma": w.lemma, "POS": w.pos, "Features": w.feats})
    return rows

# ---------- Tab 1: Unscramble ----------
with tab1:
    st.markdown("Arrange the tokens to form a correct Latin sentence.")
    if f"answer_{ex['id']}" not in st.session_state:
        st.session_state[f"answer_{ex['id']}"] = []

    colA, colB = st.columns(2)
    with colA:
        st.markdown("**Click tokens to build your sentence**")
        shuffled = st.session_state.get(f"shuffled_{ex['id']}")
        if shuffled is None:
            shuffled = ex["tokens"][:]
            random.shuffle(shuffled)
            st.session_state[f"shuffled_{ex['id']}"] = shuffled

        token_cols = st.columns(min(6, len(shuffled)))
        for i, tk in enumerate(shuffled):
            if token_cols[i % len(token_cols)].button(tk, key=f"{ex['id']}_tk_{i}"):
                st.session_state[f"answer_{ex['id']}"].append(tk)

        st.write("")
        c1, c2, c3 = st.columns(3)
        if c1.button("Undo"):
            if st.session_state[f"answer_{ex['id']}"]:
                st.session_state[f"answer_{ex['id']}"].pop()
        if c2.button("Reset"):
            st.session_state[f"answer_{ex['id']}"] = []
            st.session_state[f"shuffled_{ex['id']}"] = None  # reshuffle next run
        if c3.button("Check"):
            pass  # triggers rerun; we check below

    with colB:
        built = " ".join(st.session_state[f"answer_{ex['id']}"]).replace(" .", ".").replace(" ,", ",")
        st.markdown("**Your sentence:**")
        st.info(built if built else "—")

        target = ex["target_sentence"]
        correct = normalize(built) == normalize(target)

        if built:
            if correct:
                st.success("✅ Correct!")
            else:
                st.warning("Not quite. Tip: watch subject–object–verb and prepositional phrase order.")
            st.markdown("**Morphology (your sentence):**")
            st.table(parse_table(built))

        with st.expander("Show target sentence"):
            st.code(target, language="text")
            st.table(parse_table(target))

# ---------- Tab 2: MCQs ----------
with tab2:
    score = 0
    for idx, q in enumerate(ex["mcq"], start=1):
        st.markdown(f"**Q{idx}. {q['q']}**")
        picked = st.radio("Choose one:", q["options"], key=f"{ex['id']}_q_{idx}", index=None)
        if picked:
            if picked == q["answer"]:
                st.success("Correct.")
                score += 1
            else:
                st.error(f"Incorrect. {q['explain']}")
        st.divider()
    if ex["mcq"]:
        st.info(f"Score: {score} / {len(ex['mcq'])}")
