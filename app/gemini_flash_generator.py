import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY)


def generate_nutrition_tip_with_flash(goal: str) -> str:
    if not API_KEY:
        return "Error: GOOGLE_API_KEY is not configured."

    prompt = f'''
Give one concise, practical nutrition or recovery tip for someone whose fitness
goal is "{goal}".

Keep it friendly and easy to understand. Focus on general wellness, hydration,
balanced nutrition, protein sources, or recovery habits. Do not provide medical
treatment or diagnose health conditions.
'''

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        return f"Error generating nutrition tip: {exc}"
