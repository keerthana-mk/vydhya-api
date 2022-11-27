from dataclasses import dataclass
from datetime import datetime
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import engine
from models.appointments import Appointments, CovidQuestionnaire, DeleteAppointment, UpdateAppointment
from models.profiles import UserProfileRequests, SearchDoctorRequest
from models.users import ResetPassword, ResetPasswordResponse, UserRegistration, UserRegistrationResponse, UserLoginRequest
from databases.db_models.base_tables import Base
from services.appointments_services import ManageAppointments
from services.authentication.default_auth_service import BaseAuthentication
from services.doctor_services import DoctorService
from services.Profile.profiles_services import ProfileServices
from models.commons import convert_patient_reponse, convert_doctor_response, convert_insurer_response, \
    get_http_response, StandardHttpResponse
# from models.schemas.logging import logger
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
logger.addHandler(fh)  # Exporting logs to a file


def create_tables():  # new
    logger.error("Creating tables...")
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title="Vydhya", version="v1")
    # create_tables()
    return app


# logger.info('****************** Starting Server *****************')

app = start_application()

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
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
          response_model_exclude_none=True)
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
def search_doctor(search_doctor_request: SearchDoctorRequest):
    # if user_role not in ['patient', 'doctor', 'insurer']:
    #     status = 400
    #     error_message = f'unsupported role: {user_role}'
    #     return JSONResponse(content=get_http_response(None, status, error_message), status_code=status)

    data, error_message = None, None
    try:
        data = DoctorService.search_doctor(search_doctor_request.search_by, search_doctor_request.search_string,
                                           search_doctor_request.covid_support)
        status = 200
    except BaseException as e:
        error_message = f'error while searching doctors: {str(e)}'
        logger.error(error_message)
        status = 500
    except BaseException as e:
        error_message = f'error while searching doctors: {str(e)}'
        logger.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

# @app.post("/reset_password", response_model=StandardHttpResponse, tags="Reset Password")
# def update_password(user_password: ResetPassword):
#     auth_service= BaseAuthentication.get_auth_service()
#     data, error_message = None, None
#     try:
#         data=auth_service.reset_password(user_password)
#         logger.info(data)
#         status=200

#     except BaseException as e:
#         error_message = f'Unable to Update Password: {str(e)}'
#         logger.error(error_message)
#         status = 500
        
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.post("/add_appointment", response_model=StandardHttpResponse, tags=['Doctor Appointments'])
def add_appointment(new_appointment: Appointments):
    logger.error("Creating Appointment...")
    data, error_message= None, None
    try:
        data=ManageAppointments.add_appointment(new_appointment.appointement_id,
        new_appointment.doctor_id,
        new_appointment.patient_id,
        new_appointment.appointment_start_time,
        new_appointment.duration,
        new_appointment.feedback,
        new_appointment.rating,
        new_appointment.appointment_attended)
        logger.error("Creating Appointment-1...")
        status=200
    except BaseException as e:
            error_message = f'Failed to Add Appointment {str(e)}'
            logger.error(error_message)
            status= 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.post("/update_appointment", response_model=StandardHttpResponse, tags=['Doctor Appointments'])
def update_appointment(new_appointment: UpdateAppointment):
    data, error_message= None, None
    try:
        data=ManageAppointments.update_appointment(
            new_appointment.doctor_id,
            new_appointment.patient_id,
            new_appointment.old_time,
            new_appointment.new_time)
        status=200
    except BaseException as e:
            error_message = f'Failed to Update Appointment {str(e)}'
            logger.error(error_message)
            status= 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.delete("/delete_appointment", response_model=StandardHttpResponse, tags=['Doctor Appointments'])
def update_appointment(new_appointment: DeleteAppointment):
    data, error_message= None, None
    try:
        data=ManageAppointments.delete_appointment(
            new_appointment.doctor_id,
            new_appointment.patient_id,
            new_appointment.appointment_time)
        status=200
    except BaseException as e:
            error_message = f'Failed to Update Appointment {str(e)}'
            logger.error(error_message)
            status= 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.post("/covid_questionnaire", response_model= StandardHttpResponse, tags=["Covid Questionnaire"])
def add_covid_questionnaire(covid_details: CovidQuestionnaire):
    data, error_message=None, None
    time1=str(datetime.now())
    covid_details.updated_at=time1
    try:
        data=ManageAppointments.add_covid_questionnaire(
            covid_details.user_id,
            covid_details.name,
            covid_details.email,
            covid_details.age,
            covid_details.has_cold,
            covid_details.has_fever,
            covid_details.has_cough,
            covid_details.has_weakness,
            covid_details.has_sour_throat,
            covid_details.has_body_pains,
            covid_details.other_symptoms,
            covid_details.covid_test,
            covid_details.updated_at
        )
        status=200

    except BaseException as e:
        error_message=f'Failed to add covid questionnaire {str(e)}'
        status=500
    
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.get("/get_covid_details", response_model=StandardHttpResponse, tags=["Covid Questionnaire"])
def get_covid_details(user_id):
    data, error_message=None, None
    try:
        data=ManageAppointments.get_covid_details(user_id)
        status=200

    except BaseException as e:
        error_message=f'Failed to get covid details {str(e)}'
        status=500

    return JSONResponse(content=get_http_response(data,status, error_message), status_code=status)
