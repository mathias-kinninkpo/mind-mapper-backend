# schemas/response.py

from pydantic import BaseModel, Field
from typing import Dict

class ResponseBase(BaseModel):
    user_id: int
    id_link: str
    status: str
    id_personality: int
    id_statistique: Dict[str, str]
    content: Dict[str, str]
    date: str
    A: str
    B: str
    C: str
    D: str
    E: str
    F: str
    G: str
    H: str
    I: str

class ResponseCreate(ResponseBase):
    pass

class ResponseUpdate(ResponseBase):
    pass

class ResponseOut(ResponseBase):
    id: str = Field(..., alias='id', example="60d5f446f1b8e6c7b4efddf3")
    
    class Config:
        orm_mode = True
        from_attributes = True
