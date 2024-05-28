import mongoengine as me
from mongoengine import Document, StringField, IntField

# Connexion à MongoDB
me.connect('your_database_name', host='your_mongodb_uri')


class Question(Document):
    identifiant = IntField(primary_key=True, required=True)
    content = StringField(required=True)
    
    meta = {
        'indexes': [
            'identifiant'
        ]
    }

question = Question(
    identifiant=1,
    content='What is the capital of France?'
)
question.save()
