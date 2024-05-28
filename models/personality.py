from mongoengine import Document, StringField, IntField

class Personality(Document):
    id = IntField(primary_key=True, required=True)
    name = StringField(max_length=255, required=True)
    description = StringField()
    
    meta = {
        'indexes': [
            'name'
        ]
    }
