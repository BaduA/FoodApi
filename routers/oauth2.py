from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
import schemas
import database
import models
from sqlalchemy.orm import Session
from config import settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_DAYS = settings.access_token_expire_days


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, creds_exc):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_signature": False},
        )
        id: str = payload.get("user_id")
        if id is None:
            raise creds_exc
        token_data = schemas.TokenData(id=id)
        return token_data
    except Exception as err:
        raise creds_exc


def get_current_user(
    token: str = Depends(oauth_scheme), db: Session = Depends(database.get_db)
):

    creds_Exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, creds_Exc)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

