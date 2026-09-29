# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 web application that uses Google Gemini models to generate personalized 7-day workout plans and nutrition/recovery tips.

## Features

- Collects username, user ID, age, weight, fitness goal, and workout intensity.
- Generates a structured 7-day workout plan with Gemini 1.5 Pro.
- Generates a concise nutrition/recovery tip with Gemini Flash.
- Stores users and plans in SQLite using SQLAlchemy.
- Accepts feedback and regenerates the workout plan.
- Keeps original and updated plans.
- Provides an admin view of users and plans.
- Includes FastAPI interactive API documentation.

## Project Structure

```text
fitbuddy/
├── requirements.txt
├── .env.example
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── database.py
│   ├── schemas.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   ├── updated_plan.py
│   └── nutrition.py
├── templates/
│   ├── index.html
│   ├── result.html
│   └── all_users.html
└── static/
    └── images/
```

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```powershell
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env` and add your Gemini API key:

```text
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## Main Routes

- `GET /` – Home page
- `POST /generate-workout` – Generate and store a workout plan
- `POST /submit-feedback` – Update a plan using feedback
- `GET /view-all-users` – Admin view
- `POST /api/generate-workout` – JSON workout-generation endpoint
- `GET /api/nutrition-tip` – JSON nutrition-tip endpoint
- `POST /api/generate-plan` – JSON endpoint that saves user + plan

## Notes

The project follows the architecture and feature descriptions in the supplied FitBuddy document. The source document contains both `app/main.py` in its project structure and a later `main:app` example; this implementation uses the documented `app/main.py` structure consistently, so the startup command is `uvicorn app.main:app --reload`.

The application is an educational project and generated fitness/nutrition content should not be treated as medical advice.
