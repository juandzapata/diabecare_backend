from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
from routers import patient, personalized_planes, recomendation, user, account, file
import os

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.title = "DiabeCare API"
CLIENT = os.getenv("CLIENT_URL")
origins = ["https://localhost","http://localhost:8100"]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

# Routers
app.include_router(user.router, tags=["Usuarios"], prefix="/users")
app.include_router(account.router, tags=["Account"], prefix="/account")
app.include_router(recomendation.router, tags=["Recomendations"], prefix="/recomendations")
app.include_router(personalized_planes.router, tags=["Personalized Planes"], prefix="/personalized_planes")
app.include_router(patient.router, tags=["Patients"], prefix="/patients")
app.include_router(file.router, tags=["Files"], prefix="/files")

@app.get("/")
async def root():
    return {"message": "Bienvenido al servidor de DiabeCare"}

