from pydantic import BaseModel
from models import Account

class LoginRequest(BaseModel):
    email: str
    password:str

class RegisterResponse(BaseModel):
    message: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token:str