from fastapi import APIRouter, HTTPException
from services.admin import create_admin, login, generate_verification_code, send_verification_code_email, create_access_token, verify_code
from schemas.admin import AdminCreateRequest, AdminLogin, VerificationCodeRequest, VerificationCodeResponse
from models.admin import Admin

# Your helper functions (create_admin, create_access_token, verify_password, etc.)
# should be defined here or imported from the relevant modules.

auth_router = APIRouter(
    prefix="/auth-admin",
    tags=["Auth Administrator"],
    responses={404: {"description": "Not found"}},

)

@auth_router.post("/register", summary="Register a new admin", description="Create a new admin account and return an access token.")
def register(admin_data: AdminCreateRequest):
    admin = create_admin(**admin_data.dict())
    access_token = create_access_token({"admin_id": str(admin.id), "admin_email": str(admin.email)})
    return {"admin": admin, "access_token": access_token}

@auth_router.post("/login", summary="Login a admin", description="Authenticate a admin and return an access token.")
def login_admin(login_data: AdminLogin):
    admin_data = login(login_data.email, login_data.password)
    if not admin_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return admin_data

@auth_router.post("/verification/generate", summary="Generate verification code", description="Generate and send a verification code to the admin's email.")
def generate_verification(info: VerificationCodeRequest):
    admin = Admin.objects(email=info.email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="admin not found")
    code = generate_verification_code(admin)
    send_verification_code_email(admin.email, code)
    return {"message": "Verification code generated and sent"}

@auth_router.post("/verification/verify", summary="Verify admin", description="Verify the admin using the verification code.")
def verify_verification(verification_data: VerificationCodeResponse):
    admin = Admin.objects(email=verification_data.email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="admin not found")
    if not verify_code(admin, verification_data.code):
        raise HTTPException(status_code=400, detail="Invalid verification code")
    return {"message": "admin verified successfully"}