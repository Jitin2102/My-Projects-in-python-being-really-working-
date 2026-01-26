import json
from datetime import date
from openai import OpenAI

client = OpenAI() # requires an open-ai api key

SYSTEM_PROMPT = """
You are a Grammar Correction Agent.

Rules:
- Correct grammar, spelling, and punctuation
- Improve clarity while preserving original meaning
- Do NOT rewrite content or change tone
- Do NOT add new information
- Keep edits minimal

Return ONLY valid JSON with this schema:

{
  "corrected_text": "",
  "notes": []
}
"""


def read_input(path=r"C:\Users\HP\Python\Projects\Agents\input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def correct_text(raw_text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text},
        ],
        temperature=0.1,
    )
    return json.loads(response.choices[0].message.content)


def save_outputs(data):
    with open("corrected.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("corrected.txt", "w", encoding="utf-8") as f:
        f.write(f"Corrected Text ({date.today()})\n")
        f.write("=" * 45 + "\n\n")
        f.write(data["corrected_text"] + "\n")


def main():
    raw_text = read_input()
    corrected = correct_text(raw_text)
    save_outputs(corrected)
    print("Grammar correction complete.")
    print(corrected["corrected_text"])


if __name__ == "__main__":
    main()
