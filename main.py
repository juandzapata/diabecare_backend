from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
from routers import user, account, recomendacion, planes_personalizados, paciente, notification
import firebase_admin
from firebase_admin import credentials
import os

Base.metadata.create_all(bind=engine)
app = FastAPI()
firebase_credentials = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN")
}
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)
app.title = "DiabeCare API"
CLIENT = os.getenv("CLIENT_URL")
origins = ["https://localhost","http://localhost:8100", "http://localhost:4200"]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

# Routers
app.include_router(user.router, tags=["Usuarios"], prefix="/usuarios")
app.include_router(account.router, tags=["Account"], prefix="/account")
app.include_router(recomendacion.router, tags=["Recomendaciones"], prefix="/recomendaciones")
app.include_router(planes_personalizados.router, tags=["Planes Personalizados"], prefix="/planes_personalizados")
app.include_router(paciente.router, tags=["Pacientes"], prefix="/pacientes")
app.include_router(notification.router, tags=["Notificaciones"], prefix="/notificaciones")

@app.get("/")
async def root():
    return {"message": "Bienvenido al servidor de DiabeCare"}

