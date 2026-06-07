from services.gemini_service import generate_documentation

response = generate_documentation(
    """
def add(a,b):
    return a+b
"""
)

print(response)