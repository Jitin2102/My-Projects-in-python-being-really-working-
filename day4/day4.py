import json
from openai import OpenAI
from datetime import date
import os

OPEN_AI_API_KEY = ""  # enter your api key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", OPEN_AI_API_KEY))

SYSTEM_PROMPT = """
You are a Meeting Agenda Generator Agent.

Your job is to generate a clear, time-boxed meeting agenda.

Rules:
- Agenda must fit within the provided duration.
-Focus on the meeting objective .
-Include time allocation for each item.
-Identify decision points where applicable
-Return only valid json with this schema .
{
    "meeting_title":"",
    "objective":"",
    "agenda" :[
        {
            "topic":"",
            "time_minutes":0,
            "owner":"",
            "outcome":""
        }
    ]
}
"""


def read_input(path=r"C:\Users\HP\Python\Projects\Agents\calendar.csv"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def generate_agenda(meeting_txt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": meeting_txt},
        ],
        temperature=0.2,
    )
    return json.loads(response.choices[0].message.content)


def save_output(data):
    total_duration = sum(item["time_minutes"] for item in data["agenda"])
    with open("agenda.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    with open("agenda.txt", "w", encoding="utf-8") as f:
        f.write(f"Meeting Agenda ({date.today()})\n")
        f.write("=" * 45 + "\n\n")
        f.write(f"Title:{data['meeting_title']}\n")
        f.write(f"Objective: {data['objective']}\n")
        f.write(f"Duration :{total_duration} minutes\n\n")

        for i, item in enumerate(data["agenda"], 1):
            f.write(f"{i}. {item['topic']} ({item['time_minutes']} min)\n")
            f.write(f"  Owner :{item['owner']}\n")
            f.write(f"  Outcome :{item['outcome']}\n\n")


def main():
    meeting_text = read_input()
    agenda = generate_agenda(meeting_text)
    save_output(agenda)
    print("Meeting Agenda Generated............")
    print(agenda)


if __name__ == "__main__":
    main()
