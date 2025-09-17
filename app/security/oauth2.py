from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel import select
from app.core.config import settings
from app.db import database, models
from .schema import TokenData 


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except jwt.PyJWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(session: database.SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token,  credentials_exception)
    user = session.exec(select(models.AdminAccount).where(models.AdminAccount.id == token.id)).first()
    return user



def get_admin_user(session: database.SessionDep, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token,  credentials_exception)
    user = session.exec(select(models.AdminAccount).where(models.AdminAccount.id == token.id)).first()
    if(user.role.lower() != 'admin'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not authorized to perform this action")
    return user
    


CurrentUserDep = Annotated[str, Depends(get_current_user)]
AdminUserDep = Annotated[str, Depends(get_admin_user)]