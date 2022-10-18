from fastapi import FastAPI

from app.config import engine
from data_models.Schemas.profiles import UserProfileResponse, UserProfileRequests, PatientProfileResponse
from data_models.Schemas.users import UserRegistration, UserRegistrationResponse, UserLoginResponse, UserLoginRequest
from databases.db_models.base_tables import Base
from services.authentication.default_auth_service import BaseAuthentication
from services.authentication.profiles_services import ProfileServices


def create_tables():  # new
    print("Creating tables")
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title="Vydhya", version="v1")
    # create_tables()
    return app


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

@app.post("/profile", response_model=UserProfileResponse, tags=['User Profiles'])
def update_patient_profile(user_id, user_role, user_profile: UserProfileRequests):
    profile_service = ProfileServices()
    if user_role == 'patient':
        updated_user_profile = profile_service.update_user_profile(user_id, user_role, user_profile['patient'])
        return UserProfileResponse(patient=PatientProfileResponse(user_id=updated_user_profile.user_id,
                                                                  user_name=updated_user_profile.user_name,
                                                                  user_email=updated_user_profile.user_email,
                                                                  theme=updated_user_profile.theme,
                                                                  gender=updated_user_profile.gender,
                                                                  dob=updated_user_profile.dob,
                                                                  height=updated_user_profile.height,
                                                                  weight=updated_user_profile.weight,
                                                                  vaccinations=updated_user_profile.vaccinations,
                                                                  blood_type=updated_user_profile.blood_type,
                                                                  allergies=updated_user_profile.allergies,
                                                                  medications=updated_user_profile.medications,
                                                                  blood_pressure=updated_user_profile.blood_pressure,
                                                                  preexist_conditions=updated_user_profile.preexist_conditions,
                                                                  health_plan_id=updated_user_profile.health_plan_id,
                                                                  monthly_medical_expense=updated_user_profile.monthly_medical_expense))
