from datetime import timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from app.db import models
from app.db.database import SessionDep
from app.security import oauth2
from app.security.security import verify_password


async def login_(db: SessionDep, form_data: OAuth2PasswordRequestForm):
    
    form_data.username = form_data.username.lower()
    user = db.exec(select(models.AdminAccount).where(models.AdminAccount.email == form_data.username, models.AdminAccount.is_active == True)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid login details")
    
    verfy_pass = verify_password(form_data.password, user.password)
    if not verfy_pass:
        raise HTTPException(status_code=401, detail="Invalid login details")
    


    #create a token
    access_token = oauth2.create_access_token(data = {"id": user.id})

    # return token
    return {"access_token": access_token, "token_type":"Bearer", "user":user}


