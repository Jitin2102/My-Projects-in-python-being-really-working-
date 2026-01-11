import json
from datetime import date
from openai import OpenAI

client = OpenAI(
    api_key=""  # enter your api key
)

SYSTEM_PROMPT = """
You are a Note-to-Action Item Agent.

Your job:
- Extract ONLY actionable tasks from the notes
- Ignore ideas, opinions, or decisions without actions
- Identify owner if mentioned; otherwise use "Unassigned"
- Suggest a deadline if implied; otherwise "Not specified"
- Assign priority: Low, Medium, or High

Return ONLY valid JSON with this schema:

{
  "actions": [
    {
      "action": "",
      "owner": "",
      "deadline": "",
      "priority": "",
      "source_context": ""
    }
  ]
}
"""


def read_notes(path=r"C:\Users\HP\Python\Projects\Agents\day8.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_actions(notes_text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": notes_text},
        ],
        temperature=0.2,
    )
    return json.loads(response.choices[0].message.content)


def save_outputs(data):
    with open("actions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("actions.txt", "w", encoding="utf-8") as f:
        f.write(f"Extracted Action Items ({date.today()})\n")
        f.write("=" * 45 + "\n\n")

        for i, a in enumerate(data["actions"], 1):
            f.write(f"{i}. {a['action']}\n")
            f.write(f"   Owner: {a['owner']}\n")
            f.write(f"   Deadline: {a['deadline']}\n")
            f.write(f"   Priority: {a['priority']}\n")
            f.write(f"   Source: {a['source_context']}\n\n")


def main():
    notes_text = read_notes()
    actions = extract_actions(notes_text)
    save_outputs(actions)
    print("Action items extracted successfully.")
    print(actions)


if __name__ == "__main__":
    main()
