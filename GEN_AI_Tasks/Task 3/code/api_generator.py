from google import genai
import os

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client

def generate_apis(modules: list) -> list:
    prompt = f"""
Generate REST API endpoints.

Modules:
{', '.join(modules)}

Rules:
- Format: METHOD /endpoint
- One API per line
"""

    try:
        response = _get_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        apis = [
            line.strip()
            for line in response.text.split("\n")
            if line.strip()
        ]
        return apis
    except Exception as e:
        print(f"⚠️ Gemini failed for APIs: {e}")
        return [
            "POST /auth/register", "POST /auth/login", "GET /restaurants",
            "GET /restaurants/{id}/menu", "POST /orders", "GET /orders/{id}",
            "PUT /orders/{id}/status", "POST /payments", "GET /deliveries/{id}",
            "PUT /deliveries/{id}/location", "POST /reviews", "GET /users/profile"
        ]
