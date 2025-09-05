from gtts import gTTS
import json

with open("Week4/data/student_template.json") as f:
    data = json.load(f)

for i, p in enumerate(data["project"]["panels"], 1):
    if p["latin_text"]:
        tts = gTTS(p["latin_text"], lang="la")
        out_file = f"Week4/audio/panel{i}.mp3"
        tts.save(out_file)
        print(f"Generated {out_file}")
