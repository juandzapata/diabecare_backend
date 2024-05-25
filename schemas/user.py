from datetime import date
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
    
class UserGetLogin(BaseModel):
    usuarioId: int
    nombre: str
    apellidos: str
    correo: str
    contraseña: str
    sexo: str
    ciudad: str
    foto: str
    fechaNacimiento: str
    roles: list

    def model_dump(self):
        return {
            "usuarioId": self.usuarioId,
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "correo": self.correo,
            "contrasena": self.contraseña,
            "sexo": self.sexo,
            "ciudad": self.ciudad,
            "foto": self.foto,
            "fecha_nacimiento": self.fechaNacimiento,
            "roles": []
        }