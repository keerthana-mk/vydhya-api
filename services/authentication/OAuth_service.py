from typing  import Optional
from app.config import Oauth_settings
from jose import jwt, JWTError


def create_access_token(data:dict, expires: Optional[timedelta]):
    to_encode = data.copy()
    if expires:
        expires= datetime.utcnow() + expires
    else:
        expires=datetime.utcnow() + timedelta(minutes=Oauth_settings.ACCESS_TOKEN_EXPIRATION )
    to_encode.update({"expiry": expires})
    encoded_jwt = jwt.encode(to_encode,Oauth_settings.SECRET_KEY, algorithm=Oauth_settings.ALGORITHM)

    return encoded_jwt

