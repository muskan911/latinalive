# LatinAlive — AI, Comics, and Gamification for Latin Learning

## Overview
LatinAlive is an experimental teaching module that combines AI-assisted Latin grammar support, AI-generated comic panels, and interactive games to make Latin learning accessible and engaging.

This repository contains:
- AI-generated Latin sentences with English translations
- Morphosyntactic analysis using NLP tools (Stanza, CLTK, spaCy Latin model)
- AI-generated illustrations for comic panels
- Templates for labeling activities
- A Streamlit demo app for live Latin parsing

## Tools & Technologies
- **Text AI**: ChatGPT (Latin sentence drafting & refinement)
- **NLP Parsing**: Stanza (Latin model), CLTK, spaCy (Latin model)
- **Image Generation**: DALL·E
- **Design & Layout**: Canva
- **Collaboration**: Google Drive for asset sharing
- **Web Demo**: Streamlit

## Folder Structure
```
latinalive/
├─ README.md
├─ Week1/
│  ├─ images/               # Comic panel images
│  ├─ canva_exports/        # Exported labeled comic layouts
│  ├─ scripts/              # NLP parsing scripts
│  ├─ prompts/              # Prompts for text & images
│  ├─ data/                 # CSV or JSON with scenes & translations
└─ docs/
   └─ weekly_reports/
```

## Running the Demo
1. Install Python 3.9+ and pip.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  
   pip install stanza streamlit
   ```
3. Download Stanza Latin model:
   ```python
   import stanza
   stanza.download('la')
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run Week1/scripts/app.py
   ```

## Credits
- Latin text: Generated with ChatGPT + verified with CLTK and Stanza
- Images: Generated with DALL·E
- Layout: Canva