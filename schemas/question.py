from pydantic import BaseModel

class Question(BaseModel):
    id: int
    content: str
