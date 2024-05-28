from jwt import encode
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
from models.user import User
from schemas.user import UserResponse
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


def create_user(firstname: str, lastname: str, email: str, phone: str, password: str) -> User:
    hashed_password = hash_password(password)
    user = User(
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone=phone,
        password=hashed_password
    )
    print(user)
    user.save()
    user_dict = user.to_mongo().to_dict()
    user_dict['id'] = str(user_dict['_id'])  # Ensure the _id field is a string
    user_response = UserResponse.parse_obj(user_dict)
    return user_response

def login(email: str, password: str) -> Optional[dict]:
    user = User.objects(email=email).first()
    if user and verify_password(password, user.password):
        access_token = create_access_token({"user_id": str(user.id), "user_email": user.email})
        user_dict = user.to_mongo().to_dict()
        user_dict['id'] = str(user_dict['_id'])  # Ensure the _id field is a string
        user_response = UserResponse.parse_obj(user_dict)
        return {"user": user_response, "access_token": access_token}
    return None


def generate_verification_code(user: User) -> str:
    # Génération d'un code de vérification aléatoire de 6 chiffres
    code = ''.join(random.choices(string.digits, k=6))
    # Mise à jour du champ verification_code dans la base de données
    user.update(code=code)
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


def verify_code(user: User, code: str) -> bool:
    if user.code == code:
        user.update(is_verified=True, verification_code=None)
        return True
    return False


def get_user(user_id: str) -> Optional[User]:
    user =  User.objects(id=user_id).first()
    user_dict = user.to_mongo().to_dict()
    user_dict['id'] = str(user_dict['_id'])  # Ensure the _id field is a string
    user_response = UserResponse.parse_obj(user_dict)
    return user_response

def get_users(skip: int = 0, limit: int = 10) -> List[User]:
    users = User.objects.skip(skip).limit(limit).all()
    users_response = list()
    for user in users:
        user_dict = user.to_mongo().to_dict()
        user_dict['id'] = str(user_dict['_id'])  
        users_response.append(UserResponse.parse_obj(user_dict))
    
    return users_response
    

def update_user(user_id: str, user_data: dict) -> Optional[User]:
    user = User.objects(id=user_id).first()
    if not user:
        return None
    update_data = user_data.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    user.update(**update_data)
    user.reload()
    user_dict = user.to_mongo().to_dict()
    user_dict['id'] = str(user_dict['_id'])  
    return UserResponse.parse_obj(user_dict)

def delete_user(user_id: str) -> Optional[User]:
    user = User.objects(id=user_id).first()
    if user:
        user.delete()
        user_dict = user.to_mongo().to_dict()
        user_dict['id'] = str(user_dict['_id'])  
        return UserResponse.parse_obj(user_dict)
    return None

