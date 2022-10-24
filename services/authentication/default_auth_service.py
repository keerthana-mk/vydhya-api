import hashlib

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.users import UserRegistration, UserLoginResponse
from app.config import get_db_actual
from databases.db_models.users import UserLogin
from services.profiles_services import *
# from Profile.profiles_services import ProfileServices

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
        self.profile_services = ProfileServices()

    def verify_user(self, user_id, password, user_login=None):
        hashed_password = DefaultAuthentication.generate_hash(password)
        user_login = UserLoginRepository.get_user_login(user_id, user_id)
        if user_login is None:
            raise Exception(error=f'user not found')
        elif user_login.user_password != hashed_password:
            raise Exception(error=f'user credentials invalid')
        else:
            user_profile = self.profile_services.get_user_profile(user_login.user_id, user_login.user_role)
            return UserLoginResponse(
                user_id=user_profile.user_id,
                user_name=user_profile.contact_email,
                theme=user_profile.theme,
                user_role=user_login.user_role
            )

    def add_user(self, user_details: UserRegistration):
        profile_service = ProfileServices()
        if UserLoginRepository.get_user_login(user_details.user_id, user_details.user_email) is not None:
            error_message = f'user_id {user_details.user_id} or user_email {user_details.user_email} already exists'
            logger.error(error_message)
            raise Exception(error_message)

        hashed_password = DefaultAuthentication.generate_hash(user_details.user_password)
        try:
            user_id = UserLoginRepository.add_user_login(user_details.user_email, hashed_password,
                                                         user_details.first_name, user_details.last_name,
                                                         user_details.user_role)
            user_name = f'{user_details.first_name} {user_details.last_name}'
            profile_service.create_user_profile(user_id, user_details.user_email, user_details.user_role,
                                                      "primary")
            return True
        except Exception as e:
            error_message = f'error while inserting to database: {str(e)}'
            logger.error(error_message)
            raise Exception(error_message)

    @staticmethod
    def generate_hash(password):
        return hashlib.md5(bytes(password, 'utf-8')).hexdigest()
        # return pwd_context.hash(password)
