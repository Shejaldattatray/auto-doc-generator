import os
import google.generativeai as genai

SRC_DIR = "src"
OUTPUT_FILE = "docs/AUTO_DOCS.md"

def read_source_code():
    code_blocks = []
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    code = f.read()
                code_blocks.append((path, code))
    return code_blocks


def generate_documentation(code_blocks):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-pro")

    docs = ["# 📘 Auto Generated Documentation\n"]

    for path, code in code_blocks:
        prompt = f"""
Explain the following Python code in simple terms.
Include:
- What the file does
- Important functions/classes
- Inputs and outputs

Code:
{code}
"""
        response = model.generate_content(prompt)
        docs.append(f"## {path}\n")
        docs.append(response.text)
        docs.append("\n---\n")

    return "\n".join(docs)


def write_docs(content):
    os.makedirs("docs", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    code_blocks = read_source_code()
    documentation = generate_documentation(code_blocks)
    write_docs(documentation)
    print("✅ Documentation generated successfully")




