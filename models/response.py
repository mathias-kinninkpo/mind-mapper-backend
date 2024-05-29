# models/response.py

from mongoengine import Document, StringField, DateTimeField, DictField, ReferenceField
from datetime import datetime
from .user import User

class Response(Document):
    user_id = ReferenceField(User)
    id_link = StringField(required=True)  # Updated to StringField for UUID
    status = StringField(max_length=255, required=True)
    id_personality = StringField()
    statistique = DictField(default=None)  # Changed to DictField
    date = DateTimeField(default=datetime.utcnow, required=True)
    content = DictField(default=None)  # Changed to DictField

    meta = {
        'indexes': [
            'user_id',
            'id_link',
            'date'
        ]
    }
