import whisper
import json
import os

model = whisper.load_model("large-v2")

AUDIO_DIR = "audios"
OUTPUT_DIR = "Chunks"

os.makedirs(OUTPUT_DIR, exist_ok=True)

audios = os.listdir(AUDIO_DIR)

for audio in audios:
    if not audio.lower().endswith(".mp3"):
        continue

    if "_" not in audio:
        continue

    number_part, title_part = audio.split("_", 1)

    number = number_part.strip()
    title = title_part.rsplit(".", 1)[0].strip()

    result = model.transcribe(
        audio=os.path.join(AUDIO_DIR, audio),
        task="translate",
        word_timestamps=False
    )

    chunks = []
    for segment in result["segments"]:
        chunks.append({
            "number": number,
            "title": title,
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"]
        })

    output_data = {
        "chunks": chunks,
        "text": result["text"]
    }

    output_path = os.path.join(OUTPUT_DIR, f"{audio}.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
