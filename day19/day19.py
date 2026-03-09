#Script-to-slide outline agent
import json
from openai import OpenAI
from datetime import date
 
client = OpenAI()  # requires OPENAI_API_KEY
 
SYSTEM_PROMPT = """
You are a Script-to-Slide Outline Agent.
 
Rules:
- Convert the script into a slide outline
- One main idea per slide
- Use concise bullet points
- Do NOT include full sentences unless necessary
- Optimize for visual presentation
 
Return ONLY valid JSON with this schema:
 
{
  "slides": [
    {
      "title": "",
      "bullets": []
    }
  ]
}
"""
 
def read_input(path="input.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
 
def generate_slides(script_text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": script_text}
        ],
        temperature=0.35
    )
    return json.loads(response.choices[0].message.content)
 
def save_outputs(data):
    with open("slides.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("slides.txt", "w", encoding="utf-8") as f:
        f.write(f"Slide Outline ({date.today()})\n")
        f.write("=" * 45 + "\n\n")
        for i, slide in enumerate(data["slides"], 1):
            f.write(f"Slide {i}: {slide['title']}\n")
            for b in slide["bullets"]:
                f.write(f"- {b}\n")
            f.write("\n")
 
def main():
    script = read_input()
    slides = generate_slides(script)
    save_outputs(slides)
    print("Slide outline generated successfully.")
 
if __name__ == "__main__":
    main()
