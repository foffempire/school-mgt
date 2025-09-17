from typing import Annotated
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext



#**********Verify ownership****************
def is_owner(item_school_id, user_school_id):
    if item_school_id == user_school_id:
        return True
    else:
        return False
    


#**********password Hashing****************
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)




# **************** API KEYS****************
API_KEY_NAME = "SMA-Key"
API_KEYS = {"redis_05df4682305df46a0df38ef5140bb718", "admin_7af870e2b3848ae926fb9958718bab7c", "web_d7b19fc1b47c472e55a201ddbd11cae8", "app_14c9a3ce11b2aa1f46f7bcf7339c7db3", "other_44b4ab34e05b23d806f4a9eb5bb5a24a", "other_90f9c300a74c6b3a0bc7e460513fbbea"}

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key in API_KEYS:
        return api_key 
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid or missing API Key",
    )

APIKeyDep = Annotated[str, Depends(get_api_key)]