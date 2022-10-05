import hashlib

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from data_models.Schemas.users import UserRegistration, UserLoginResponse
from databases.db_connection import get_db, get_db_actual
from databases.db_models.users import UserLogin
from databases.repository.users import UserLoginRepository, UserProfileRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseAuthentication:

    def verify_user(self, username, password):
        pass

    def generate_token(self, username, password):
        pass

    def add_user(self, user_details: UserRegistration):
        pass

    @staticmethod
    def get_auth_service():
        return DefaultAuthentication()


class DefaultAuthentication(BaseAuthentication):

    def __init__(self):
        self.database: Session = get_db_actual()
        self.orm_model = UserLogin

    def verify_user(self, user_id, password, user_login=None):
        hashed_password = DefaultAuthentication.generate_hash(password)
        user_login = UserLoginRepository.get_user_login(user_id, user_id)
        print(f'hashed_password: {hashed_password} \nfrom_database: {str(user_login.user_password)}')
        if user_login is None:
            return UserLoginResponse(
                error=f'user not found'
            )
        elif user_login.user_password != hashed_password:
            return UserLoginResponse(
                error=f'user credentials invalid'
            )
        else:
            user_profile = UserProfileRepository.get_user_profile(user_id)
            return UserLoginResponse(
                user_id=user_profile.user_id,
                user_email=user_profile.user_email,
                theme=user_profile.theme,
                user_role=user_profile.user_role
            )

    def add_user(self, user_details: UserRegistration):
        if UserLoginRepository.get_user_login(user_details.user_id, user_details.user_email) is not None:
            error_message = f'user_id {user_details.user_id} or user_email {user_details.user_email} already exists'
            print(error_message)
            raise Exception(error_message)

        hashed_password = DefaultAuthentication.generate_hash(user_details.user_password)
        try:
            user_id = UserLoginRepository.add_user_login(user_details.user_email, hashed_password,
                                                         user_details.first_name, user_details.last_name,
                                                         user_details.user_role, user_details.created_at,
                                                         user_details.updated_at)
            UserProfileRepository.create_user_profile(user_id, user_details.user_email, user_details.user_role,
                                                      "primary")
            return True
        except Exception as e:
            error_message = f'error while inserting to database: {str(e)}'
            print(error_message)
            raise Exception(error_message)

    @staticmethod
    def generate_hash(password):
        return hashlib.md5(bytes(password, 'utf-8')).hexdigest()
        # return pwd_context.hash(password)
