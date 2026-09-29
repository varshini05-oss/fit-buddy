import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def generate_workout_gemini(user_input: dict) -> str:
    if client is None:
        return "Error: GEMINI_API_KEY is not configured."

    goal = user_input.get("goal", "general fitness")
    intensity = user_input.get("intensity", "medium")

    prompt = f"""
You are a professional fitness trainer assistant.

Create a personalized, structured 7-day workout plan for a user with the goal
of "{goal}" and preferred workout intensity "{intensity}".

For each day include:
- Warm-up
- Main workout
- Exercises
- Sets and repetitions or duration
- Cooldown or recovery guidance

Keep the plan practical and clearly organized from Day 1 through Day 7.
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        if not response.text:
            return "Error generating workout plan: Gemini returned an empty response."

        return response.text.strip()

    except Exception as e:
        return f"Error generating workout plan: {e}"