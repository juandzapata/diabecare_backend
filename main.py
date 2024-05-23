from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
from routers import user, account, paciente
import os

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.title = "DiabeCare API"
CLIENT = os.getenv("CLIENT_URL")
origins = ["https://localhost","http://localhost:8100"]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

app.include_router(user.router, tags=["Usuarios"], prefix="/usuarios")
app.include_router(account.router, tags=["Account"], prefix="/account")
app.include_router(paciente.router, tags=["Pacientes"], prefix="/pacientes")



@app.get("/")
async def root():
    return {"message": "Bienvenido al servidor de DiabeCare"}

