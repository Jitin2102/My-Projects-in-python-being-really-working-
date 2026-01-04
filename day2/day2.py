import json
from datetime import date
from openai import OpenAI
import os

OPEN_AI_API_KEY = ""  # enter your api key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", OPEN_AI_API_KEY))

SYSTEM_PROMPT = """
    You are an Email Summarizing Agent.

    Your job:
     1. Summarize the email in 2-3 sentences
     2. Extract key points
     3.Extract action items (who should what)
     4.Identify deadlines
     5. Classify urgency :Low,Medium,High

    Return ONLY valid JSON with this schema :

    {
        "summary":"",
        "key-points":[],
        "action-items" :[],
        "deadlines" :[],
        "urgency":""
    }

"""


def read_email(path=r"C:\Users\HP\Python\Projects\Agents\email.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def summarize_email(email_txt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": email_txt},
        ],
        temperature=0.2,
    )
    return json.loads(response.choices[0].message.content)


def save_output(data):
    with open("summary.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("summary.txt", "w", encoding="utf") as f:
        f.write(f"Email Summary({date.today()}) \n")
        f.write("=" * 40 + "\n\n")
        f.write("Summary:\n")
        f.write(data["summary"] + "\n\n")

        f.write("KEY POINTS:\n")
        for p in data["key-points"]:
            f.write(f"-{p}\n")

        f.write("\nACTION ITEMS:\n")
        for a in data["action-items"]:
            f.write(f"-{a}\n")

        f.write("\nDEADLINES:\n")
        for d in data["deadlines"]:
            f.write(f"-{d}\n")

        f.write(f"\nURGENCY:{data['urgency']}\n")


def main():
    email_txt = read_email()
    result = summarize_email(email_txt)
    save_output(result)
    print("Email summarized suceesfully.")
    print(result)


if __name__ == "__main__":
    main()
