from asyncio.windows_events import NULL
from email import message
from urllib import response
from fastapi import FastAPI, Depends

from data_models.Schemas.users import UserRegistration, UserRegistrationResponse, UserLoginResponse, UserLoginRequest
from databases.db_connection import engine, get_db
from databases.db_models.base_tables import Base
from services.authentication.default_auth_service import BaseAuthentication
from vydhya_api.data_models.Schemas.users import ResetPassword, ResetPasswordResponse


def create_tables():  # new
    print("Creating tables")
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title="Vydhya", version="v1")
    create_tables()
    return app


app = start_application()

@app.get("/")
async def root():
    # return check_db_connected()
    return {"message": "Hello World"}


@app.post("/login", response_model=UserLoginResponse, tags='User Login')
def login_user(user_login_req: UserLoginRequest):
    auth_service = BaseAuthentication.get_auth_service()
    return auth_service.verify_user(user_login_req.user_id, user_login_req.user_password)


@app.post("/user_registration", response_model=UserRegistrationResponse, tags='User Registration and Login')
def create_user(user_details: UserRegistration):
    auth_service = BaseAuthentication.get_auth_service()
    try:
        auth_service.add_user(user_details)
        response = UserRegistrationResponse(
            message=f'successfully created user {user_details.user_id}',
            status_code=200
        )
    except Exception as e:
        response = UserRegistrationResponse(
            message=f'failed to register user: {str(e)}',
            status_code=500
        )
    return response

@app.post("/reset_password", response_model=ResetPasswordResponse, tags="Reset Password")
def update_password(user_password: ResetPassword):
    auth_service= BaseAuthentication.get_auth_service()
    try:
        auth_service.reset_password(user_password)
        response = ResetPasswordResponse(
            status=200,
            error= NULL,
            data= {
                message:'Reset successful for '+str(user_password.user_id)
            }
        )
    except Exception as e:
        response= ResetPasswordResponse(
            status=500,
            error="Failed to reset password"+ str(e),
            data={
                message: "Reset unsuccessful "+str(e)
            }
        )

    return response
