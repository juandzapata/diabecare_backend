from models.base import TokenUsuario
from schemas.token import tokenCreate, tokenDeviceOut


def post_token (token: tokenCreate, database) -> tokenDeviceOut:
    db_token : TokenUsuario = TokenUsuario(
        tokenDispositivo = token.token,
        usuarioId = token.usuarioId
    )
    database.add(db_token)
    database.commit()
    database.refresh(db_token)
    return db_token.tokenUsuarioId