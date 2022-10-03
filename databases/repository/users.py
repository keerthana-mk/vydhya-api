from sqlalchemy.orm import Session

from data_models.Schemas.Users import UsersRegistration
from data_models.Schemas.commons import DateTimeModel
from databases.db_models.users import User_login
from core.hashing import Hasher


def create_new_user(user:UsersRegistration,datetimeobj:DateTimeModel,db:Session):
    user = User_login(
        user_id = "P_001"
        user_email = user.email,
        user_password=Hasher.get_password_hash(user.password),
        first_name =user.first_name
        last_name = user.last_name
        user_role = user.user_role
        created_at = user.created_at
        updated_at = user.updated_at
        isFirstLogin="yes",
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

