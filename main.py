import os
import json
import hashlib

from services.gemini_service import (
    generate_documentation,
    generate_project_summary
)

SOURCE_FOLDER = "sample_code"
DOCS_FOLDER = "docs"
HASH_FILE = "file_hashes.json"


def get_file_hash(file_path):
    with open(file_path, "rb") as file:
        return hashlib.md5(file.read()).hexdigest()


# Load previous hashes
if os.path.exists(HASH_FILE):
    with open(HASH_FILE, "r") as file:
        file_hashes = json.load(file)
else:
    file_hashes = {}

updated_hashes = {}
all_documentation = ""

for filename in os.listdir(SOURCE_FOLDER):

    if not filename.endswith(".py"):
        continue

    file_path = os.path.join(SOURCE_FOLDER, filename)

    current_hash = get_file_hash(file_path)

    updated_hashes[filename] = current_hash

    if file_hashes.get(filename) == current_hash:
        print(f"Skipping {filename} (no changes)")
        continue

    print(f"Generating docs for {filename}")

    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()

    documentation = generate_documentation(code)

    all_documentation += f"\n# {filename}\n"
    all_documentation += documentation
    all_documentation += "\n\n"

    output_file = filename.replace(".py", ".md")

    with open(
        os.path.join(DOCS_FOLDER, output_file),
        "w",
        encoding="utf-8"
    ) as doc_file:

        doc_file.write(documentation)

# Generate project README
if all_documentation:

    print("Generating project README...")

    readme_content = generate_project_summary(
        all_documentation
    )

    with open(
        os.path.join(DOCS_FOLDER, "README.md"),
        "w",
        encoding="utf-8"
    ) as readme_file:

        readme_file.write(readme_content)

# Save hashes
with open(HASH_FILE, "w") as file:
    json.dump(updated_hashes, file, indent=4)

print("Documentation process completed!")