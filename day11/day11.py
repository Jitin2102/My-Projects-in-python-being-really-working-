
import json
from datetime import date
from openai import OpenAI
 
client = OpenAI()  # requires OPENAI_API_KEY
 
SYSTEM_PROMPT = """
You are a Blog Post Generator Agent.
 
Your job:
- Generate a well-structured blog post
- Adapt tone and depth to the target audience
- Use clear section headers
- Keep writing concise and readable
- Avoid fluff and repetition
 
Return ONLY valid JSON with this schema:
 
{
  "title": "",
  "sections": [
    {
      "header": "",
      "content": ""
    }
  ],
  "conclusion": ""
}
"""
 
def read_blog_input(path="blog.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
 
def generate_blog(blog_instructions):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": blog_instructions}
        ],
        temperature=0.4
    )
    return json.loads(response.choices[0].message.content)
 
def save_outputs(blog):
    with open("blog.json", "w", encoding="utf-8") as f:
        json.dump(blog, f, indent=2)
 
    with open("blog.txt", "w", encoding="utf-8") as f:
        f.write(f"{blog['title']}\n")
        f.write("=" * len(blog["title"]) + "\n\n")
 
        for s in blog["sections"]:
            f.write(f"{s['header']}\n")
            f.write("-" * len(s["header"]) + "\n")
            f.write(s["content"] + "\n\n")
 
        f.write("Conclusion\n")
        f.write("-" * 10 + "\n")
        f.write(blog["conclusion"] + "\n")
 
def main():
    instructions = read_blog_input()
    blog = generate_blog(instructions)
    save_outputs(blog)
    print("Blog post generated successfully.")
    print(blog["title"])
 
if __name__ == "__main__":
    main()
