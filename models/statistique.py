import mongoengine as me
from mongoengine import Document, IntField, DateTimeField, StringField
from datetime import datetime

class Statistique(Document):
    id = IntField(primary_key=True, required=True)
    id_user = IntField(required=True)
    id_personality = IntField(required=True)
    id_response = IntField(required=True)
    date = DateTimeField(default=datetime.utcnow, required=True)
    
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
            'id_user',
            'id_personality',
            'id_response',
            'date'
        ]
    }
