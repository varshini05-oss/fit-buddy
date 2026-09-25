from pydantic import BaseModel, Field


class UserInput(BaseModel):
    user_id: int = Field(gt=0)
    username: str = Field(min_length=1, max_length=120)
    age: int = Field(gt=0, le=120)
    weight: float = Field(gt=0, le=500)
    goal: str = Field(min_length=1, max_length=120)
    intensity: str = Field(pattern="^(low|medium|high)$")


class FeedbackRequest(BaseModel):
    user_id: int = Field(gt=0)
    feedback: str = Field(min_length=1, max_length=2000)


class WorkoutRequest(BaseModel):
    goal: str = Field(min_length=1, max_length=120)
    intensity: str = Field(pattern="^(low|medium|high)$")
