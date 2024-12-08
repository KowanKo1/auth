from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database import get_db
import requests
from sqlmodel import Session
import os

from typing import Annotated, Optional, List
from utils.auth import decode_access_token
from crud import get_account_by_email
from models import Item

router = APIRouter()
    
security = HTTPBearer()

INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")
AUTHENTICATION_SERVICE_URL = os.getenv("AUTHENTICATION_SERVICE_URL")

@router.get("/", response_model=List[Item])
async def read_items(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], category_id: Optional[int] = None, db:Session = Depends(get_db)):
    email = decode_access_token(credentials.credentials)
    account = get_account_by_email(db, email)
    
    requestParam = {
        'category_id': category_id
    }

    if account is None:
        raise HTTPException(status_code=400, detail="Account is not recognized")

    try:
        response = requests.get(f"{INVENTORY_SERVICE_URL}/items", params=requestParam, headers={"origin":AUTHENTICATION_SERVICE_URL})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to log transaction: {e}")

    return response.json()
    
@router.post("/", response_model=Item)
async def read_items(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], item: Item, db:Session = Depends(get_db)):
    email = decode_access_token(credentials.credentials)
    account = get_account_by_email(db, email)

    if account is None:
        raise HTTPException(status_code=400, detail="Account is not recognized")

    try:
        response = requests.post(f"{INVENTORY_SERVICE_URL}/items", json=item.dict(), headers={"origin":AUTHENTICATION_SERVICE_URL})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to log transaction: {e}")
    
    return response.json()
    
@router.put("/{item_id}/update_stock", response_model=Item)
async def read_items(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], item_id: int, quantity: int, transaction_type: str, db:Session = Depends(get_db)):
    email = decode_access_token(credentials.credentials)
    account = get_account_by_email(db, email)

    if account is None:
        raise HTTPException(status_code=400, detail="Account is not recognized")

    requestParams = {
        'quantity': quantity,
        'transaction_type': transaction_type
    }
    try:
        response = requests.put(f"{INVENTORY_SERVICE_URL}/items/{item_id}/update_stock", params=requestParams, headers={"origin":AUTHENTICATION_SERVICE_URL})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to log transaction: {e}")
    
    return response.json()