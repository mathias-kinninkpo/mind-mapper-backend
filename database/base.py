from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from mongoengine import connect 

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer l'URI de connexion MongoDB à partir des variables d'environnement
MONGO_URI = os.getenv("MONGO_URI")

# Fonction pour se connecter à MongoDB et récupérer la base de données
async def connect_to_mongodb(database_name: str = "Cluster0"):
    client = AsyncIOMotorClient(MONGO_URI)
    return client[database_name]

def init_db():
    connect(host=MONGO_URI)