from mongoengine import Document, StringField

class Personality(Document):
    name = StringField(max_length=255, required=True)
    description = StringField()
    
    meta = {
        'indexes': [
            'name'
        ]
    }
