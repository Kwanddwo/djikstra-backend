from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.db import Base
import uuid
from datetime import datetime, timezone

# Association table for many-to-many relationship between User and Skill, with learning level
user_skills = Table(
    "user_skills",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("skill_id", UUID(as_uuid=True), ForeignKey("skills.id"), primary_key=True),
    Column("learning_level", Float, default=0.0),  # 0.0 to 1.0
)

# Association table for many-to-many relationship between Lesson and Skill, with gain value
lesson_skills = Table(
    "lesson_skills",
    Base.metadata,
    Column("lesson_id", UUID(as_uuid=True), ForeignKey("lessons.id"), primary_key=True),
    Column("skill_id", UUID(as_uuid=True), ForeignKey("skills.id"), primary_key=True),
    Column("gain", Float, nullable=False, default=0.1),  # 0.0 < gain <= 1.0
)

# Association table for many-to-many relationship between PracticeProblem and Skill, with gain value
problem_skills = Table(
    "problem_skills",
    Base.metadata,
    Column("problem_id", UUID(as_uuid=True), ForeignKey("practice_problems.id"), primary_key=True),
    Column("skill_id", UUID(as_uuid=True), ForeignKey("skills.id"), primary_key=True),
    Column("gain", Float, nullable=False, default=0.1),  # 0.0 < gain <= 1.0
)

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstname = Column(String, index=True, nullable=False)
    lastname = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    tokens_used = Column(Integer, default=0)
    last_reset = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    skills = relationship("Skill", secondary=user_skills, back_populates="users")

class Skill(Base):
    __tablename__ = "skills"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    users = relationship("User", secondary=user_skills, back_populates="skills")
    lessons = relationship("Lesson", secondary=lesson_skills, back_populates="skills")
    problems = relationship("PracticeProblem", secondary=problem_skills, back_populates="skills")

class Course(Base):
    __tablename__ = "courses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    units = relationship("Unit", back_populates="course")

class Unit(Base):
    __tablename__ = "units"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"))
    course = relationship("Course", back_populates="units")
    order = Column(Integer, nullable=False, default=1) # starts at 1
    lesson = relationship("Lesson", uselist=False, back_populates="unit")
    practice_problems = relationship("PracticeProblem", back_populates="unit")

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id"))
    unit = relationship("Unit", back_populates="lesson")
    skills = relationship("Skill", secondary=lesson_skills, back_populates="lessons")

class PracticeProblem(Base):
    __tablename__ = "practice_problems"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False)  # e.g., "multiple_choice" or "interactive_graph"
    question = Column(String, nullable=False)
    data = Column(String, nullable=True)  # JSON or other data for the problem
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id"))
    unit = relationship("Unit", back_populates="practice_problems")
    skills = relationship("Skill", secondary=problem_skills, back_populates="problems")

class PromptLog(Base):
    __tablename__ = "prompt_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user_prompt = Column(String, nullable=False)
    llm_response = Column(String, nullable=False)
    tokens_used = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    user = relationship("User")

class UserLessonCompletion(Base):
    __tablename__ = "user_lesson_completion"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False)
    completed_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    user = relationship("User")
    lesson = relationship("Lesson")

class UserProblemCompletion(Base):
    __tablename__ = "user_problem_completion"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("practice_problems.id"), nullable=False)
    completed_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    user = relationship("User")
    problem = relationship("PracticeProblem")

class UserCourseOrderProgress(Base):
    __tablename__ = "user_course_order_progress"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), primary_key=True)
    current_order = Column(Integer, nullable=False, default=1)  # starts at 1
    last_updated = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    user = relationship("User")
    course = relationship("Course")