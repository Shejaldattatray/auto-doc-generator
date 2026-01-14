import ast
import os

SRC_DIR = "src"

def extract_from_file(filepath):
    with open(filepath, "r") as f:
        tree = ast.parse(f.read())

    items = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            items.append({
                "type": "function",
                "name": node.name,
                "code": ast.get_source_segment(open(filepath).read(), node)
            })
        elif isinstance(node, ast.ClassDef):
            items.append({
                "type": "class",
                "name": node.name,
                "code": ast.get_source_segment(open(filepath).read(), node)
            })

    return items


def extract_code():
    extracted = []

    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                extracted.append({
                    "file": path,
                    "items": extract_from_file(path)
                })

    return extracted


if __name__ == "__main__":
    data = extract_code()
    print(data)


