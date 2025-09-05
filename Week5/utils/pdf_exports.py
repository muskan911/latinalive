from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

def export_portfolio_pdf(portfolio: dict, out_path: str):
    styles = getSampleStyleSheet()
    story = []
    title = portfolio.get("title", "LatinAlive Portfolio")
    student = portfolio.get("student", "Student")
    story.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    story.append(Paragraph(f"Student: {student}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # Comic panels
    story.append(Paragraph("<b>Mini Comic</b>", styles["Heading2"]))
    for i, p in enumerate(portfolio.get("panels", []), 1):
        if p.get("image_path") and os.path.exists(p["image_path"]):
            story.append(Image(p["image_path"], width=360, height=240))
        story.append(Paragraph(f"<b>Latin:</b> {p.get('latin','')}", styles["Normal"]))
        story.append(Paragraph(f"<b>English:</b> {p.get('english','')}", styles["Normal"]))
        story.append(Spacer(1, 8))

    # Glossary
    gloss = portfolio.get("glossary", [])
    if gloss:
        story.append(Paragraph("<b>Glossary</b>", styles["Heading2"]))
        data = [["Latin", "Meaning"]]+[[g["latin"], g["meaning"]] for g in gloss]
        t = Table(data, colWidths=[150, 350])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0), colors.lightgrey),
            ("GRID",(0,0),(-1,-1), 0.5, colors.grey),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
        ]))
        story.append(t)
        story.append(Spacer(1, 8))

    # Reflections
    refl = portfolio.get("reflections", {})
    story.append(Paragraph("<b>Reflections</b>", styles["Heading2"]))
    for k in ["strategy","challenge","next"]:
        if refl.get(k):
            story.append(Paragraph(f"<b>{k.capitalize()}:</b> {refl[k]}", styles["Normal"]))
            story.append(Spacer(1, 6))

    doc = SimpleDocTemplate(out_path, pagesize=letter)
    doc.build(story)
    return out_path
