from pydantic import BaseModel, EmailStr
import uuid

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

class ChatRequest(BaseModel):
    user_input: str