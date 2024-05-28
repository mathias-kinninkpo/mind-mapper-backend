from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from database.base import init_db
from routes.auth import auth_router
from routes.user import user_router
from routes.question import question_router
from routes.personality import personality_router
from routes.response import response_router




load_dotenv()

app = FastAPI(
    title="Mind Mapper App",
    description="Une api pour la gestion d'utilisateurs pour un cabinet Psy",
    version="1.0.0",
    contact={
        "name": "Mathias KINNINKPO",
        "url": "https://mathias-kinninkpo.netlify.app",
        "email": "mathiaskin2003@gmail.com",
    },
    license_info={
        "name": "MMA License",
        "url": "https://opensource.org/licenses/MMA",
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

routers = [auth_router, user_router, question_router, personality_router, response_router]
for router in routers:
    app.include_router(router)



app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    init_db()
    print("Connexion à MongoDB établie")
    




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

