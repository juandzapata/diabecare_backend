from datetime import date
from typing import Optional
from pydantic import BaseModel

class GetUser(BaseModel):
    usuarioId: int
    nombre: str
    apellidos: str
    correo: str
    contraseña: str
    sexo: str
    ciudad: str
    foto: str
    fechaNacimiento: str
    rolId: Optional[int]

class UserRead(BaseModel):
    usuarioId: int
    nombre: str
    apellidos: str
    correo: str
    contraseña: str
    sexo: str
    ciudad: str
    foto: str
    fechaNacimiento: date
    rolId: Optional[int]

    class Config:
        orm_mode = True
        from_attributes = True