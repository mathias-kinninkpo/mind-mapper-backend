# models/response.py

from mongoengine import Document, IntField, StringField, DateTimeField, DictField
from datetime import datetime

class Response(Document):
    id = IntField(primary_key=True, required=True)
    user_id = IntField(required=True)
    id_link = StringField(required=True)  # Updated to StringField for UUID
    status = StringField(max_length=255, required=True)
    id_personality = IntField(required=True)
    id_statistique = DictField()  # Changed to DictField
    date = DateTimeField(default=datetime.utcnow, required=True)
    content = DictField(required=True)  # Changed to DictField
    A = StringField(max_length=255)
    B = StringField(max_length=255)
    C = StringField(max_length=255)
    D = StringField(max_length=255)
    E = StringField(max_length=255)
    F = StringField(max_length=255)
    G = StringField(max_length=255)
    H = StringField(max_length=255)
    I = StringField(max_length=255)

    meta = {
        'indexes': [
            'user_id',
            'id_link',
            'id_personality',
            'date'
        ]
    }
