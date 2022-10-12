from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from databases.base_class import Base


class UserLogin(Base):
    
    user_id = Column(String, primary_key=True, index=True)
    user_email = Column(String, nullable=False)
    user_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    user_role = Column(String)
    created_at = Column(String, default=datetime.now().strftime('%y-%m-%d %H:%M:%S'))
    updated_at = Column(String, default=datetime.now().strftime('%y-%m-%d %H:%M:%S'))
    is_first_login = Column(String, default="yes")

    # user_profile = relationship('userprofile', backref='UserProfile.user_id',
    #                             primaryjoin='UserLogin.user_id==UserProfile.user_id', lazy='dynamic')


class UserProfile(Base):
    user_id = Column(String, primary_key=True)
    user_name = Column(String, nullable=False)
    user_role = Column(String)
    user_phone = Column(String)
    user_address = Column(String)
    user_email = Column(String)
    theme = Column(String)
    # user_login = relationship('UserLogin', foreign_keys='UserLogin.user_id')

