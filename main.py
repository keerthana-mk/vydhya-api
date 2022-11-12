import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from app.config import engine, get_db
from databases.repository.users import UserLoginRepository
from models.healthcare_plans import AddHealthcarePlanRequest, AddHealthcarePlanResponse, UpdateHealthcarePlanRequest
from models.profiles import UserProfileRequests, SearchDoctorRequest
from models.users import UserRegistration, UserRegistrationResponse, UserLoginRequest, ResetPasswordRequest
from databases.db_models.base_tables import Base
from services.authentication.default_auth_service import BaseAuthentication
from services.doctor_services import DoctorService
from services.insurer_services import InsurerServices
from services.profiles_services import ProfileServices
from services.authentication.reset_password_service import ResetPasswordServices
from models.commons import convert_patient_reponse, convert_doctor_response, convert_insurer_response, \
    get_http_response, StandardHttpResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
fh = logging.FileHandler(filename='./server.log')
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
    )
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)  # Exporting logs to the screen
# logger.addHandler(fh)  # Exporting logs to a file

def create_tables():  # new
    logger.error("Creating tables...")
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title="Vydhya", version="v1")
    origins = [
        "http://localhost:8000",
        "http://localhost:3000",
        "https://vydhya.netlify.app/",
        "http://localhost",
        "http://localhost:8080",
        ]
    app.add_middleware(CORSMiddleware,
                       allow_origins=["*"],
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"],
                       )
    return app

# logger.info('****************** Starting Server *****************')

app = start_application()

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        # reload=True,
        port=8000,
        )

@app.on_event('startup')
def create_all_tables():
    create_tables()

@app.get("/")
async def root():
    # return check_db_connected()
    return {"message": "Hello World"}

@app.post("/user_registration", response_model=StandardHttpResponse, tags=['User Registration and Login'],
          response_model_exclude_none=True )
def create_user(user_details: UserRegistration):
    auth_service = BaseAuthentication.get_auth_service()
    error_message, data = None, None
    try:
        auth_service.add_user(user_details)
        data = UserRegistrationResponse(
            message=f'successfully created user {user_details.user_id}',
            status_code=200
            )
        status = 200
    except Exception as e:
        error_message = f'failed to register user: {str(e)}'
        status = 500
    return JSONResponse(get_http_response(data, status, error_message), status_code=status)

@app.post("/login", response_model=StandardHttpResponse, tags=['User Registration and Login'],
          response_model_exclude_none=True)
def login_user(user_login_req: UserLoginRequest):
    auth_service = BaseAuthentication.get_auth_service()
    error_message, data = None, None
    try:
        data = auth_service.verify_user(user_login_req.user_id, user_login_req.user_password)
        status = 200
    except Exception as e:
        error_message = f'error while authenticating user {user_login_req.user_id}: {str(e)}'
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

# @app.post('/login/google', response_model=UserLoginResponse, tags=['User Registration and Login'])
# async def login_user1(request: Request):
#     redirect_uri = request.url_for('auth')
#     return await goauth.google.authorize_access_token(request, redirect_uri)

# @app.post('/token', response_model= Token)
# def

@app.post("/profile", response_model=StandardHttpResponse, tags=['User Profiles'], response_model_exclude_none=True)
def update_user_profile(user_id, user_role, user_profile: UserProfileRequests):
    profile_service = ProfileServices()
    error_message, data = None, None
    try:
        if user_role == 'patient':
            updated_user_profile = profile_service.update_user_profile(user_id, user_role, user_profile.patient)
            data = convert_patient_reponse(updated_user_profile)
            status = 200
        elif user_role == 'doctor':
            updated_user_profile = profile_service.update_user_profile(user_id, user_role, user_profile.doctor)
            data = convert_doctor_response(updated_user_profile)
            status = 200
        elif user_role == 'insurer':
            updated_user_profile = profile_service.update_user_profile(user_id, user_role, user_profile.insurer)
            data = convert_insurer_response(updated_user_profile)
            status = 200
        else:
            error_message = f'unsupported user_role: {user_role}'
            status = 500
    except Exception as e:
        error_message = f'error while authenticating user {user_id}: {str(e)}'
        status = 500
    return JSONResponse(get_http_response(data, status, error_message), status_code=status)

