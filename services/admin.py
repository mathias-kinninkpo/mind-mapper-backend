from jwt import encode
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
from models.admin import Admin
from schemas.admin import AdminResponse
import random
import string
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_DAYS = os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=int(ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_admin(firstname: str, lastname: str, email: str, phone: str, password: str) -> Admin:
    hashed_password = hash_password(password)
    admin = Admin(
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone=phone,
        password=hashed_password
    )
    print(admin)
    admin.save()
    admin_dict = admin.to_mongo().to_dict()
    admin_dict['id'] = str(admin_dict['_id'])  # Ensure the _id field is a string
    admin_response = AdminResponse.parse_obj(admin_dict)
    return admin_response

def login(email: str, password: str) -> Optional[dict]:
    admin = Admin.objects(email=email).first()
    if admin and verify_password(password, admin.password):
        access_token = create_access_token({"admin_id": str(admin.id), "admin_email": admin.email})
        admin_dict = admin.to_mongo().to_dict()
        admin_dict['id'] = str(admin_dict['_id'])  # Ensure the _id field is a string
        admin_response = AdminResponse.parse_obj(admin_dict)
        return {"admin": admin_response, "access_token": access_token}
    return None


def generate_verification_code(admin: Admin) -> str:
    # Génération d'un code de vérification aléatoire de 6 chiffres
    code = ''.join(random.choices(string.digits, k=6))
    # Mise à jour du champ verification_code dans la base de données
    admin.update(code=code)
    return code

def send_verification_code_email(email: str, code: str) -> None:
    # Implémentez ici la logique pour envoyer le code de vérification par e-mail
    # Cette fonction pourrait utiliser un service d'e-mail comme SendGrid, SMTP, etc.
    # Par exemple, avec FastAPI, vous pouvez envoyer un e-mail en utilisant un package Python comme `smtplib`
    # Voici un exemple simple avec smtplib :
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["Subject"] = "Votre de verification pour Mind Mapper App"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Votre code de verification est: {code}"
    html = f"""\
    <html>
      <body>
        <p>Vous avez demandé à changer votre mot de passe <br/>Votre code de verification est : <strong>{code}</strong></p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)
    
    try:
        
        with smtplib.SMTP(os.getenv("EMAIL_SERVER"), 587) as server:
            server.starttls()
            server.login(sender_email, os.getenv("EMAIL_PASSWORD"))
            senders = server.sendmail(sender_email, receiver_email, message.as_string())
            
            return senders
    except:
        return None


def verify_code(admin: Admin, code: str) -> bool:
    if admin.code == code:
        admin.update(is_verified=True, verification_code=None)
        return True
    return False


def get_admin(admin_id: str) -> Optional[Admin]:
    admin =  Admin.objects(id=admin_id).first()
    admin_dict = admin.to_mongo().to_dict()
    admin_dict['id'] = str(admin_dict['_id'])  # Ensure the _id field is a string
    admin_response = AdminResponse.parse_obj(admin_dict)
    return admin_response

def get_admins() -> List[Admin]:
    admins = Admin.objects.all()
    admins_response = list()
    for admin in admins:
        admin_dict = admin.to_mongo().to_dict()
        admin_dict['id'] = str(admin_dict['_id'])  
        admins_response.append(AdminResponse.parse_obj(admin_dict))
    
    return admins_response
    

def update_admin(admin_id: str, admin_data: dict) -> Optional[Admin]:
    admin = Admin.objects(id=admin_id).first()
    if not admin:
        return None
    update_data = admin_data.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    admin.update(**update_data)
    admin.reload()
    admin_dict = admin.to_mongo().to_dict()
    admin_dict['id'] = str(admin_dict['_id'])  
    return AdminResponse.parse_obj(admin_dict)

def delete_admin(admin_id: str) -> Optional[Admin]:
    admin = Admin.objects(id=admin_id).first()
    if admin:
        admin.delete()
        admin_dict = admin.to_mongo().to_dict()
        admin_dict['id'] = str(admin_dict['_id'])  
        return AdminResponse.parse_obj(admin_dict)
    return None

