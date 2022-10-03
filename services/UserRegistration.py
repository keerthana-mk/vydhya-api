from pydantic import BaseModel

class UserRegistration(BaseModel):
    userId : str
