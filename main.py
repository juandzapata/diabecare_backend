from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
from routers import user, account, recomendacion, planes_personalizados
import os

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.title = "DiabeCare API"
CLIENT = os.getenv("CLIENT_URL")
origins = ["https://localhost","http://localhost:8100"]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

# Routers
app.include_router(user.router, tags=["Usuarios"], prefix="/usuarios")
app.include_router(account.router, tags=["Account"], prefix="/account")
app.include_router(recomendacion.router, tags=["Recomendaciones"], prefix="/recomendaciones")
app.include_router(planes_personalizados.router, tags=["Planes Personalizados"], prefix="/planes_personalizados")

@app.get("/")
async def root():
    return {"message": "Bienvenido al servidor de DiabeCare"}

