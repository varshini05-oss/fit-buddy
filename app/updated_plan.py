import os


from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY)


def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    if not API_KEY:
        return "Error: GOOGLE_API_KEY is not configured."

    prompt = f'''
You are a professional fitness trainer assistant.

Here is the original 7-day workout plan:

--- ORIGINAL PLAN ---
{original_plan}
--- END ORIGINAL PLAN ---

User feedback:
{user_feedback}

Revise the relevant parts of the workout plan according to the feedback.
Preserve the overall 7-day structure where possible. Return the complete revised
plan, including warm-up, main workout, and cooldown/recovery guidance.

Do not provide medical diagnosis or treatment.
'''

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as exc:
        return f"Error updating plan: {exc}"
