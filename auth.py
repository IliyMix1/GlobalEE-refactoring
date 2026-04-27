from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session, select_record
from models.models import User
from datetime import datetime, timedelta
from jose     import jwt, JWTError 
from dotenv   import load_dotenv
import bcrypt
import os

#Загружаем переменные из .env
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
security = HTTPBearer()

def hash_password(password: str) -> str:  
    #Обрезаем начальную строку, превращаем в байты и добавляем "соль"
    return bcrypt.hashpw(password[:70].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password_plain: str, password_hashed: str) -> bool:
    #Убираем "соль" из хэша и сравниваем введённый пароль с тем, что лежит в БД
    return bcrypt.checkpw(password_plain[:70].encode('utf-8'), password_hashed[:70].encode('utf-8'))

def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload['exp'] = datetime.utcnow() +timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: AsyncSession = Depends(get_session)):
    '''Проверяет залогинен ли пользователь'''
    #Достаём токен из заголовка
    token = credentials.credentials

    try:
        #Расшифровываем jwt-токен и достаёт оттуда id
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail='Authentication required')
        
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')

    return await select_record(id=user_id, model=User, session=session)