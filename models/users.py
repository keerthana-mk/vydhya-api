from typing import Union

from pydantic import BaseModel, EmailStr
from datetime import timedelta

class UserRegistrationResponse(BaseModel):
    message: str
    status_code: int


class UserLoginResponse(BaseModel):
    user_id: Union[str, None]
    user_name: Union[str, None]
    user_role: Union[str, None]
    theme: Union[str, None]
    token: Union[str, None]
    error: Union[str, None]


class UserLoginRequest(BaseModel):
    user_id: str
    user_password: str
class ResetPasswordRequest(BaseModel):
    reset_code: str
    user_password: str
    updated_at: str

class UserRegistration(BaseModel):
    user_id: Union[str, None]
    user_email: EmailStr
    user_password: str
    first_name: str
    last_name: str
    user_role: str
    is_first_login: Union[str, None]

class TokenData(BaseModel):
    user_id: Union[str,None] 
class Token(BaseModel):
    access_token: str
    token_type: str# class UserDetails(BaseModel, UsersRegistration):

    class Config():  # to convert non dict obj to json
        orm_mode = True


class ResetPassword(BaseModel):
    user_id: str
    user_email: EmailStr
    user_password: str
    updated_at: str

class ResetPasswordResponseMessage(BaseModel):
    message: str

class ResetPasswordResponse(BaseModel):
    status: int
    error: str
    data: ResetPasswordResponseMessage