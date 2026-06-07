import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    raise ValueError("GEMINI_API_KEY not found!")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-2.0-flash-lite"
)


def generate_documentation(code):

    prompt = f"""
    Analyze the Python code below.

    Generate professional markdown documentation.

    Include:

    - Purpose
    - Functions
    - Parameters
    - Return values

    Code:

    {code}
    """

    response = model.generate_content(prompt)

    return response.text


def generate_project_summary(documentation_text):

    prompt = f"""
    Create a professional README.md file.

    Include:

    1. Project Overview
    2. Modules
    3. Features
    4. Summary of each module

    Documentation:

    {documentation_text}
    """

    response = model.generate_content(prompt)

    return response.text