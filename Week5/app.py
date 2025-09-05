import os, json, io
import streamlit as st
from utils.parsing import analyze
from utils.checks import feedback_for_sentence
from utils.pdf_exports import export_portfolio_pdf

st.set_page_config(page_title="LatinAlive — All-in-One", layout="wide")

# storage
BASE = "Week5/storage/portfolios"
os.makedirs(BASE, exist_ok=True)

@st.cache_data
def load_exercises():
    p = "Week5/data/exercises.json"
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f).get("exercises", [])
    return []

def save_portfolio(student_id, data):
    out_json = os.path.join(BASE, f"{student_id}.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return out_json

def load_portfolio(student_id):
    p = os.path.join(BASE, f"{student_id}.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {"title":"LatinAlive Portfolio","student":student_id,"panels":[],"glossary":[],"reflections":{}}

st.sidebar.header("Portfolio")
student_id = st.sidebar.text_input("Student ID", value="student01")
portfolio = load_portfolio(student_id)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Comic Builder", "Instant Feedback", "Exercises", "Reflections", "Portfolio Export"
])

# --- Comic Builder ---
with tab1:
    st.subheader("Build your mini comic")
    if "panels" not in portfolio: portfolio["panels"]=[]
    cols = st.columns(3)
    add = cols[0].button("Add Panel")
    if add:
        portfolio["panels"].append({"image_path":"","latin":"","english":""})
    for i, p in enumerate(portfolio["panels"]):
        st.markdown(f"**Panel {i+1}**")
        up = st.file_uploader("Upload panel image", type=["png","jpg","jpeg"], key=f"img_{i}")
        if up:
            img_dir = "Week5/storage/portfolios"
            img_path = os.path.join(img_dir, f"{student_id}_panel{i+1}.png")
            with open(img_path, "wb") as f: f.write(up.getbuffer())
            p["image_path"] = img_path
        p["latin"] = st.text_area("Latin", p.get("latin",""), key=f"lat_{i}")
        p["english"] = st.text_area("English", p.get("english",""), key=f"eng_{i}")
        st.divider()

    st.markdown("**Glossary**")
    if "glossary" not in portfolio: portfolio["glossary"]=[]
    new_latin = st.text_input("Latin word")
    new_meaning = st.text_input("Meaning")
    cols = st.columns(2)
    if cols[0].button("Add to Glossary"):
        if new_latin and new_meaning:
            portfolio["glossary"].append({"latin":new_latin, "meaning":new_meaning})
    if cols[1].button("Clear Glossary"):
        portfolio["glossary"] = []

# --- Instant Feedback ---
with tab2:
    st.subheader("Automatic feedback on your captions")
    for i, p in enumerate(portfolio.get("panels", [])):
        st.markdown(f"**Panel {i+1}** — {p.get('latin','') or '—'}")
        rows = analyze(p.get("latin",""))
        if rows:
            st.table(rows)
            tips = feedback_for_sentence(rows)
            if tips:
                for t in tips: st.warning(t)
            else:
                st.success("Looks good!")
        else:
            st.info("Add Latin text above to see feedback.")
        st.divider()

# --- Exercises (reuse Week2 dataset) ---
with tab3:
    st.subheader("Practice")
    exs = load_exercises()
    if not exs:
        st.info("No exercises found. Add Week5/data/exercises.json.")
    else:
        ex = st.selectbox("Choose exercise", exs, format_func=lambda e: f"{e['id']} — {e['scene']}")
        # Unscramble UI
        st.markdown("**Unscramble**")
        tokens = ex["tokens"]
        cur = st.text_input("Type your order (space-separated)", "")
        target = " ".join(tokens).replace(" .",".")
        if st.button("Check Order"):
            if cur.strip().replace(" .",".") == target:
                st.success("Correct!")
            else:
                st.warning(f"Not quite. Target: {target}")
        # MCQs
        st.markdown("**MCQs**")
        score=0
        for idx,q in enumerate(ex["mcq"],1):
            pick = st.radio(q["q"], q["options"], key=f"q_{ex['id']}_{idx}", index=None)
            if pick:
                if pick==q["answer"]:
                    st.success("Correct"); score+=1
                else:
                    st.error(q["explain"])
        st.info(f"Score: {score}/{len(ex['mcq'])}")

# --- Reflections ---
with tab4:
    st.subheader("Metacognitive reflections")
    refl = portfolio.get("reflections", {})
    refl["strategy"]  = st.text_area("What strategies helped you write Latin?", refl.get("strategy",""))
    refl["challenge"] = st.text_area("What was hardest and how did you solve it?", refl.get("challenge",""))
    refl["next"]      = st.text_area("What will you try next time?", refl.get("next",""))
    portfolio["reflections"] = refl

# --- Portfolio Export ---
with tab5:
    st.subheader("Save & Export")
    if st.button("Save Portfolio"):
        path = save_portfolio(student_id, portfolio)
        st.success(f"Saved: {path}")
    if st.button("Export PDF"):
        pdf_path = os.path.join(BASE, f"{student_id}.pdf")
        export_portfolio_pdf(portfolio, pdf_path)
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name=f"{student_id}.pdf", mime="application/pdf")