@app.get("/profile", response_model=StandardHttpResponse, tags=['User Profiles'], response_model_exclude_none=True)
def get_user_profiles(user_id, user_role):
    logger.info("please tell me i am here")
    profile_service = ProfileServices()
    error_message, data = None, None
    try:
        if user_role == 'patient':
            user_profile_details = profile_service.get_user_profile(user_id, user_role)
            data = convert_patient_reponse(user_profile_details)
            status = 200
        elif user_role == 'doctor':
            user_profile_details = profile_service.get_user_profile(user_id, user_role)
            data = convert_doctor_response(user_profile_details)
            status = 200
        elif user_role == 'insurer':
            user_profile_details = profile_service.get_user_profile(user_id, user_role)
            data = convert_insurer_response(user_profile_details)
            status = 200
        else:
            error_message = f'unsupported user_role: {user_role}'
            status = 500
    except Exception as e:
        error_message = f'error while authenticating user {user_id}: {str(e)}'
        logger.error(error_message)
        status = 500

    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

@app.post("/doctor/search", response_model=StandardHttpResponse, tags=['Search Doctor'],
          response_model_exclude_none=True)
def search_doctor(search_by, search_string, covid_support):
    # if user_role not in ['patient', 'doctor', 'insurer']:
    #     status = 400
    #     error_message = f'unsupported role: {user_role}'
    #     return JSONResponse(content=get_http_response(None, status, error_message), status_code=status)

    data, error_message = None, None
    try:
        data = DoctorService.search_doctor(search_by, search_string, covid_support)
        status = 200
    except BaseException as e:
        error_message = f'error while searching doctors: {str(e)}'
        logger.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

@app.get("/insurer/plans", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
         response_model_exclude_none=True)
def get_insurer_plans(insurer_id):
    data, error_message = None, None
    try:
        data = InsurerServices.get_healthcare_plans(insurer_id)
        status = 200
    except BaseException as e:
        error_message = f'error while fetching plans: {str(e)}'
        logger.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

@app.post("/insurer/plans", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
         response_model_exclude_none=True)
def create_insurer_plans(add_plan_request: AddHealthcarePlanRequest):
    data, error_message = None, None
    try:
        plan_id = InsurerServices.create_healthcare_plan(add_plan_request)
        data = AddHealthcarePlanResponse(plan_id=plan_id)
        status = 200
    except BaseException as e:
        error_message = f'error while creating plans: {str(e)}'
        logger.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.post("/insurer/plans/update", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
         response_model_exclude_none=True)
def update_insurer_plans(insurer_id, plan_name, update_plan_request: UpdateHealthcarePlanRequest):
    data, error_message = None, None
    try:
        if not InsurerServices.plan_exists(insurer_id, plan_name):
            error_message = f'plan {plan_name} does not exist for insurer {insurer_id}'
            logging.error(error_message)
            raise BaseException(error_message)
        data = InsurerServices.update_healthcare_plan(insurer_id, plan_name, update_plan_request)
        status = 200
    except BaseException as e:
        error_message = f'error while updating plans: {str(e)}'
        logger.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.delete("/insurer/plans", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
         response_model_exclude_none=True)
def delete_insurer_plans(insurer_id, plan_name):
    data, error_message = None, None
    try:
        InsurerServices.delete_healthcare_plan(insurer_id, plan_name)
        data = {'message': f'successfully deleted plan {plan_name} for insurer {insurer_id}'}
        status = 200
    except BaseException as e:
        error_message = f'error while deleting plans: {str(e)}'
        logger.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

@app.get('/sendresetcode', response_model=StandardHttpResponse, tags=['User Registration and Login'])
async def send_reset_code(user_id):
    # query = 
    data, error_message = None, None
    user = UserLoginRepository.get_user_login(user_id)
    email = user.user_name
    try:
        await ResetPasswordServices.generate_reset_password_email(user_id, email)
        data = {'message' : 'Reset code sent to registered email {} successfully'.format(email)}
        status = 200
    except BaseException as e:
        error_message = "Error while sending reset code to {}".format(email) 
        status = 500
    return JSONResponse(content= get_http_response(data, status, error_message), status_code=status)
@app.post('/resetpassword', response_model=StandardHttpResponse, tags=['User Registration and Login'])
def reset_verify_password(user_id, reset_code_details: ResetPasswordRequest):
    data, error_message = None, None
    try:
        data = ResetPasswordServices.verify_update_password(user_id, reset_code_details)
        logger.info("data",data)
        status = 200
    except BaseException as e:
        error_message = f' Error while password reset. Try Again : {str(e)}'
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code = status)