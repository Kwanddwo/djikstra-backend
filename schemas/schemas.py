from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
import uuid

# --- User Schemas ---
class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: uuid.UUID
    firstname: str
    lastname: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

# --- Chat Request Schema ---
class ChatRequest(BaseModel):
    user_input: str
    additional_context: Optional[str] = None
    class Config:
        schema_extra = {
            "example": {
                "user_input": "What is an edge?",
                "additional_context": "User is currently on the 'What is a graph?' Lesson in the 'Introduction to Graphs' unit."
            }
        }


# --- Lesson Schemas ---
class LessonOut(BaseModel):
    id: UUID
    title: str
    content: str
    unit_id: UUID
    class Config:
        orm_mode = True

# --- Practice Problem Schemas ---
class PracticeProblemOut(BaseModel):
    id: UUID
    type: str
    question: str
    data: Optional[str]
    unit_id: UUID
    class Config:
        orm_mode = True

class PracticeProblemCreate(BaseModel):
    type: str
    question: str
    data: Optional[str] = None
    unit_id: UUID

# --- Course & Unit Schemas ---
class UnitCreate(BaseModel):
    name: str
    course_id: UUID
    order: int = Field(ge=1)  # Order starts at 1

class UnitOut(BaseModel):
    id: UUID
    name: str
    course_id: UUID
    order: int
    lesson: LessonOut
    practice_problems: List[PracticeProblemOut] = []
    class Config:
        orm_mode = True

class UnitUpdate(BaseModel):
    name: Optional[str] = None
    order: Optional[int] = Field(None, ge=1)  # Order starts at 1
    course_id: Optional[UUID] = None

class CourseCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CourseOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    units: List[UnitOut] = []
    class Config:
        orm_mode = True
        
class LessonCreate(BaseModel):
    title: str
    content: str
    unit_id: UUID

# --- Skill Schemas ---
class SkillOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    class Config:
        orm_mode = True

# --- User Skill Progress ---
class UserSkillOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    learning_level: float
    class Config:
        orm_mode = True

# --- User Unit Progress ---
class UserUnitProgressOut(BaseModel):
    user_id: UUID
    unit_id: UUID
    completion_percentage: float
    last_updated: datetime
    class Config:
        orm_mode = True

class UserUnitProgressUpdate(BaseModel):
    completion_percentage: float
    last_updated: Optional[datetime] = None

class UserLessonCompletion(BaseModel):
    id: UUID
    user_id: UUID
    lesson_id: UUID
    completed_at: datetime
    class Config:
        orm_mode = True

class UserProblemCompletion(BaseModel):
    id: UUID
    user_id: UUID
    problem_id: UUID
    completed_at: datetime
    class Config:
        orm_mode = True 

class UserCompletions(BaseModel):
    user_id: UUID
    lessons: List[UserLessonCompletion]
    practice_problems: List[UserProblemCompletion]
    class Config:
        orm_mode = True

# --- Prompt Log ---
class PromptLogOut(BaseModel):
    id: UUID
    user_id: UUID
    user_prompt: str
    llm_response: str
    timestamp: datetime
    class Config:
        orm_mode = True