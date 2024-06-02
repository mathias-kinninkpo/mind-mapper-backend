from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

class AdminBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    phone: str

class AdminCreateRequest(AdminBase):
    password: str

class AdminUpdateRequest(AdminBase):
    password: Optional[str] = None

class AdminResponse(AdminBase):
    id: str = Field(..., alias='id', example="60d5f446f1b8e6c7b4efddf3")
    is_verified: bool
    is_admin: str

    class Config:
        from_attributes=True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        
class AdminLogin(BaseModel):
    email: str
    password : str
    
class VerificationCodeRequest(BaseModel):
    email : str
    
class VerificationCodeRequest(BaseModel):
    email : str
    
class VerificationCodeResponse(BaseModel):
    email : str
    code: str