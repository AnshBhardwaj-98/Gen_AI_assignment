from google import genai
import os

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client

def generate_pseudocode(requirement: str) -> str:
    prompt = f"""
Write high-level pseudocode for this system.

Requirement:
{requirement}

Rules:
- Use IF, ELSE, LOOP
- Plain text
"""

    try:
        response = _get_client().models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Gemini failed for pseudocode: {e}")
        return """BEGIN FoodDeliveryApp

  FUNCTION UserLogin(email, password):
    IF user exists AND password matches THEN
      RETURN auth_token
    ELSE
      RETURN error "Invalid credentials"

  FUNCTION BrowseRestaurants(location):
    FETCH all restaurants near location
    RETURN sorted list by rating

  FUNCTION PlaceOrder(user_id, restaurant_id, items):
    VALIDATE items are available
    CREATE order record
    CALCULATE total price
    TRIGGER payment flow
    IF payment successful THEN
      NOTIFY restaurant
      ASSIGN delivery driver
    ELSE
      RETURN error "Payment failed"

  FUNCTION TrackDelivery(order_id):
    LOOP UNTIL order status == "delivered":
      FETCH driver location
      UPDATE delivery status
      PUSH notification to user

END FoodDeliveryApp"""
