from datetime import date
from typing import Optional
from pydantic import BaseModel

class GetUser(BaseModel):
    id: int
    nombre: str
    apellidos: str
    correo: str
    contrasena: str
    sexo: str
    ciudad: str
    foto: str
    fecha_nacimiento: date
    
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