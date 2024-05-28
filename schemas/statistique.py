from pydantic import BaseModel
from typing import List

class StatistiqueBase(BaseModel):
    id_user: int
    id_personality: int
    id_response: int
    date: str  # ou DateTime, selon la façon dont vous voulez représenter la date
    A: str
    B: str
    C: str
    D: str
    E: str
    F: str
    G: str
    H: str
    I: str

class StatistiqueCreate(StatistiqueBase):
    pass

class StatistiqueUpdate(StatistiqueBase):
    pass

class StatistiqueOut(BaseModel):
    id: int
    id_user: int
    id_personality: int
    id_response: int
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

    class Config:
        orm_mode = True
