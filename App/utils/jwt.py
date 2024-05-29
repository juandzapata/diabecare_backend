import os
from jose import jwt
from schemas.user import GetUser


def create_token(user: GetUser) -> str:
    key_hash = os.environ.get('KEY_HASH_TOKEN')
    token: str = jwt.encode(
        claims=user.model_dump(),
        key=key_hash, 
        algorithm='HS256'
    )
    return token


def validate_token(token: str) -> dict | None:
    key_hash = os.environ.get('KEY_HASH_TOKEN')
    try:
        data: dict = jwt.decode(
            token=token, 
            key=key_hash, 
            algorithms=['HS256']
        )
        return data
    except jwt.JWTError:
        return None
    except jwt.ExpiredSignatureError:
        return None
