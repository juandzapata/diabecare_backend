from datetime import date
from pydantic import BaseModel


class GetUsuario(BaseModel):
    id: int
    nombre: str
    apellidos: str
    correo: str
    contrasena: str
    sexo: str
    ciudad: str
    foto: str
    fecha_nacimiento: date
    
    
