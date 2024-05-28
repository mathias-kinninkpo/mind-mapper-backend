from fastapi import APIRouter, HTTPException
from services.user import create_user, login, generate_verification_code, send_verification_code_email, create_access_token, verify_code
from schemas.user import UserCreateRequest, UserLogin, VerificationCodeRequest, VerificationCodeResponse
from models.user import User

# Your helper functions (create_user, create_access_token, verify_password, etc.)
# should be defined here or imported from the relevant modules.

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},

)

@auth_router.post("/register", summary="Register a new user", description="Create a new user account and return an access token.")
def register(user_data: UserCreateRequest):
    user = create_user(**user_data.dict())
    access_token = create_access_token({"user_id": str(user.id), "user_email": str(user.email)})
    return {"user": user, "access_token": access_token}

@auth_router.post("/login", summary="Login a user", description="Authenticate a user and return an access token.")
def login_user(login_data: UserLogin):
    user_data = login(login_data.email, login_data.password)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user_data

@auth_router.post("/verification/generate", summary="Generate verification code", description="Generate and send a verification code to the user's email.")
def generate_verification(info: VerificationCodeRequest):
    user = User.objects(email=info.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    code = generate_verification_code(user)
    send_verification_code_email(user.email, code)
    return {"message": "Verification code generated and sent"}

@auth_router.post("/verification/verify", summary="Verify user", description="Verify the user using the verification code.")
def verify_verification(verification_data: VerificationCodeResponse):
    user = User.objects(email=verification_data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_code(user, verification_data.code):
        raise HTTPException(status_code=400, detail="Invalid verification code")
    return {"message": "User verified successfully"}