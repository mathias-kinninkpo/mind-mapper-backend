from fastapi import APIRouter, HTTPException
from typing import List
from services.user import create_user, get_user, get_users, update_user, delete_user
from schemas.user import UserResponse, UserCreateRequest, UserUpdateRequest

# Your helper functions (create_user, get_user, get_users, update_user, delete_user)
# should be defined here or imported from the relevant modules.

user_router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}}
)

@user_router.post("/", response_model=UserResponse, summary="Create a new user", description="Create a new user account and return the user details.")
def create_new_user(user_data: UserCreateRequest):
    user = create_user(**user_data.dict())
    return user

@user_router.get("/{user_id}", response_model=UserResponse, summary="Get user details", description="Retrieve details of a user by their ID.")
def read_user(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/", response_model=List[UserResponse], summary="Get list of users", description="Retrieve a list of users with pagination.")
def read_users(skip: int = 0, limit: int = 10):
    users = get_users(skip=skip, limit=limit)
    return users

@user_router.put("/{user_id}", response_model=UserResponse, summary="Update user details", description="Update details of a user by their ID.")
def update_user_data(user_id: str, user_data: UserUpdateRequest):
    user = update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.delete("/{user_id}", response_model=UserResponse, summary="Delete a user", description="Delete a user by their ID and return the deleted user details.")
def delete_user_data(user_id: str):
    user = delete_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user