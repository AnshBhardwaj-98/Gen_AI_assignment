from google import genai
import os

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client

def generate_seo_keywords(product_name):
    """
    Generates 3–4 SEO keywords for the product
    """

    try:
        prompt = f"""
Generate 4 SEO keywords for a blog about this product:
{product_name}

Rules:
- Short keywords
- High buying intent
- Comma separated
"""

        response = _get_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        keywords = response.text.strip().split(",")
        return [k.strip() for k in keywords][:4]

    except Exception as e:
        print(f"⚠️ Gemini failed: {e}")
        # Fallback
        base = product_name.lower().split()[:3]
        return [
            "best " + " ".join(base),
            "buy " + " ".join(base),
            "top " + " ".join(base),
            " ".join(base) + " review"
        ]
