from fastapi import FastAPI

from data_models.Schemas.users import UserRegistration, UserRegistrationResponse, UserLoginResponse, UserLoginRequest
from data_models.Schemas.profiles import UserProfileResponse, UserProfileRequests
from app.config import engine 
from databases.db_models.base_tables import Base
from services.authentication.default_auth_service import BaseAuthentication
from services.Profile.profiles_services import ProfileServices
from data_models.Schemas.profiles import PatientProfileResponse
from data_models.Schemas.commons import convert_patient_reponse, convert_doctor_response, convert_insurer_response
from data_models.Schemas.logging import logger


def create_tables():  # new
    print("Creating tables")
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title="Vydhya", version="v1")
    # create_tables()
    return app

logger.info('****************** Starting Server *****************')

app = start_application()

@app.on_event('startup')
def create_all_tables():
    create_tables()


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

@app.post("/profile", response_model=UserProfileResponse, tags=['User Profiles'], response_model_exclude_none=True)
def update_user_profile(user_id, user_role, user_profile : UserProfileRequests):

    profile_service = ProfileServices()
    if user_role == 'patient':
        updated_user_profile = profile_service.update_user_profile(user_id, user_role, user_profile.patient)
        return convert_patient_reponse(updated_user_profile)
    if user_role == 'doctor':
        updated_user_profile = profile_service.update_user_profile(user_id, user_role, user_profile.doctor)
        return convert_doctor_response(updated_user_profile)
    if user_role == 'insurer':
        updated_user_profile = profile_service.update_user_profile(user_id, user_role, user_profile.insurer)
        return convert_insurer_response(updated_user_profile)
    
@app.get("/profile", response_model=UserProfileResponse, tags=['User Profiles'],response_model_exclude_none=True)      
def get_user_profiles(user_id, user_role):
    profile_service = ProfileServices()
    if user_role == 'patient':
        user_profile_details = profile_service.get_user_profile(user_id, user_role)
        return convert_patient_reponse(user_profile_details)
    if user_role == 'doctor':
        user_profile_details = profile_service.get_user_profile(user_id, user_role)
        return convert_doctor_response(user_profile_details)
    if user_role == 'insurer':
        user_profile_details = profile_service.get_user_profile(user_id, user_role)
        return convert_insurer_response(user_profile_details)
    
    return ' User role doesnt exist'
    
