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
    usuarioid: int
    nombre: str
    apellidos: str
    correo: str
    contraseña: str
    sexo: str
    ciudad: str
    foto: str
    fechaNacimiento: date

def model_dump(self):
    return {
        "id": self.id,
        "nombre": self.nombre,
        "apellidos": self.apellidos,
        "correo": self.correo
    }
