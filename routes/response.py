from fastapi import APIRouter, HTTPException
from typing import List, Dict

from services.response import (
    create_response,
    get_response,
    get_all_responses,
    update_response,
    delete_response,
    update_response_personality
)
from schemas.response import ResponseCreate, ResponseOut

response_router = APIRouter(
    prefix="/responses",
    tags=["Response"],
    responses={404: {"description": "Not found"}}
)

@response_router.post("/", response_model=ResponseOut, summary="Create a new response", description="Create a new response in the database.")
def create_new_response(response_data: ResponseCreate):
    try:
        return create_response(response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@response_router.get("/{id_link}", response_model=ResponseOut, summary="Get a response by ID", description="Retrieve a response by its ID.")
def read_response(id_link: str):
    response = get_response(id_link)
    if not response:
        raise HTTPException(status_code=404, detail="Response not found")
    return response

@response_router.get("/", response_model=List[ResponseOut], summary="Get all responses", description="Retrieve all responses with optional pagination.")
def read_responses():
    try:
        return get_all_responses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@response_router.put("/{id_link}", response_model=ResponseOut, summary="Update a response", description="Update a response by its ID.")
def update_existing_response(id_link: str, response_data: Dict):
    try:
        response = update_response(id_link, response_data)
        if not response:
            raise HTTPException(status_code=404, detail="Response not found")
        return response
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@response_router.delete("/{response_id}", response_model=ResponseOut, summary="Delete a response", description="Delete a response by its ID.")
def delete_existing_response(response_id: str):
    try:
        response = delete_response(response_id)
        if not response:
            raise HTTPException(status_code=404, detail="Response not found")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@response_router.patch("/{response_id}/personality", response_model=ResponseOut, summary="Update a response personality", description="Update the personality ID of a response.")
def update_response_personality(response_id: str, id_personality: int):
    try:
        response = update_response_personality(response_id, id_personality)
        if not response:
            raise HTTPException(status_code=404, detail="Response not found")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
