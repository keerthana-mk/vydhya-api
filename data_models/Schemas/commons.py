from pydantic import BaseModel, validator, EmailStr
from datetime import datetime


class DateTimeModel(BaseModel):
    created_at: datetime
    updated_at: datetime

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(
            cls,
            value: datetime,
    ) -> datetime:
        return value or datetime.now().strftime('%y-%m-%d %H:%M:%S')

class EmailSchema(BaseModel):
    email: List[EmailStr]