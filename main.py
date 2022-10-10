from fastapi import FastAPI

from data_models.Schemas.users import UserRegistration, UserRegistrationResponse, UserLoginResponse, UserLoginRequest
from app.config import engine 
from databases.db_models.base_tables import Base
from services.authentication.default_auth_service import BaseAuthentication


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

@app.post("/user_registration", response_model=UserRegistrationResponse, tags=['User Registration and Login'])
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

@app.post("/login", response_model=UserLoginResponse, tags=['User Registration and Login'])
def login_user(user_login_req: UserLoginRequest):
    auth_service = BaseAuthentication.get_auth_service()
    return auth_service.verify_user(user_login_req.user_id, user_login_req.user_password)

# @app.post('/login/google', response_model=UserLoginResponse, tags=['User Registration and Login'])
# async def login_user1(request: Request):
#     redirect_uri = request.url_for('auth')
#     return await goauth.google.authorize_access_token(request, redirect_uri)

# @app.post('/token', response_model= Token)
# def