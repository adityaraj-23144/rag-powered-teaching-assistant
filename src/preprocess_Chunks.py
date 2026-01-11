import requests
import os
import json
import pandas as pd
import re
import time
import joblib

OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
MODEL_NAME = "bge-m3"

CHUNKS_DIR = "Chunks"
OUTPUT_DIR = "embeddings"
OUTPUT_FILE = "all_lectures_embeddings.joblib"

BATCH_SIZE = 8   

def clean_text(text):
    if not text:
        return None
    text = text.strip()
    if len(text) < 10:
        return None
    if not re.search(r"[a-zA-Z]", text):
        return None
    return text


def ollama_embed(input_texts):
    r = requests.post(
        OLLAMA_EMBED_URL,
        json={"model": MODEL_NAME, "input": input_texts},
        timeout=120
    )
    return r.json()


def safe_embed_batch(texts):
    try:
        data = ollama_embed(texts)

        if "embeddings" in data:
            return data["embeddings"]
        if "embedding" in data:
            return [data["embedding"]]

        raise RuntimeError(data)

    except Exception:
        embeddings = []
        for t in texts:
            try:
                single = ollama_embed([t])
                if "embedding" in single:
                    embeddings.append(single["embedding"])
                elif "embeddings" in single:
                    embeddings.append(single["embeddings"][0])
                else:
                    embeddings.append(None)
            except Exception:
                embeddings.append(None)

            time.sleep(0.2)

        return embeddings


os.makedirs(OUTPUT_DIR, exist_ok=True)

json_files = [f for f in os.listdir(CHUNKS_DIR) if f.endswith(".json")]
print(f" Found {len(json_files)} JSON files")

records = []
global_chunk_id = 0

for json_file in json_files:
    print(f"\n Processing: {json_file}")

    with open(os.path.join(CHUNKS_DIR, json_file), encoding="utf-8") as f:
        content = json.load(f)

    clean_chunks = []

    for c in content.get("chunks", []):
        txt = clean_text(c.get("text", ""))
        if txt:
            clean_chunks.append({
                "source_file": json_file,
                "number": c.get("number"),
                "title": c.get("title"),
                "start": c.get("start"),
                "end": c.get("end"),
                "text": txt
            })

    print(f"   Valid chunks: {len(clean_chunks)}")

    for i in range(0, len(clean_chunks), BATCH_SIZE):
        batch = clean_chunks[i:i + BATCH_SIZE]
        texts = [c["text"] for c in batch]

        print(f"  🔹 Embedding batch {i//BATCH_SIZE + 1}")

        batch_embeddings = safe_embed_batch(texts)

        for j, emb in enumerate(batch_embeddings):
            if emb is None:
                continue

            records.append({
                "chunk_id": global_chunk_id,
                "source_file": batch[j]["source_file"],
                "number": batch[j]["number"],
                "title": batch[j]["title"],
                "start": batch[j]["start"],
                "end": batch[j]["end"],
                "text": batch[j]["text"],
                "embedding": emb
            })
            global_chunk_id += 1


df = pd.DataFrame.from_records(records)

output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
joblib.dump(df, output_path)

print("\n FULL INGESTION COMPLETE")
print(f" Saved to: {output_path}")
print(f" Total chunks embedded: {len(df)}")
print(f" Embedding dimension: {len(df.iloc[0]['embedding'])}")
