from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import datetime
from app.config import get_db, get_db_actual
from databases.db_models.users import UserLogin, UserProfile

class UserLoginRepository:
    database: Session = get_db_actual()

    @staticmethod
    def get_user_login(user_id):
        query_result = UserLoginRepository.database.query(UserLogin).filter(
            or_(UserLogin.user_id == user_id, UserLogin.user_name == user_id))
        query_result = query_result.all()
        return query_result[0] if len(query_result) == 1 else None

    @staticmethod
    def get_last_user():
        query_result = UserLoginRepository.database.query(UserLogin.user_id).order_by(UserLogin.user_id)
        query_result = query_result.all()
        return query_result[len(query_result) - 1] if len(query_result) > 0 else None

    @staticmethod
    def add_user_login(user_email, user_password, first_name, last_name, user_role):
        try:
            last_user = UserLoginRepository.get_last_user()
            if last_user is None:
                last_user_num = 0
            else:
                last_user_num = int(last_user.user_id.split('_')[1])
            new_user_id = f'{user_role}_{last_user_num + 1}'
            new_user_login = UserLogin(
                user_id=new_user_id,
                user_name=user_email,
                user_password=user_password,
                first_name=first_name,
                last_name=last_name,
                user_role=user_role,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_first_login="yes"
                )
            UserLoginRepository.database.add(new_user_login)
            UserLoginRepository.database.commit()
            return new_user_id
        except Exception as e:
            UserLoginRepository.database.rollback()
            error_message = "Error while creating user for user: {}".format(e)
            raise(e)

    @staticmethod
    def update_reset_code(user_id, reset_details):
        try:
            query_result = UserLoginRepository.database.query(UserLogin)\
                .filter(or_(UserLogin.user_id == user_id, UserLogin.user_name == user_id)).update(reset_details)
            UserLoginRepository.database.commit()
        except Exception as e:
            UserLoginRepository.database.rollback()
            raise BaseException(e)
    @staticmethod
    def update_password(user_id, password_details):
        try:
            query = UserLoginRepository.database.query(UserLogin). filter(or_(UserLogin.user_id == user_id, UserLogin.user_name == user_id))\
                .update(password_details)
            UserLoginRepository.database.commit()
        except Exception as e:
            UserLoginRepository().database.rollback()
            raise BaseException(e)              

class UserProfileRepository:
    database: Session = get_db_actual()

    @staticmethod
    def create_user_profile(user_id, user_email, user_role, theme):
        new_user_profile = UserProfile(
            user_id=user_id,
            user_name=user_email,
            user_email=user_email,
            user_role=user_role,
            theme=theme
            )
        UserProfileRepository.database.add(new_user_profile)
        UserProfileRepository.database.commit()

    @staticmethod
    def get_user_profile(user_id):
        query_result = UserProfileRepository.database.query(UserProfile) \
            .filter(or_(UserProfile.user_id == user_id, UserProfile.user_name == user_id))
        query_result = query_result.all()
        return query_result[0] if len(query_result) == 1 else None
    
    @staticmethod
    def store_profile_pic_database(user_id, base64_encode):
        try:
            profile_pic_details ={"profile_pic": base64_encode}
            query = UserLoginRepository.database.query(UserLogin).filter(or_(UserLogin.user_id == user_id, UserLogin.user_name == user_id))\
            .update(profile_pic_details)
            UserLoginRepository.database.commit()
        except Exception as e:
            UserLoginRepository().database.rollback()
            raise BaseException(e)
    @staticmethod
    def fetch_profile_image(user_id):
        query_result =  UserLoginRepository.database.query(UserLogin).filter(or_(UserLogin.user_id == user_id, UserLogin.user_name == user_id))
        query_result = query_result.all()
        return query_result[0].profile_pic
    