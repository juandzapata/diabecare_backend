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

    def model_dump(self):
        return {
            "id": self.usuarioId,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "correo": self.correo,
            "contrasena": self.contraseña,
            "sexo": self.sexo,
            "ciudad": self.ciudad,
            "foto": self.foto,
            "fecha_nacimiento": self.fechaNacimiento
        }


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