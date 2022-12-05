from typing  import Optional
from app.config import Oauth_settings
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.users import TokenData
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
import logging
import json



def create_access_token(data, expires: Optional[timedelta]):
    logging.info(f'data dictionary is {data}')
    to_encode = data.copy()
    if expires:
        expires= datetime.utcnow() + timedelta(expires)
    else:
        expires=datetime.utcnow() + timedelta(minutes=Oauth_settings.ACCESS_TOKEN_EXPIRATION)
        
    # to_encode.update({"expiry": json.dumps(expires, default=json_serial)})

    to_encode.update({"expiry": expires.strftime('%Y-%m-%d %H:%M:%S')})
    encoded_jwt = jwt.encode(to_encode,Oauth_settings.SECRET_KEY, algorithm=Oauth_settings.ALGORITHM)

    return encoded_jwt

