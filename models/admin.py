from mongoengine import Document, StringField, EmailField, EnumField, IntField, BooleanField
import enum


class RoleEnum(enum.Enum):
    admin = "admin"
    manager = "manager"
    # Ajoutez d'autres rôles au besoin


class Admin(Document):
    firstname = StringField(max_length=255, required=True)
    lastname = StringField(max_length=255, required=True)
    email = EmailField(unique=True, required=True)
    phone = StringField(max_length=20, required=True)
    code = StringField(max_length=10, required=False)
    is_verified = BooleanField(default=False)
    password = StringField(max_length=255, required=True)
    
    meta = {
        'indexes': [
            'email',
            'phone'
        ]
    }

