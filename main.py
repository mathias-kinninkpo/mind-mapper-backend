from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from database.base import init_db
from routes.auth import auth_router
from routes.user import user_router




load_dotenv()

app = FastAPI(
    title="Mind Mapper App",
    description="Une api pour la gestion d'utilisateurs pour un cabinet Psy",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "url": "http://your-website.com/contact",
        "email": "your-email@domain.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)


# Middleware pour autoriser les requêtes CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [auth_router, user_router]
for router in routers:
    app.include_router(router)



app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    init_db()
    print("Connexion à MongoDB établie")
    




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="192.168.1.88", port=8000)

