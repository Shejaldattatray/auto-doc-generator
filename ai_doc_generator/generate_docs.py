import os
import requests
import json

SRC_DIR = "src"
OUTPUT_FILE = "docs/AUTO_DOCS.md"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def generate_with_gemini(code):
    if not GEMINI_API_KEY:
        return "Gemini API key not provided. Skipping AI generation."

    url = (
        "https://generativelanguage.googleapis.com/v1/models/"
        "gemini-1.5-flash:generateContent"
        f"?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [{
            "parts": [{"text": "Explain this Python code:\n\n" + code}]
        }]
    }

    try:
        r = requests.post(url, json=payload, timeout=30)
        if r.status_code != 200:
            return f"Gemini error: {r.text}"
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Gemini request failed: {e}"

def main():
    docs = ["# Auto Generated Documentation\n"]

    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path) as f:
                    code = f.read()

                docs.append(f"## {path}\n")
                docs.append(generate_with_gemini(code))
                docs.append("\n---\n")

    os.makedirs("docs", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(docs))

    print("Docs generated successfully")

if __name__ == "__main__":
    main()






