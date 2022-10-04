from sqlalchemy import or_
from sqlalchemy.orm import Session, Query

from databases.db_connection import get_db_actual
from databases.db_models.users import UserLogin, UserProfile


class UserLoginRepository:
    database: Session = get_db_actual()

    @staticmethod
    def get_user_login(user_id, user_email):
        query_result = UserLoginRepository.database.query(UserLogin).filter(
            or_(UserLogin.user_id == user_id, UserLogin.user_email == user_email))
        query_result = query_result.all()
        return query_result[0] if len(query_result) == 1 else None

    @staticmethod
    def get_last_user():
        query_result = UserLoginRepository.database.query(UserLogin.user_id).order_by(UserLogin.user_id)
        query_result = query_result.all()
        return query_result[len(query_result) - 1] if len(query_result) > 0 else None

    @staticmethod
    def add_user_login(user_email, user_password, first_name, last_name, user_role, created_at, updated_at):
        last_user = UserLoginRepository.get_last_user()
        if last_user is None:
            last_user_num = 0
        else:
            last_user_num = int(last_user.user_id.split('_')[1])
        new_user_id = f'{user_role}_{last_user_num + 1}'
        new_user_login = UserLogin(
            user_id=new_user_id,
            user_email=user_email,
            user_password=user_password,
            first_name=first_name,
            last_name=last_name,
            user_role=user_role,
            created_at=created_at,
            updated_at=updated_at,
            is_first_login="yes"
        )
        UserLoginRepository.database.add(new_user_login)
        UserLoginRepository.database.commit()
        return new_user_id


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
        query_result = UserProfileRepository.database.query(UserProfile)\
            .filter(or_(UserProfile.user_id == user_id, UserProfile.user_email == user_id))
        query_result = query_result.all()
        return query_result[0] if len(query_result) == 1 else None
