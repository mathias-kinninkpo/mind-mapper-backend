from pydantic import BaseModel

class PersonalityBase(BaseModel):
    name: str
    description: str

class PersonalityCreate(PersonalityBase):
    pass

class PersonalityUpdate(PersonalityBase):
    pass

class PersonalityOut(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
        from_attributes=True
