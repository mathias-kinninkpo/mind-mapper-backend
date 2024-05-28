# routes/personality.py

from fastapi import APIRouter, HTTPException
from typing import List
from services.personality import (
    create_personality,
    get_personality,
    get_all_personalities,
    update_personality,
    delete_personality
)
from schemas.personality import PersonalityCreate, PersonalityUpdate, PersonalityResponse

personality_router = APIRouter(
    prefix="/personalities",
    tags=["Personality"],
    responses={404: {"description": "Not found"}}
)

@personality_router.post("/", response_model=PersonalityResponse, summary="Create a new personality", description="Create a new personality in the database.")
def create_new_personality(personality_data: PersonalityCreate):
    return create_personality(personality_data)

@personality_router.get("/{personality_id}", response_model=PersonalityResponse, summary="Get a personality by ID", description="Retrieve a personality by its ID.")
def read_personality(personality_id: str):
    personality = get_personality(personality_id)
    if not personality:
        raise HTTPException(status_code=404, detail="Personality not found")
    return personality

@personality_router.get("/", response_model=List[PersonalityResponse], summary="Get all personalities", description="Retrieve all personalities with optional pagination.")
def read_personalities():
    return get_all_personalities()

@personality_router.put("/{personality_id}", response_model=PersonalityResponse, summary="Update a personality", description="Update a personality by its ID.")
def update_existing_personality(personality_id: str, personality_data: PersonalityUpdate):
    personality = update_personality(personality_id, personality_data)
    if not personality:
        raise HTTPException(status_code=404, detail="Personality not found")
    return personality

@personality_router.delete("/{personality_id}", response_model=PersonalityResponse, summary="Delete a personality", description="Delete a personality by its ID.")
def delete_existing_personality(personality_id: str):
    personality = delete_personality(personality_id)
    if not personality:
        raise HTTPException(status_code=404, detail="Personality not found")
    return personality
