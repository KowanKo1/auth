from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from typing import Union, Any
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer
from utils.auth import *

from jose import jwt
from pydantic import ValidationError

def get_email(authorization: str) -> str:
    try:
        token = authorization[7:]
        payload = decode_access_token(token)
        print('payload: ', payload)
        # token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(payload.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload.sub