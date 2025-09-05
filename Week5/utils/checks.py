def has_pos(rows, tag):
    return any(r["pos"] == tag for r in rows)

def feedback_for_sentence(rows):
    tips = []
    if not has_pos(rows, "VERB"):
        tips.append("Add a finite verb (e.g., est, amat, videt).")
    if not has_pos(rows, "NOUN") and not has_pos(rows, "PROPN") and not has_pos(rows, "PRON"):
        tips.append("Add a clear subject (nominative).")
    # light case hint:
    # if no obvious object-like word:
    if not any("Case=Acc" in (r["feats"] or "") for r in rows):
        tips.append("Consider a direct object (accusative) if your verb is transitive.")
    return tips
