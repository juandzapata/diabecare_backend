from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data.database.db import Base, engine
from routers import user, account, recomendation, personalized_planes, patient, notification, file, health_professional
import firebase_admin
import uvicorn
from firebase_admin import credentials
import os

# Inicializa la base de datos
Base.metadata.create_all(bind=engine)

# Inicializa la aplicación FastAPI
app = FastAPI()

# Configuración de Firebase
cred = credentials.Certificate({
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),  # Asegúrate de que las nuevas líneas sean correctas
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN")
})
firebase_admin.initialize_app(cred)

# Configuración de CORS
origins = [
    os.getenv("ORIGIN_DEVICE"),
    os.getenv("ORIGIN_FRONTEND_DEFAULT"),
    os.getenv("ORIGIN_FRONTEND_SECOND")
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Routers
app.include_router(user.router, tags=["Usuarios"], prefix="/users")
app.include_router(account.router, tags=["Cuentas"], prefix="/accounts")
app.include_router(patient.router, tags=["Pacientes"], prefix="/pacientes")
app.include_router(notification.router, tags=["Notifications"], prefix="/notifications")
app.include_router(recomendation.router, tags=["Recomendations"], prefix="/recomendations")
app.include_router(personalized_planes.router, tags=["Personalized Planes"], prefix="/personalized_planes")
app.include_router(file.router, tags=["Files"], prefix="/files")
app.include_router(health_professional.router, tags=["Health Professional"], prefix="/health_professional")

# Endpoint raíz
@app.get("/")
async def root():
    return {"message": "Bienvenido al servidor de DiabeCare"}

# Configuración del puerto
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
