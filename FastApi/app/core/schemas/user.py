from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class UserCreateSchema(BaseModel):
    email: EmailStr = Field(max_length=255, description="Унікальна електронна пошта користувача.")
    password: str = Field(min_length=6, max_length=255, description="Пароль користувача.")
    role: str = Field(default="Student", max_length=50, description="Роль користувача (Student, Instructor, Admin).")

class UserResponseSchema(BaseModel):
    id: int = Field(description="Унікальний ідентифікатор користувача.")
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class UserPartialUpdateSchema(BaseModel):
    email: Optional[EmailStr] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=6, max_length=255)
    role: Optional[str] = Field(None, max_length=50)