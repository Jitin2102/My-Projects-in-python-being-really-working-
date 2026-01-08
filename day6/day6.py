import json
from datetime import date
from openai import OpenAI

client = OpenAI()  # requires OPENAI_API_KEY

SYSTEM_PROMPT = """
You are a Daily Goal Reflection Agent.

Your task:
- Compare planned goals with actual outcomes
- Identify what was completed and what was missed
- Analyze reasons for misses
- Extract insights and lessons
- Provide 2–3 actionable suggestions for tomorrow

Return ONLY valid JSON with this schema:

{
  "summary": "",
  "completed_goals": [],
  "missed_goals": [],
  "insights": [],
  "lessons_learned": [],
  "tomorrow_suggestions": []
}
"""

def read_day(path="day.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def reflect(day_text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": day_text}
        ],
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)

def save_outputs(data):
    with open("reflection.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("reflection.txt", "w", encoding="utf-8") as f:
        f.write(f"Daily Reflection ({date.today()})\n")
        f.write("=" * 45 + "\n\n")

        f.write("SUMMARY:\n")
        f.write(data["summary"] + "\n\n")

        f.write("COMPLETED GOALS:\n")
        for g in data["completed_goals"]:
            f.write(f"- {g}\n")

        f.write("\nMISSED GOALS:\n")
        for g in data["missed_goals"]:
            f.write(f"- {g}\n")

        f.write("\nINSIGHTS:\n")
        for i in data["insights"]:
            f.write(f"- {i}\n")

        f.write("\nLESSONS LEARNED:\n")
        for l in data["lessons_learned"]:
            f.write(f"- {l}\n")

        f.write("\nSUGGESTIONS FOR TOMORROW:\n")
        for s in data["tomorrow_suggestions"]:
            f.write(f"- {s}\n")

def main():
    day_text = read_day()
    reflection = reflect(day_text)
    save_outputs(reflection)
    print("Daily reflection generated successfully.")
    print(reflection)

if __name__ == "__main__":
    main()
