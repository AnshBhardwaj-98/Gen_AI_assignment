from google import genai
import os

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client

def generate_blog(product, keywords):
    """
    Generates SEO blog content
    """

    prompt = f"""
Write a 150-200 word SEO blog post.

Product Name: {product['name']}
Category: {product['category']}
Keywords: {", ".join(keywords)}

Rules:
- Natural tone
- No keyword stuffing
- Promotional but informative
"""

    try:
        response = _get_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Gemini failed: {e}")
        return (
            f"Introducing the **{product['name']}** — a top pick in the "
            f"{product['category']} category.\n\n"
            f"{product.get('description', '')}\n\n"
            f"Whether you're looking for {keywords[0]} or searching for {keywords[1]}, "
            f"this product delivers exceptional quality and value. "
            f"Don't miss your chance to own one of the best {keywords[2]} on the market today."
        )
