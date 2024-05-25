from pydantic import BaseModel

class tokenCreate(BaseModel):
    token: str
    userId: int

class tokenDeviceOut(BaseModel):
    tokenUsuarioId: int