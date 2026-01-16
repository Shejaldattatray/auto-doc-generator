import os

SRC_DIR = "src"
OUTPUT_FILE = "docs/AUTO_DOCS.md"

def main():
    docs = ["# Auto Generated Documentation\n"]

    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                docs.append(f"## {path}\n")
                docs.append("Documentation placeholder\n")
                docs.append("---\n")

    os.makedirs("docs", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(docs))

    print("Docs generated successfully")

if __name__ == "__main__":
    main()





