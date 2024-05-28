import mongoengine as me
from mongoengine import Document, StringField, IntField

# Connexion à MongoDB
me.connect('your_database_name', host='your_mongodb_uri')


class Question(Document):
    content = StringField(required=True)
    

