from pydantic import BaseModel

class tokenCreate(BaseModel):
    token: str
    usuarioId: int

class tokenDeviceOut(BaseModel):
    tokenUsuarioId: int