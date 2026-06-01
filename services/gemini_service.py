import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
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