import json
import numpy as np
from openai import OpenAI
from datetime import date
import os

OPEN_AI_API_KEY = ""  # enter your api key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", OPEN_AI_API_KEY))

EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4.1-mini"


def read_notes(path=r"C:\Users\HP\Python\Projects\Agents\day5.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def embed_texts(texts):
    response = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [e.embedding for e in response.data]


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def store_knowledge(chunks, embeddings):
    records = []
    for text, emb in zip(chunks, embeddings):
        records.append(
            {"text": text, "embedding": emb, "created": date.today().isoformat()}
        )
    with open("knowledge.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    return records


def load_knowledge():
    with open("knowledge.json", "r", encoding="utf-8") as f:
        return json.load(f)


def retrieve(query, records, top_k=3):
    query_emb = embed_texts([query])[0]
    scored = []
    for r in records:
        score = cosine_similarity(query_emb, r["embedding"])
        scored.append((score, r["text"]))
    scored.sort(reverse=True)
    return [text for _, text in scored[:top_k]]


def answer_query(query, contexts):
    prompt = f"""
Answer the following question using ONLY the provided notes.

Notes:
{chr(10).join(contexts)}

Question:
{query}
"""
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


def main():
    print("Ingesting notes...")
    chunks = read_notes()
    embeddings = embed_texts(chunks)
    records = store_knowledge(chunks, embeddings)

    print("Knowledge base ready.")
    query = input("\nAsk a question: ")
    top_contexts = retrieve(query, records)
    answer = answer_query(query, top_contexts)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()
