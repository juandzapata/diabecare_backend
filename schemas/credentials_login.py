from pydantic import BaseModel


class CredentialsLogin(BaseModel):
    email: str
    password: str