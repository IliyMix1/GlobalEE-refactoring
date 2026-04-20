from passlib.context import CryptContext
from jose import jwt, JWTError 
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

#Загружаем переменные из .env
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:  
    pwd_context.hash(password)

def verify_password(password_plain: str, password_hashed: str) -> bool:
    pwd_context.verify(password_plain, password_hashed)

def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload['exp'] = datetime.utcnow() +timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
