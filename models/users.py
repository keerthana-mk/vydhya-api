from typing import Union

from pydantic import BaseModel, EmailStr


class UserRegistrationResponse(BaseModel):
    message: str
    status_code: int


class UserLoginResponse(BaseModel):
    user_id: Union[str, None]
    user_name: Union[str, None]
    user_role: Union[str, None]
    theme: Union[str, None]
    error: Union[str, None]


class UserLoginRequest(BaseModel):
    user_id: str
    user_password: str


class UserRegistration(BaseModel):
    user_id: Union[str, None]
    user_email: EmailStr
    user_password: str
    first_name: str
    last_name: str
    user_role: str
    is_first_login: Union[str, None]


    class Token(BaseModel):
        access_token: str
        token_type: str# class UserDetails(BaseModel, UsersRegistration):

    class Config():  # to convert non dict obj to json
        orm_mode = True