# schemas/response.py

from pydantic import BaseModel, Field
from typing import Dict
from .user import UserResponse

class ResponseBase(BaseModel):
    user_id: UserResponse
    id_link: str
    status: str
    id_personality: int
    statistique: Dict[str, bool]
    content: Dict[str, bool]
    date: str

class ResponseCreate(BaseModel):
    user_id : UserResponse
    

class ResponseUpdate(ResponseBase):
    pass

class ResponseOut(ResponseBase):
    id: str = Field(..., alias='id', example="60d5f446f1b8e6c7b4efddf3")
    
    class Config:
        orm_mode = True
        from_attributes = True
