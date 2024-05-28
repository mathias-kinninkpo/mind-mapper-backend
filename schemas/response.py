from pydantic import BaseModel
from typing import List

class ResponseBase(BaseModel):
    user_id: int
    id_link: int
    status: str
    id_personality: int
    id_statistique: int
    date: str
    
    # # Génération dynamique des champs A1, A2, ..., I10
    # for letter in 'ABCDEFGHI':
    #     for number in range(1, 11):
    #         locals()[f'{letter}{number}'] = str  # Tous les champs seront de type str

class ResponseCreate(ResponseBase):
    pass

class ResponseUpdate(ResponseBase):
    pass

class ResponseOut(BaseModel):
    id: int
    user_id: int
    id_link: int
    status: str
    id_personality: int
    id_statistique: int
    date: str
    content: dict
    A : str
    B : str
    C : str
    D : str
    E : str
    F : str
    G : str
    H : str
    I : str

    # # Génération dynamique des champs A1, A2, ..., I10
    # for letter in 'ABCDEFGHI':
    #     for number in range(1, 11):
    #         locals()[f'{letter}{number}'] = str  # Tous les champs seront de type str

    class Config:
        orm_mode = True
        from_attributes=True
