from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean,Date, ForeignKey
from sqlalchemy.orm import relationship

from databases.base_class import Base

class User_login(Base):
    user_id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False)
    user_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    user_role = Column(String)
    created_at = Column(String, default=datetime.now().strftime('%y-%m-%d %H:%M:%S'))
    updated_at = Column(String, default=datetime.now().strftime('%y-%m-%d %H:%M:%S'))
    isFirstLogin = Column(String, default="yes")

