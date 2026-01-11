import os
import json
import re

INPUT_FOLDER = "Texts"
OUTPUT_FOLDER = "Chunks"

def to_seconds(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)

def format_mm_ss(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def extract_number_title(filename):
    name = filename.replace(".txt", "")
    match = re.match(r"Lecture\s*(\d+)[_-](.*)", name)
    if match:
        return match.group(1), match.group(2)
    return "", name

for file in os.listdir(INPUT_FOLDER):
    if not file.endswith(".txt"):
        continue

    lecture_number, lecture_title = extract_number_title(file)

    with open(os.path.join(INPUT_FOLDER, file), "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    entries = []
    full_text_parts = []   #  collect full lecture text

    for line in lines:
        parts = line.split(" ", 1)
        if len(parts) != 2:
            continue

        timestamp, text = parts

        if timestamp.count(":") != 2:
            continue

        start = to_seconds(timestamp)
        entries.append({"start": start, "text": text})
        full_text_parts.append(text)   

    chunks = []

    for i in range(len(entries)):
        start = entries[i]["start"]
        end = entries[i + 1]["start"] if i + 1 < len(entries) else start + 5

        chunks.append({
            "number": lecture_number,
            "title": lecture_title,
            "start": format_mm_ss(start),
            "end": format_mm_ss(end),
            "text": entries[i]["text"]
        })
        
    #  final combined text
    full_text = " ".join(full_text_parts)  

    json_name = file.replace(".txt", ".json")
    json_path = os.path.join(OUTPUT_FOLDER, json_name)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "chunks": chunks,
                "text": full_text
            },
            f,
            indent=2
        )

    print(f"Created: {json_path}")
