from dataclasses import dataclass
from datetime import datetime, timedelta
from starlette.requests import Request
import uvicorn
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.config import engine, get_db
from databases.repository.users import UserLoginRepository, UserProfileRepository
from databases.repository.profiles import PatientProfileRepository
from databases.repository.feedback_repo import AppointmentFeedbackRepository
from databases.repository.appointments import AppointmentsRepository
from models.healthcare_plans import AddHealthcarePlanRequest, AddHealthcarePlanResponse, UpdateHealthcarePlanRequest
from models.appointments import Appointments, CovidQuestionnaire, DeleteAppointment, Schedule, UpdateAppointment, \
    CovidTestScheduleRequest
from models.profiles import UserProfileRequests, SearchDoctorRequest
from models.users import ResetPassword, ResetPasswordResponse, UserRegistration, UserRegistrationResponse, \
    UserLoginRequest, ResetPasswordRequest, Token, TokenData
from models.feedback import FeedbackRequest
from databases.db_models.base_tables import Base
from services.appointments_services import ManageAppointments
from services.authentication.default_auth_service import BaseAuthentication
from services.doctor_services import DoctorService
from services.insurer_services import InsurerServices
from services.profiles_services import ProfileServices
from services.authentication.reset_password_service import ResetPasswordServices
from services.authentication.OAuth_service import create_access_token
from models.commons import convert_patient_reponse, convert_doctor_response, convert_insurer_response, \
    get_http_response, StandardHttpResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config import Oauth_settings
from jose import jwt, JWTError
import logging
import base64


# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# ch = logging.StreamHandler()
# # fh = logging.FileHandler(filename='./server.log')
# formatter = logging.Formatter(
#     "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
#     )
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# logger.addHandler(ch)  # Exporting logs to the screen
# logger.addHandler(fh)  # Exporting logs to a file

