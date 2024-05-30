# schemas/response.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Optional, Union
from .user import UserResponse

class ResponseBase(BaseModel):
    user_id: UserResponse
    id_link: Optional[str] = None
    status: Optional[str] = None
    id_personality: Optional[str] = None
    statistique: Optional[Dict[str, Union[str, None]]] = None
    content: Optional[Dict[str, Union[bool, None]]] = None
    date: datetime

class ResponseCreate(BaseModel):
    user_id: str 
    
class ResponseUpdate(ResponseBase):
    pass

class ResponseOut(ResponseBase):
    id: str = Field(..., alias='id', example="60d5f446f1b8e6c7b4efddf3")

    class Config:
        orm_mode = True
        from_attributes = True


