from pydantic import BaseModel
class RolUserLogin(BaseModel):
    rolId: int
    nombre: str