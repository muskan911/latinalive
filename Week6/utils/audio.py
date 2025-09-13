from gtts import gTTS
import os

def generate_audio(text, out_path):
    if not text.strip():
        return None
    tts = gTTS(text, lang='la')
    tts.save(out_path)
    return out_path
