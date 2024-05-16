from fastapi import FastAPI
from database.db import Base, engine
from routers import usuario

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.title = "DiabeCare API"

app.include_router(usuario.router, tags=["Usuarios"], prefix="/usuarios")


@app.get("/")
async def root():
    return {"message": "Bienvenido al servidor de DiabeCare"}