from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from .base import PyObjectId
from bson import ObjectId

class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    phone: str

class UserCreateRequest(UserBase):
    password: str

class UserUpdateRequest(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: str = Field(..., alias='id', example="60d5f446f1b8e6c7b4efddf3")
    is_verified: bool
    is_admin: str

    class Config:
        from_attributes=True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        
class UserLogin(BaseModel):
    email: str
    password : str
    
class VerificationCodeRequest(BaseModel):
    email : str
    
class VerificationCodeRequest(BaseModel):
    email : str
    
class VerificationCodeResponse(BaseModel):
    email : str
    code: str