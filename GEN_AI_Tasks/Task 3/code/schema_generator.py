from google import genai
import os

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client

def generate_schema(modules: list) -> list:
    prompt = f"""
Design a simple database schema.

Modules:
{', '.join(modules)}

Rules:
- Use table format
- table_name(field1, field2, field3)
- One table per line
"""

    try:
        response = _get_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        schema = [
            line.strip()
            for line in response.text.split("\n")
            if line.strip()
        ]
        return schema
    except Exception as e:
        print(f"⚠️ Gemini failed for schema: {e}")
        return [
            "users(id, name, email, phone, password_hash, created_at)",
            "restaurants(id, name, address, cuisine_type, rating, owner_id)",
            "menu_items(id, restaurant_id, name, price, category, is_available)",
            "orders(id, user_id, restaurant_id, status, total_price, created_at)",
            "order_items(id, order_id, menu_item_id, quantity, price)",
            "payments(id, order_id, method, status, amount, transaction_id)",
            "deliveries(id, order_id, driver_id, status, location_lat, location_lng)",
            "drivers(id, name, phone, vehicle_type, is_available)",
            "reviews(id, user_id, restaurant_id, rating, comment, created_at)"
        ]
