import os
from models.base import Usuario
from schemas.user import UserGetLogin
from utils import auth, jwt as jwt
from schemas.credentials_login import CredentialsLogin



def login(credentials: CredentialsLogin, db) -> str:
    if not exit_user(credentials.email, db):
        return None
    user = get_user_by_email(credentials.email, db)
    if user and auth.check_password(credentials.password, user.contraseña):
        user_get = UserGetLogin(
            usuarioId=user.usuarioId,
            nombre=user.nombre,
            apellidos=user.apellidos,
            correo=user.correo,
            contraseña=user.contraseña,
            sexo=user.sexo,
            ciudad=user.ciudad,
            foto=user.foto,
            fechaNacimiento=user.fechaNacimiento.__str__(),
            rolId = 0
        )
        if user.rolId is not None:
            user_get.rolId = user.rolId
        token = jwt.create_token(user_get)
    return token


def validate_token(token: str, db) -> dict:
    data_token = jwt.validate_token(token)
    if not data_token:
        return None
    return data_token

def exit_user(email: str, db) -> bool:
    user = get_user_by_email(email, db)
    return user != None


def get_user_by_email(email: str, db) -> Usuario:
    user = db.query(Usuario).filter(Usuario.correo == email).first()
    return user