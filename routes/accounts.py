from utils.auth import *
from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from models import Account
from sqlmodel import Session
from contracts.auth import *
from crud import *

router = APIRouter()

@router.post('/register', summary="Create new account", response_model=RegisterResponse)
async def register(account: Account, db: Session = Depends(get_db)):
    exist = get_account_by_email(db, account.email)
    if exist is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account with this email already exist"
        )
            
    account.password = get_hashed_password(account.password)
    account.createdAt = datetime.now()
    account.modifiedAt = datetime.now()
    
    create_account(db, account)

    return RegisterResponse(message='New account has successfully created')


@router.post('/login', summary="Create access and refresh tokens for account", response_model=LoginResponse)
async def login(request:LoginRequest, db:Session = Depends(get_db)):
    account = get_account_by_email(db, request.email)
   
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = account.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    response: LoginResponse = LoginResponse(
         access_token=create_access_token(account.email),
    )

    return response