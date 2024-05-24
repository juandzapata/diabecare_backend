from datetime import date
from pydantic.types import Decimal
from pydantic import BaseModel

class PacienteLista(BaseModel):
    nombre_completo: str
    fecha_actualizacion: date
    edad: int
    nivel_glucosa: Decimal
    actividad_fisica: Decimal
    medicamento: str
    ultima_comida: str
    