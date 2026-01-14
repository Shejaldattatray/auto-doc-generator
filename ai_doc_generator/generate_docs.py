import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")


def generate_doc(code_block, name):
    prompt = f"""
Explain the following Python code in simple terms.

Name: {name}

Code:
{code_block}

Provide:
- What it does
- Inputs
- Outputs
"""

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    sample_code = "def add(a, b): return a + b"
    print(generate_doc(sample_code, "add"))

