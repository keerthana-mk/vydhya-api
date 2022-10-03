from datetime import datetime, date
from pydantic import BaseModel, EmailStr
from data_models.Schemas.commons import DateTimeModel

class UsersRegistration(BaseModel):
    userId : str
    userEmail : EmailStr
    user_password: str
    FirstName: str
    LastName : str
    Role : str
    isFirstTimeLogin : str
    created_at : str
    updated_at: str

# class UserDetails(BaseModel, UsersRegistration):

    class Config():  # to convert non dict obj to json
        orm_mode = True