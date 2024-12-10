from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database import get_db
import requests
from sqlmodel import Session
import os

from typing import Annotated, List
from dto import TransactionResponse
from utils.auth import decode_access_token
from crud import get_account_by_email
from models import Transaction

router = APIRouter()
    
security = HTTPBearer()

TRANSACTION_SERVICE_URL = os.getenv("TRANSACTION_SERVICE_URL")
AUTHENTICATION_SERVICE_URL = os.getenv("AUTHENTICATION_SERVICE_URL")

@router.get("/", response_model=List[TransactionResponse])
async def read_items(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], db:Session = Depends(get_db)):
    email = decode_access_token(credentials.credentials)
    account = get_account_by_email(db, email)

    if account is None:
        raise HTTPException(status_code=400, detail="Account is not recognized")

    try:
        response = requests.get(f"{TRANSACTION_SERVICE_URL}/api/transactions", headers={"origin":AUTHENTICATION_SERVICE_URL, "email":email})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to log transaction: {e}")
    
    return response.json()