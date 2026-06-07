from flask import Flask, render_template, request
from git import Repo
from services.groq_service import (
    generate_documentation,
    generate_code_review
)
import os
import uuid

app = Flask(__name__)

REPO_FOLDER = "repositories"
os.makedirs(REPO_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    repo_url = request.form.get("repo_url")

    repo_path = os.path.join(
        REPO_FOLDER,
        str(uuid.uuid4())
    )

    Repo.clone_from(repo_url, repo_path)

    files_found = []

    documentation_preview = ""
    review_preview = ""

    # Find Python files
    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if file.endswith(".py"):
                files_found.append(file)

    # Find first Python file
    first_python_file = None

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if file.endswith(".py"):

                first_python_file = os.path.join(
                    root,
                    file
                )

                break

        if first_python_file:
            break

    if first_python_file:

        with open(
            first_python_file,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            code = f.read()[:1000]

        try:

            print("Generating Documentation...")

            documentation_preview = generate_documentation(code)

            review_preview = ""

        except Exception as e:

            print(e)

            documentation_preview = (
                f"Error:\n\n{str(e)}"
            )

            review_preview = (
                f"Error:\n\n{str(e)}"
            )

    repo_name = repo_url.split("/")[-1]

    return render_template(
        "index.html",
        files=files_found,
        documentation=documentation_preview,
        review=review_preview,
        message=f"Repository: {repo_name}",
        status="Analysis Complete"
    )
@app.route("/review", methods=["POST"])
def review():

    repo_url = request.form.get("repo_url")

    repo_path = os.path.join(
        REPO_FOLDER,
        str(uuid.uuid4())
    )

    Repo.clone_from(repo_url, repo_path)

    files_found = []

    review_preview = ""

    first_python_file = None

    for root, dirs, files in os.walk(repo_path):

        for file in files:

            if file.endswith(".py"):

                files_found.append(file)

                if first_python_file is None:

                    first_python_file = os.path.join(
                        root,
                        file
                    )

    if first_python_file:

        with open(
            first_python_file,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            code = f.read()[:1000]

        review_preview = generate_code_review(code)

    repo_name = repo_url.split("/")[-1]

    return render_template(
        "index.html",
        files=files_found,
        review=review_preview,
        documentation="",
        message=f"Repository: {repo_name}",
        status="Code Review Complete"
    )

if __name__ == "__main__":
    app.run(debug=True)
