import os

# import google.generativeai as genai

from google import genai

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY)


def generate_workout_gemini(user_input: dict) -> str:
    if not API_KEY:
        return "Error: GOOGLE_API_KEY is not configured."

    goal = user_input.get("goal", "general fitness")
    intensity = user_input.get("intensity", "medium")

    prompt = f'''
You are a professional fitness trainer assistant.

Create a personalized, structured 7-day workout plan for a user with the goal of
"{goal}" and preferred workout intensity "{intensity}".

For each day include:
- Warm-up (5-10 minutes)
- Main workout with exercise names, sets, and reps or duration
- Cooldown or recovery guidance

Keep the plan practical, clearly organized by Day 1 through Day 7, and suitable
for a general wellness application. Avoid making medical diagnoses or claiming
the plan is suitable for a specific medical condition.
'''

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        return f"Error generating workout plan: {exc}"
