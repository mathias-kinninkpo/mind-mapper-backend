from fastapi import APIRouter, HTTPException
from typing import List
from services.admin import create_admin, get_admin, get_admins, update_admin, delete_admin
from schemas.admin import AdminResponse, AdminCreateRequest, AdminUpdateRequest

# Your helper functions (create_admin, get_admin, get_admins, update_admin, delete_admin)
# should be defined here or imported from the relevant modules.

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}}
)

@admin_router.post("/", response_model=AdminResponse, summary="Create a new admin", description="Create a new admin account and return the admin details.")
def create_new_admin(admin_data: AdminCreateRequest):
    admin = create_admin(**admin_data.dict())
    return admin

@admin_router.get("/{admin_id}", response_model=AdminResponse, summary="Get admin details", description="Retrieve details of a admin by their ID.")
def read_admin(admin_id: str):
    admin = get_admin(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="admin not found")
    return admin

@admin_router.get("/", response_model=List[AdminResponse], summary="Get list of admins", description="Retrieve a list of admins with pagination.")
def read_admins():
    admins = get_admins()
    return admins

@admin_router.put("/{admin_id}", response_model=AdminResponse, summary="Update admin details", description="Update details of a admin by their ID.")
def update_admin_data(admin_id: str, admin_data: AdminUpdateRequest):
    admin = update_admin(admin_id, admin_data)
    if not admin:
        raise HTTPException(status_code=404, detail="admin not found")
    return admin

@admin_router.delete("/{admin_id}", response_model=AdminResponse, summary="Delete a admin", description="Delete a admin by their ID and return the deleted admin details.")
def delete_admin_data(admin_id: str):
    admin = delete_admin(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="admin not found")
    return admin