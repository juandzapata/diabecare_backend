from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from utils.jwt import validate_token


class NeedToken(HTTPBearer):
    async def _call_(self, request: Request):
        auth = await super()._call_(request)
        if auth is None:
            raise HTTPException(
                status_code=401, detail="Not authorized add the token")
        return auth.credentials