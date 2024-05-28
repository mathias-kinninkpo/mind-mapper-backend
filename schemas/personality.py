from pydantic import BaseModel, Field

class PersonalityBase(BaseModel):
    name: str
    description: str

class PersonalityCreate(PersonalityBase):
    pass

class PersonalityUpdate(PersonalityBase):
    pass

class PersonalityResponse(PersonalityBase):
    id: str = Field(..., alias='id', example="60d5f446f1b8e6c7b4efddf3")

    # class Config:
    #     orm_mode = True
    #     from_attributes=True
