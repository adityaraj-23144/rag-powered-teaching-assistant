import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
import pandas as pd

OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"

EMBED_MODEL = "bge-m3"
LLM_MODEL = "llama3.2"

EMBEDDING_FILE = "embeddings/all_lectures_embeddings.joblib"
TOP_K = 5

def ollama_embed(input_texts):
    r = requests.post(
        OLLAMA_EMBED_URL,
        json={"model": EMBED_MODEL, "input": input_texts},
        timeout=120
    )
    return r.json()


def inference(prompt):
    r = requests.post(
        OLLAMA_GENERATE_URL,
        json={"model": LLM_MODEL, "prompt": prompt, "stream": False},
        timeout=300
    )
    return r.json()


df = joblib.load(EMBEDDING_FILE)
print(f"Loaded {len(df)} embedded chunks")


# Asking Query

incoming_query = input("Ask a Question: ").strip()

embed_response = ollama_embed([incoming_query])

if "embedding" in embed_response:
    question_embedding = embed_response["embedding"]
elif "embeddings" in embed_response:
    question_embedding = embed_response["embeddings"][0]
else:
    raise RuntimeError(f"Failed to embed query: {embed_response}")


# Cosine Similarity

embedding_matrix = np.vstack(df["embedding"].values)

similarities = cosine_similarity(
    embedding_matrix,
    np.array(question_embedding).reshape(1, -1)
).flatten()

top_indices = similarities.argsort()[::-1][:TOP_K]
new_df = df.loc[top_indices]


# System Prompt

prompt = f"""
You are a teaching assistant for the NPTEL course “Internet of Things”.

You are given subtitle excerpts from lecture videos with lecture title,
lecture number, start time, end time, and spoken text.

Answer the student’s question ONLY using this information.
Explain clearly in simple language.

Always mention:
- which lecture(s)
- exact timestamp(s)
where the topic is explained, and guide the student to rewatch that part.

If the question is not covered in the IoT course, say so clearly.
Do not mention internal data formats or technical processing details.

Lecture data:
{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records", indent=2)}

---------------------------------
Student question:
"{incoming_query}"
"""

with open("prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)


# LLM Response

response_json = inference(prompt)

if "response" not in response_json:
    raise RuntimeError(f"LLM generation failed: {response_json}")

final_answer = response_json["response"]

print("\n🧠 Answer:\n")
print(final_answer)

with open("response.txt", "w", encoding="utf-8") as f:
    f.write(final_answer)
