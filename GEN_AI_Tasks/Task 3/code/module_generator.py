from google import genai
import os

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client

def generate_modules(requirement: str) -> list:
    prompt = f"""
You are a software architect.

From the following business requirement,
list system modules.

Rules:
- Output only module names
- One module per line
- No numbering

Requirement:
{requirement}
"""

    try:
        response = _get_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        modules = [
            line.strip()
            for line in response.text.split("\n")
            if line.strip()
        ]
        return modules
    except Exception as e:
        print(f"⚠️ Gemini failed for modules: {e}")
        return [
            "User Management", "Restaurant Management", "Menu Management",
            "Order Management", "Payment Processing", "Delivery Tracking",
            "Notification Service", "Rating & Review", "Admin Dashboard"
        ]
