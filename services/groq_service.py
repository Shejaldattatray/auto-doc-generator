from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_documentation(code):

    prompt = f"""
    Analyze this Python code.

    Generate professional documentation.

    Include:

    - Purpose
    - Functions
    - Parameters
    - Return Values

    Code:

    {code}
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content


def generate_code_review(code):

    prompt = f"""
    Review this Python code.

    Provide:

    1. Code Quality Analysis
    2. Bugs or Risks
    3. Performance Improvements
    4. Security Concerns
    5. Best Practices

    Code:

    {code}
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content