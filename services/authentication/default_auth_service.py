import hashlib
import logging
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from databases.repository.users import UserLoginRepository

from models.users import ResetPassword, UserRegistration, UserLoginResponse
from app.config import get_db_actual, Oauth_settings
from databases.db_models.users import UserLogin
from services.profiles_services import *
from .OAuth_service import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




class BaseAuthentication:

    def verify_user(self, username, password):
        pass

    def generate_token(self, username, password):
        pass

    def add_user(self, user_details: UserRegistration):
        pass

    def reset_password(self, password_details: ResetPassword):
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
        try:
            hashed_password = DefaultAuthentication.generate_hash(password)
            user_login = UserLoginRepository.get_user_login(user_id)
            if user_login is None:
                # return {"message": f"userid = {user_id} does not exist"}
                raise BaseException(error=f'user not found')
            elif user_login.user_password != hashed_password:
                # return {"message" : f'username or password is incorrect!'}
                raise BaseException(error=f'user credentials invalid')
            else:
                user_profile = self.profile_services.get_user_profile(user_login.user_id, user_login.user_role)
                token_details = {"user_id" : user_profile.user_id,
                                 "user_name" : user_profile.contact_email,
                                 "fullname" : f"{user_login.first_name} {user_login.last_name}",
                                 "user_role" :user_login.user_role,
                                 "theme" : user_profile.theme,
                }
                access_token = create_access_token(token_details, Oauth_settings.ACCESS_TOKEN_EXPIRATION)            
                return UserLoginResponse(
                    user_id=user_profile.user_id,
                    user_name=user_profile.contact_email,
                    theme=user_profile.theme,
                    user_role=user_login.user_role,
                    token = access_token
                )
        except BaseException as e:
            error_message = f"could not fetch the user details for user = {user_id}: {str(e)}"
            # return {"message" : error_message}
            raise BaseException(error_message)
        
    def add_user(self, user_details: UserRegistration):
        profile_service = ProfileServices()
        if UserLoginRepository.get_user_login(user_details.user_id) is not None:
            error_message = f'user_id {user_details.user_id} or user_email {user_details.user_email} already exists'
            logging.error(error_message)
            raise Exception(error_message)

        hashed_password = DefaultAuthentication.generate_hash(user_details.user_password)
        try:
            user_id = UserLoginRepository.add_user_login(user_details.user_email, hashed_password,
                                                         user_details.first_name, user_details.last_name,
                                                         user_details.user_role)
            user_name = f'{user_details.first_name} {user_details.last_name}'
            logging.info("successfully added userlogin details")
            profile_service.create_user_profile(user_id, user_name, user_details.user_email, user_details.user_role,
                                                      "primary")
            return user_id
        except Exception as e:
            error_message = f'error while inserting to database: {str(e)}'
            raise Exception(error_message)

    def reset_password(self,password_details: ResetPassword):

        hashed_password= DefaultAuthentication.generate_hash(password_details.user_password)

        try:
            UpdatePassword.update_password(password_details.user_id,hashed_password,password_details.updated_at)

        except Exception as e:
            error_message = f'Error while reseting password: {str(e)}'
            raise Exception(error_message)

        return "Reset successful"

        


    @staticmethod
    def generate_hash(password):
        return hashlib.md5(bytes(password, 'utf-8')).hexdigest()
        # return pwd_context.hash(password)
