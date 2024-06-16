import token
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data.database.db import Base, engine
from routers import user, account, recomendation, personalized_planes, patient, notification
import firebase_admin
from firebase_admin import credentials
from routers import patient, personalized_planes, recomendation, user, file
from routers import user, account, health_professional
import os

Base.metadata.create_all(bind=engine)
app = FastAPI()
firebase_credentials = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
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
origins = [os.getenv("ORIGIN_DEVICE"),os.getenv("ORIGIN_FRONTEND_DEFAULT")]
print("ORIGINS",origins)
origins = ["*"]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

# Routers
app.include_router(user.router, tags=["Usuarios"], prefix="/users")
app.include_router(account.router, tags=["Cuentas"], prefix="/accounts")
app.include_router(patient.router, tags=["Pacientes"], prefix="/pacientes")
app.include_router(notification.router, tags=["Notifications"], prefix="/notifications")
app.include_router(recomendation.router, tags=["Recomendations"], prefix="/recomendations")
app.include_router(personalized_planes.router, tags=["Personalized Planes"], prefix="/personalized_planes")
app.include_router(file.router, tags=["Files"], prefix="/files")
app.include_router(health_professional.router, tags=["Health Professional"], prefix="/health_professional")


@app.get("/")
async def root():
    return {"message": "Bienvenido al servidor de DiabeCare"}

port = int(os.environ.get("PORT", 8000))