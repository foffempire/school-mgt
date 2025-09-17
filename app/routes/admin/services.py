from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.db import models
from app.security import oauth2
from app.security.security import get_password_hash
from .schema import AdminCreate, MakeAdmin



def email_exist(email: str, db: Session):
    query = db.exec(select(models.AdminAccount).where(models.AdminAccount.email == email)).first()
    if query:
        return True
    else:
        return False



def create_account(db: Session, admin = AdminCreate):
    if(email_exist(admin.email, db)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email have been used, try another email")
    
    admin.password = get_password_hash(admin.password)
    query = models.AdminAccount.model_validate(admin)
    db.add(query)
    db.commit()
    db.refresh(query)

    #create a token
    access_token = oauth2.create_access_token(data = {"id": query.id})
    
    return {"access_token": access_token, "token_type":"Bearer", "user": query}



def make_admin(db: Session, school_id, new = MakeAdmin):
    
    if(email_exist(new.email, db)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email have been used, try another email")
    
    data = {
        "school_id": school_id,
        "email": new.email,
        "password": get_password_hash(new.password),
        "firstname": new.firstname,
        "lastname": new.lastname,
        "role": "staff"
    }

    query = models.AdminAccount.model_validate(data)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def deactivate_account(user_id, db: Session):
    query = db.exec(select(models.AdminAccount).where(models.AdminAccount.id == user_id)).first()

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # cannot deactivate an admin
    if(query.role == 'admin'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You cannot deactivate an admin")
 
    
    query.is_active = False
    db.add(query)
    db.commit()
    return {"success": "Deleted Successfully"}
