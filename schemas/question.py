from pydantic import BaseModel, Field

class Question(BaseModel):
    identifiant : str
    content: str
    
class QuestionResponse(Question):
    id: str = Field(..., alias='id', example="60d5f446f1b8e6c7b4efddf3")

class QuestionCreate(Question):
    pass

class QuestionUpdate(Question):
    pass