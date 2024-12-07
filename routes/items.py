from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database import get_db
from sqlmodel import Session

from typing import Annotated
from utils.auth import decode_access_token
from crud import get_account_by_email
from models import AuthCredentials

router = APIRouter()
    
security = HTTPBearer()

@router.get("/")
async def read_items(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], db:Session = Depends(get_db)):
    
    email = decode_access_token(credentials.credentials)
    account = get_account_by_email(db, email)

    if account is None:
        raise HTTPException(status_code=400, detail="Account is not recognized")

    return account