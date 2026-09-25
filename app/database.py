from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, unique=True, index=True, nullable=False)
#     name = Column(String(120), nullable=False)
#     age = Column(Integer, nullable=False)
#     weight = Column(Float, nullable=False)
#     goal = Column(String(120), nullable=False)
#     intensity = Column(String(20), nullable=False)

#     plans = relationship(
#         "WorkoutPlan",
#         back_populates="user",
#         cascade="all, delete-orphan",
#     )

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "workout_plans"

    id:Mapped[int] = mapped_column(primary_key= True, index= True)
    user_id: Mapped[int] = mapped_column(unique= True, index=True, nullable=False)
    name:Mapped[str] = mapped_column(String(120), nullable=False)
    age:Mapped[int] = mapped_column(nullable=False)
    weight:Mapped[float] = mapped_column(nullable=False)
    goal:Mapped[str] = mapped_column(String(120), nullable=False)
    intensity:Mapped[str] = mapped_column(String(20), nullable=False)

# class WorkoutPlan(Base):
#     __tablename__ = "workout_plans"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
#     original_plan = Column(Text, nullable=False)
#     updated_plan = Column(Text, nullable=True)

#     user = relationship("User", back_populates="plans")

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
        index=True
    )
    original_plan:Mapped[str] = mapped_column(Text, nullable=False)
    updated_plan: Mapped[str | None] = mapped_column(Text, nullable=False)



Base.metadata.create_all(bind=engine)


def save_user(user_id: int, name: str, age: int, weight: float, goal: str, intensity: str):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.user_id == user_id).first()

        if existing:
            existing.name = name
            existing.age = age
            existing.weight = weight
            existing.goal = goal
            existing.intensity = intensity
            db.commit()
            db.refresh(existing)
            return existing

        user = User(
            user_id=user_id,
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def save_plan(user_id: int, plan: str):
    db = SessionLocal()
    try:
        workout = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()

        if workout:
            workout.original_plan = plan
            workout.updated_plan = None
        else:
            workout = WorkoutPlan(
                user_id=user_id,
                original_plan=plan,
            )
            db.add(workout)

        db.commit()
        db.refresh(workout)
        return workout
    finally:
        db.close()


def update_plan(user_id: int, updated_text: str):
    db = SessionLocal()
    try:
        workout = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if not workout:
            return None

        workout.updated_plan = updated_text
        db.commit()
        db.refresh(workout)
        return workout
    finally:
        db.close()


def get_original_plan(user_id: int) -> str | None:
    db = SessionLocal()
    try:
        workout = (
            db.query(WorkoutPlan)
            .filter(WorkoutPlan.user_id == user_id)
            .first()
        )
        return workout.original_plan if workout else None
    finally:
        db.close()


def get_user(user_id: int):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.user_id == user_id).first()
    finally:
        db.close()


def get_all_users():
    db = SessionLocal()
    try:
        return db.query(User).order_by(User.id.desc()).all()
    finally:
        db.close()


def get_all_plans():
    db = SessionLocal()
    try:
        return db.query(WorkoutPlan).all()
    finally:
        db.close()