def create_tables():  # new
    logging.info("Creating tables...")
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Oauth_settings.SECRET_KEY, algorithms=[Oauth_settings.ALGORITHM])
        user_id: str = payload.get("user_id")
        logging.info(f" user_id = {user_id}")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    user = UserLoginRepository.get_user_login(user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


@app.post("/user_registration", response_model=StandardHttpResponse, tags=['User Registration and Login'],
          response_model_exclude_none=True)
def create_user(user_details: UserRegistration):
    auth_service = BaseAuthentication.get_auth_service()
    error_message, data = None, None
    try:
        user_id = auth_service.add_user(user_details)
        data = UserRegistrationResponse(
            message=f'successfully created user {user_id}',
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

# @app.post("/profile", response_model=StandardHttpResponse, tags=['User Profiles'], response_model_exclude_none=True)
# def update_user_profile(user_id, user_role, user_profile: UserProfileRequests):
#     current_logged_user = get_current_user()
#     profile_service = ProfileServices()
#     error_message, data = None, None
#     try:
#         if user_role == 'patient':
#             updated_user_profile = profile_service.update_user_profile(user_id, user_role, user_profile.patient)
#             data = convert_patient_reponse(updated_user_profile)
#             status = 200
#         elif user_role == 'doctor':
#             updated_user_profile = profile_service.update_user_profile(user_id, user_role, user_profile.doctor)
#             data = convert_doctor_response(updated_user_profile)
#             status = 200
#         elif user_role == 'insurer':
#             updated_user_profile = profile_service.update_user_profile(user_id, user_role, user_profile.insurer)
#             data = convert_insurer_response(updated_user_profile)
#             status = 200
#         else:
#             error_message = f'unsupported user_role: {user_role}'
#             status = 500
#     except Exception as e:
#         error_message = f'error while authenticating user {user_id}: {str(e)}'
#         status = 500
#     return JSONResponse(get_http_response(data, status, error_message), status_code=status)
@app.post("/profile", response_model=StandardHttpResponse, tags=['User Profiles'], response_model_exclude_none=True)
def update_user_profile(user_profile: UserProfileRequests, request: Request, current_user=Depends(get_current_user)):
    print('current_user: ', current_user)
    profile_service = ProfileServices()
    error_message, data = None, None
    try:
        if current_user.user_role == 'patient':
            updated_user_profile = profile_service.update_user_profile(current_user.user_id, current_user.user_role,
                                                                       user_profile.patient)
            data = convert_patient_reponse(updated_user_profile)
            status = 200
        elif current_user.user_role == 'doctor':
            updated_user_profile = profile_service.update_user_profile(current_user.user_id, current_user.user_role,
                                                                       user_profile.doctor)
            data = convert_doctor_response(updated_user_profile)
            status = 200
        elif current_user.user_role == 'insurer':
            updated_user_profile = profile_service.update_user_profile(current_user.user_id, current_user.user_role,
                                                                       user_profile.insurer)
            data = convert_insurer_response(updated_user_profile)
            status = 200
        else:
            error_message = f'unsupported user_role: {current_user.user_role}'
            status = 500
    except Exception as e:
        error_message = f'error while authenticating user {current_user.user_id}: {str(e)}'
        status = 500
    return JSONResponse(get_http_response(data, status, error_message), status_code=status)


# @app.get("/profile", response_model=StandardHttpResponse, tags=['User Profiles'], response_model_exclude_none=True)
# def get_user_profiles(user_id, user_role):
#     logging.info("please tell me i am here")
#     profile_service = ProfileServices()
#     error_message, data = None, None
#     try:
#         if user_role == 'patient':
#             user_profile_details = profile_service.get_user_profile(user_id, user_role)
#             data = convert_patient_reponse(user_profile_details)
#             status = 200
#         elif user_role == 'doctor':
#             user_profile_details = profile_service.get_user_profile(user_id, user_role)
#             data = convert_doctor_response(user_profile_details)
#             status = 200
#         elif user_role == 'insurer':
#             user_profile_details = profile_service.get_user_profile(user_id, user_role)
#             data = convert_insurer_response(user_profile_details)
#             status = 200
#         else:
#             error_message = f'unsupported user_role: {user_role}'
#             status = 500
#     except Exception as e:
#         error_message = f'error while authenticating user {user_id}: {str(e)}'
#         logging.error(error_message)
#         status = 500

#     return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)
@app.get("/profile", response_model=StandardHttpResponse, tags=['User Profiles'], response_model_exclude_none=True)
def get_user_profiles(request: Request, current_user=Depends(get_current_user)):
    logging.info(f" user_id = {current_user.user_id}")
    profile_service = ProfileServices()
    error_message, data = None, None
    try:
        if current_user.user_role == 'patient':
            user_profile_details = profile_service.get_user_profile(current_user.user_id, current_user.user_role)
            data = convert_patient_reponse(user_profile_details)
            status = 200
        elif current_user.user_role == 'doctor':
            user_profile_details = profile_service.get_user_profile(current_user.user_id, current_user.user_role)
            data = convert_doctor_response(user_profile_details)
            status = 200
        elif current_user.user_role == 'insurer':
            logging.info(f'current_user role in insurance profile :{current_user.user_role}')
            user_profile_details = profile_service.get_user_profile(current_user.user_id, current_user.user_role)
            data = convert_insurer_response(user_profile_details)
            status = 200
        else:
            error_message = f'unsupported user_role: {current_user.user_role}'
            status = 500
    except Exception as e:
        logging.info(f"I am throwing error from here")
        error_message = f'error while authenticating user {current_user.user_id}: {str(e)}'
        logging.error(error_message)
        status = 500

    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.post("/doctor/search", response_model=StandardHttpResponse, tags=['Search Doctor'],
          response_model_exclude_none=True)
def search_doctor(search_by, search_string, covid_support: bool, request: Request,
                  current_user=Depends(get_current_user)):
    # if user_role not in ['patient', 'doctor', 'insurer']:
    #     status = 400
    #     error_message = f'unsupported role: {user_role}'
    #     return JSONResponse(content=get_http_response(None, status, error_message), status_code=status)

    data, error_message = None, None
    try:
        data = DoctorService.search_doctor(search_by, search_string, covid_support)
        print(f'data in doctor search ={data}')
        status = 200
    except BaseException as e:
        error_message = f'error while searching doctors: {str(e)}'
        logging.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.get("/insurer/plans", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
#          response_model_exclude_none=True)
# def get_insurer_plans(insurer_id):
#     data, error_message = None, None
#     try:
#         data = InsurerServices.get_healthcare_plans(insurer_id)
#         status = 200
#     except BaseException as e:
#         error_message = f'error while fetching plans: {str(e)}'
#         logging.error(error_message)
#         status = 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

@app.get("/insurer/plans", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
         response_model_exclude_none=True)
def get_insurer_plans(request: Request, current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        data = InsurerServices.get_healthcare_plans(current_user.user_id)
        status = 200
    except BaseException as e:
        error_message = f'error while fetching plans: {str(e)}'
        logging.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.get("/insurer/all_plans", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
#          response_model_exclude_none=True)
# def get_all_insurer_plans():
#     data, error_message = None, None
#     try:
#         data = InsurerServices.get_all_healthcare_plans()
#         status = 200
#     except BaseException as e:
#         error_message = f'error while fetching plans: {str(e)}'
#         logging.error(error_message)
#         status = 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)
@app.get("/insurer/all_plans", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
         response_model_exclude_none=True)
def get_all_insurer_plans(request: Request, current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        data = InsurerServices.get_all_healthcare_plans()
        status = 200
    except BaseException as e:
        error_message = f'error while fetching plans: {str(e)}'
        logging.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.post("/insurer/plans", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
#          response_model_exclude_none=True)
# def create_insurer_plans(add_plan_request: AddHealthcarePlanRequest):
#     data, error_message = None, None
#     try:
#         plan_id = InsurerServices.create_healthcare_plan(add_plan_request)
#         data = AddHealthcarePlanResponse(plan_id=plan_id)
#         status = 200
#     except BaseException as e:
#         error_message = f'error while creating plans: {str(e)}'
#         logging.error(error_message)
#         status = 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

@app.post("/insurer/plans", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
          response_model_exclude_none=True)
def create_insurer_plans(add_plan_request: AddHealthcarePlanRequest, request: Request,
                         current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        logging.info("add request_plan: ".format(add_plan_request))
        plan_id = InsurerServices.create_healthcare_plan(current_user.user_id, add_plan_request)
        data = AddHealthcarePlanResponse(plan_id=plan_id)
        status = 200
    except BaseException as e:
        error_message = f'error while creating plans: {str(e)}'
        logging.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.post("/insurer/plans/update", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
#          response_model_exclude_none=True)
# def update_insurer_plans(insurer_id, plan_name, update_plan_request: UpdateHealthcarePlanRequest):
#     data, error_message = None, None
#     try:
#         if not InsurerServices.plan_exists(insurer_id, plan_name):
#             error_message = f'plan {plan_name} does not exist for insurer {insurer_id}'
#             logging.error(error_message)
#             raise BaseException(error_message)
#         data = InsurerServices.update_healthcare_plan(insurer_id, plan_name, update_plan_request)
#         status = 200
#     except BaseException as e:
#         error_message = f'error while updating plans: {str(e)}'
#         logging.error(error_message)
#         status = 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

# @app.post("/insurer/plans/update", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
#          response_model_exclude_none=True)
# def update_insurer_plans(insurer_id, plan_name, update_plan_request: UpdateHealthcarePlanRequest):
#     data, error_message = None, None
#     try:
#         if not InsurerServices.plan_exists(insurer_id, plan_name):
#             error_message = f'plan {plan_name} does not exist for insurer {insurer_id}'
#             logging.error(error_message)
#             raise BaseException(error_message)
#         data = InsurerServices.update_healthcare_plan(insurer_id, plan_name, update_plan_request)
#         status = 200
#     except BaseException as e:
#         error_message = f'error while updating plans: {str(e)}'
#         logging.error(error_message)
#         status = 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

@app.post("/insurer/plans/update", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
          response_model_exclude_none=True)
def update_insurer_plans(plan_name, update_plan_request: UpdateHealthcarePlanRequest, request: Request,
                         current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        if not InsurerServices.plan_exists(current_user.user_id, plan_name):
            error_message = f'plan {plan_name} does not exist for insurer {current_user.user_id}'
            logging.error(error_message)
            raise BaseException(error_message)
        data = InsurerServices.update_healthcare_plan(current_user.user_id, plan_name, update_plan_request)
        status = 200
    except BaseException as e:
        error_message = f'error while updating plans: {str(e)}'
        logging.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.delete("/insurer/plans", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
#          response_model_exclude_none=True)
# def delete_insurer_plans(insurer_id, plan_name):
#     data, error_message = None, None
#     try:
#         InsurerServices.delete_healthcare_plan(insurer_id, plan_name)
#         data = {'message': f'successfully deleted plan {plan_name} for insurer {insurer_id}'}
#         status = 200
#     except BaseException as e:
#         error_message = f'error while deleting plans: {str(e)}'
#         logging.error(error_message)
#         status = 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

@app.delete("/insurer/plans", response_model=StandardHttpResponse, tags=['Insurer Health Plans'],
            response_model_exclude_none=True)
def delete_insurer_plans(plan_name, request: Request, current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        InsurerServices.delete_healthcare_plan(current_user.user_id, plan_name)
        data = {'message': f'successfully deleted plan {plan_name} for insurer {current_user.user_id}'}
        status = 200
    except BaseException as e:
        error_message = f'error while deleting plans: {str(e)}'
        logging.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.get('/sendresetcode', response_model=StandardHttpResponse, tags=['User Registration and Login'])
# async def send_reset_code(user_id):
#     # query = 
#     data, error_message = None, None
#     user = UserLoginRepository.get_user_login(user_id)
#     email = user.user_name
#     try:
#         await ResetPasswordServices.generate_reset_password_email(user_id, email)
#         data = {'message' : 'Reset code sent to registered email {} successfully'.format(email)}
#         status = 200
#     except BaseException as e:
#         error_message = "Error while sending reset code to {}".format(email) 
#         status = 500
#     return JSONResponse(content= get_http_response(data, status, error_message), status_code=status)

@app.get('/sendresetcode', response_model=StandardHttpResponse, tags=['User Registration and Login'])
async def send_reset_code(user_id):
    # query = 
    data, error_message = None, None
    user = UserLoginRepository.get_user_login(user_id)
    email = user.user_name
    try:
        await ResetPasswordServices.generate_reset_password_email(user_id, email)
        data = {'message': 'Reset code sent to registered email {} successfully'.format(email)}
        status = 200
    except BaseException as e:
        error_message = "Error while sending reset code to {}".format(email)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.post('/resetpassword', response_model=StandardHttpResponse, tags=['User Registration and Login'])
# def reset_verify_password(user_id, reset_code_details: ResetPasswordRequest):
#     data, error_message = None, None
#     try:
#         data = ResetPasswordServices.verify_update_password(user_id, reset_code_details)
#         status = 200
#     except BaseException as e:
#         error_message = f' Error while password reset. Try Again : {str(e)}'
#         status = 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code = status)

@app.post('/resetpassword', response_model=StandardHttpResponse, tags=['User Registration and Login'])
def reset_verify_password(user_id, reset_code_details: ResetPasswordRequest):
    data, error_message = None, None
    try:
        data = ResetPasswordServices.verify_update_password(user_id, reset_code_details)
        status = 200
    except BaseException as e:
        error_message = f' Error while password reset. Try Again : {str(e)}'
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.post('/upload/profilepic',response_model=StandardHttpResponse, tags=['User Profiles'])
# def upload_profile_pic(user_id, file:UploadFile = File(...)):
#     data, error_message = None, None
#     try:
#         contents = file.file.read()
#         with open(f"profileimages\\{user_id}_"+file.filename,"wb") as f:
#             f.write(contents)
#         base64_encoded_image = base64.b64encode(contents).decode("utf-8")
#         UserProfileRepository.store_profile_pic_database(user_id, base64_encoded_image)
#         status = 200
#         data = {"message":f"profile picture uploaded successfully for user = {user_id}"}
#     except Exception as e:
#         error_message = f'Error while uploading profile pic = {str(e)}'
#         status = 500

#     finally:
#         file.file.close()
# return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

@app.post('/upload/profilepic', response_model=StandardHttpResponse, tags=['User Profiles'])
def upload_profile_pic(request: Request, current_user=Depends(get_current_user), file: UploadFile = File(...)):
    data, error_message = None, None
    try:
        contents = file.file.read()
        with open(f"profileimages\\{current_user.user_id}_" + file.filename, "wb") as f:
            f.write(contents)
        base64_encoded_image = base64.b64encode(contents).decode("utf-8")
        UserProfileRepository.store_profile_pic_database(current_user.user_id, base64_encoded_image)
        status = 200
        data = {"message": f"profile picture uploaded successfully for user = {current_user.user_id}"}
    except Exception as e:
        error_message = f'Error while uploading profile pic = {str(e)}'
        status = 500

    finally:
        file.file.close()
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.get('/profilepic', tags=['User Profiles'])
# def fetch_profile_pic(user_id):
#     # base64_encode_data 
#     result = UserProfileRepository.fetch_profile_image(user_id)
#     return result
@app.get('/profilepic', tags=['User Profiles'])
def fetch_profile_pic(request: Request, current_user=Depends(get_current_user)):
    # base64_encode_data 
    result = UserProfileRepository.fetch_profile_image(current_user.user_id)
    return result


# @app.post('/addFeedback', response_model=StandardHttpResponse, tags=['General Doctor Feedback'])
# def add_doctor_feedback(doctor_id: str, patient_id: str, feedback_request: FeedbackRequest):
#     data, error_message = None, None
#     try:
#         data = AppointmentFeedbackRepository.create_feedback(doctor_id, patient_id, feedback_request)
#         status = 200
#     except BaseException as e:
#         error_message = f' Error while adding Feedback : {str(e)}'
#         status = 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code = status)

@app.post('/addFeedback', response_model=StandardHttpResponse, tags=['General Doctor Feedback'])
def add_doctor_feedback(doctor_id: str, feedback_request: FeedbackRequest, request: Request,
                        current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        data = AppointmentFeedbackRepository.create_feedback(doctor_id, current_user.user_id, feedback_request)
        status = 200
    except BaseException as e:
        error_message = f' Error while adding Feedback : {str(e)}'
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.get("/get_feedback_by_doctor", response_model=StandardHttpResponse, tags=['General Doctor Feedback'])
# def get_feedbacks_by_doctor(doctor_id):
#     data, error_message = None, None
#     try:
#         data = AppointmentFeedbackRepository.fetch_feedback_by_doctor(doctor_id)
#         status = 200
#     except BaseException as e:
#         error_message = f' Error while fetching Feedback for doctor {doctor_id} : {str(e)}'
#         status = 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code = status)

@app.get("/get_feedback_by_doctor", response_model=StandardHttpResponse, tags=['General Doctor Feedback'])
def get_feedbacks_by_doctor(doctor_id, request: Request, current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        data = AppointmentFeedbackRepository.fetch_feedback_by_doctor(doctor_id)
        status = 200
    except BaseException as e:
        error_message = f' Error while fetching Feedback for doctor {doctor_id} : {str(e)}'
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.post("/add_appointment", response_model=StandardHttpResponse, tags=['Doctor Appointments'])
# def add_appointment(new_appointment: Appointments):
#     logging.error("Creating Appointment...")
#     data, error_message= None, None
#     try:
#         data=ManageAppointments.add_appointment(new_appointment.appointment_id,
#         new_appointment.doctor_id,
#         new_appointment.patient_id,
#         new_appointment.appointment_start_time,
#         new_appointment.duration,
#         new_appointment.feedback,
#         new_appointment.rating,
#         new_appointment.appointment_attended)
#         logging.error("Creating Appointment-1...")
#         status=200
#     except BaseException as e:
#             error_message = f'Failed to Add Appointment {str(e)}'
#             logging.error(error_message)
#             status= 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

@app.post("/add_appointment", response_model=StandardHttpResponse, tags=['Doctor Appointments'])
def add_appointment(new_appointment: Appointments, request: Request, current_user=Depends(get_current_user)):
    logging.info("Creating Appointment...")
    data, error_message = None, None
    try:
        data = ManageAppointments.add_appointment(new_appointment.appointment_id,
                                                  new_appointment.doctor_id,
                                                  current_user.user_id,
                                                  new_appointment.appointment_start_time,
                                                  new_appointment.duration,
                                                  new_appointment.feedback,
                                                  new_appointment.rating,
                                                  False)
        logging.error("Creating Appointment-1...")
        status = 200
    except BaseException as e:
        error_message = f'Failed to Add Appointment {str(e)}'
        logging.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.post("/update_appointment", response_model=StandardHttpResponse, tags=['Doctor Appointments'])
# def update_appointment(new_appointment: UpdateAppointment):
#     data, error_message= None, None
#     try:
#         data=ManageAppointments.update_appointment(
#             new_appointment.doctor_id,
#             new_appointment.patient_id,
#             new_appointment.old_time,
#             new_appointment.new_time)
#         status=200
#     except BaseException as e:
#             error_message = f'Failed to Update Appointment {str(e)}'
#             logging.error(error_message)
#             status= 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.post("/update_appointment", response_model=StandardHttpResponse, tags=['Doctor Appointments'])
def update_appointment(new_appointment: UpdateAppointment, request: Request, current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        data = ManageAppointments.update_appointment(
            new_appointment.doctor_id,
            current_user.user_id,
            new_appointment.old_time,
            new_appointment.new_time)
        status = 200
    except BaseException as e:
        error_message = f'Failed to Update Appointment {str(e)}'
        logging.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.delete("/delete_appointment", response_model=StandardHttpResponse, tags=['Doctor Appointments'])
# def update_appointment(new_appointment: DeleteAppointment):
#     data, error_message= None, None
#     try:
#         data=ManageAppointments.delete_appointment(
#             new_appointment.doctor_id,
#             new_appointment.patient_id,
#             new_appointment.appointment_time)
#         status=200
#     except BaseException as e:
#             error_message = f'Failed to Update Appointment {str(e)}'
#             logging.error(error_message)
#             status= 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

@app.delete("/delete_appointment", response_model=StandardHttpResponse, tags=['Doctor Appointments'])
def delete_appointment(new_appointment: DeleteAppointment, request: Request, current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        data = ManageAppointments.delete_appointment(
            new_appointment.doctor_id,
            current_user.user_id,
            new_appointment.appointment_time)
        status = 200
    except BaseException as e:
        error_message = f'Failed to delete Appointment {str(e)}'
        logging.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.post("/update_feedback_by_appointment", response_model=StandardHttpResponse, tags=['Doctor Appointments'])
# def update_feedback_by_appointment(appoinment_id, feedback_response: FeedbackRequest):
#     data, error_message = None, None
#     try:
#         logging.info("from main:", feedback_response)
#         data = AppointmentsRepository.add_feedback_by_appointment(appoinment_id,feedback_response)
#         status = 200
#     except BaseException as e:
#         error_message = f' Error while adding feedback for appointment on {appoinment_id} : {str(e)}'
#         status = 500
#     return JSONResponse(content=get_http_response(data, status, error_message), status_code = status)

@app.post("/update_feedback_by_appointment", response_model=StandardHttpResponse, tags=['Doctor Appointments'])
def update_feedback_by_appointment(appoinment_id, feedback_response: FeedbackRequest, request: Request,
                                   current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        data = AppointmentsRepository.add_feedback_by_appointment(appoinment_id, feedback_response)
        status = 200
    except BaseException as e:
        error_message = f' Error while adding feedback for appointment on {appoinment_id} : {str(e)}'
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.post("/covid_questionnaire", response_model= StandardHttpResponse, tags=["Covid Questionnaire"])
# def add_covid_questionnaire(covid_details: CovidQuestionnaire):
#     data, error_message=None, None
#     time1=str(datetime.now())
#     covid_details.updated_at=time1
#     try:
#         data=ManageAppointments.add_covid_questionnaire(
#             covid_details.user_id,
#             covid_details.name,
#             covid_details.email,
#             covid_details.age,
#             covid_details.has_cold,
#             covid_details.has_fever,
#             covid_details.has_cough,
#             covid_details.has_weakness,
#             covid_details.has_sour_throat,
#             covid_details.has_body_pains,
#             covid_details.other_symptoms,
#             covid_details.covid_test,
#             covid_details.updated_at
#         )
#         status=200

#     except BaseException as e:
#         error_message=f'Failed to add covid questionnaire {str(e)}'
#         status=500

#     return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)

@app.post("/covid_questionnaire", response_model=StandardHttpResponse, tags=["Covid Questionnaire"])
def add_covid_questionnaire(covid_details: CovidQuestionnaire, request: Request,
                            current_user=Depends(get_current_user)):
    data, error_message = None, None
    time1 = str(datetime.now())
    covid_details.updated_at = time1
    try:
        data = ManageAppointments.add_covid_questionnaire(
            current_user.user_id,
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
        status = 200

    except BaseException as e:
        error_message = f'Failed to add covid questionnaire {str(e)}'
        status = 500

    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.get("/get_covid_details", response_model=StandardHttpResponse, tags=["Covid Questionnaire"])
# def get_covid_details(user_id):
#     data, error_message=None, None
#     try:
#         data=ManageAppointments.get_covid_details(user_id)
#         status=200

#     except BaseException as e:
#         error_message=f'Failed to get covid details {str(e)}'
#         status=500

#     return JSONResponse(content=get_http_response(data,status, error_message), status_code=status)

@app.get("/get_covid_details", response_model=StandardHttpResponse, tags=["Covid Questionnaire"])
def get_covid_details(request: Request, current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        data = ManageAppointments.get_covid_details(current_user.user_id)
        status = 200

    except BaseException as e:
        error_message = f'Failed to get covid details {str(e)}'
        status = 500

    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.post('/schedule_covid_test', response_model=StandardHttpResponse, tags=["Covid Questionnaire"])
def schedule_covid_test(new_appointment: CovidTestScheduleRequest, request: Request,
                        current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        data = ManageAppointments.add_covid_appointment("covid_test",
                                                        "Covid test Lab",
                                                        current_user.user_id,
                                                        new_appointment.appointment_start_time,
                                                        new_appointment.duration,
                                                        False)
        logging.error("Creating Appointment-1...")
        status = 200
    except BaseException as e:
        error_message = f'Failed to Add Appointment {str(e)}'
        logging.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.get('/get_covid_test', response_model=StandardHttpResponse, tags=["Covid Questionnaire"])
def get_covid_test(request: Request, current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        data = AppointmentsRepository.get_covid_tests(current_user.user_id)
        print(f"get covid test : {data}")
        status = 200
    except BaseException as e:
        error_message = f'Failed to get covid tests:{str(e)}'
        logging.error(error_message)
        status = 500
    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


# @app.post('/enroll_health_plan', response_model=StandardHttpResponse, tags=['Enroll in Healthcare Plans'])
# def enroll_healthcare_plan(patient_id, plan_id):
#     data, error_message=None, None
#     try:
#         data= PatientProfileRepository.enroll_in_healthcare_plan(patient_id, plan_id)
#         status=200

#     except BaseException as e:
#         error_message=f'Failed to enroll healthcare plan: {str(e)}'
#         status=500

#     return JSONResponse(content=get_http_response(data,status, error_message), status_code=status)

@app.post('/enroll_health_plan', response_model=StandardHttpResponse, tags=['Enroll in Healthcare Plans'])
def enroll_healthcare_plan(plan_id, request: Request, current_user=Depends(get_current_user)):
    data, error_message = None, None
    try:
        data = PatientProfileRepository.enroll_in_healthcare_plan(current_user.user_id, plan_id)
        status = 200

    except BaseException as e:
        error_message = f'Failed to enroll healthcare plan: {str(e)}'
        status = 500

    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    auth_service = BaseAuthentication.get_auth_service()
    logging.info('am i coming here????')
    user = auth_service.verify_user(form_data.username, form_data.password)
    logging.info(f'user.user_id: {user.user_id}')
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = Oauth_settings.ACCESS_TOKEN_EXPIRATION
    details = {}
    details['user_id'] = user.user_id
    access_token = create_access_token(data=details, expires=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/get_schedule", response_model=StandardHttpResponse, tags=["Get Doctor Schedule"])
def get_schedule(request: Request, current_user=Depends(get_current_user)):
    data, error_message = None, None

    try:
        data = ManageAppointments.get_schedule(current_user.user_id)
        status = 200

    except BaseException as e:
        error_message = f'Failed to get Doctor Schedule {str(e)}'
        status = 500

    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.post("/add_schedule", response_model=StandardHttpResponse, tags=["Add Doctor Schedule"])
def add_schedule(new_schedule: Schedule, request: Request, current_user=Depends(get_current_user)):
    data, error_message = None, None

    try:
        data = ManageAppointments.add_schedule(current_user.user_id,
                                               new_schedule.schedule_start_date_time,
                                               new_schedule.schedule_end_date_time,
                                               new_schedule.is_available)
        status = 200

    except BaseException as e:
        error_message = f'Failed to get Doctor Schedule {str(e)}'
        status = 500

    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)


@app.get("/get_appointments", response_model=StandardHttpResponse, tags=["Add Doctor Schedule"])
def get_appointments(request: Request, current_user=Depends(get_current_user)):
    data, error_message = None, None

    try:
        data = ManageAppointments.get_upcoming_appointments(current_user.user_id)
        status = 200

    except BaseException as e:
        error_message = f'Failed to get Doctor Schedule {str(e)}'
        status = 500

    return JSONResponse(content=get_http_response(data, status, error_message), status_code=status)
