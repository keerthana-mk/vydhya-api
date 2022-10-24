from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config import engine
from models.profiles import UserProfileRequests, SearchDoctorRequest
from models.users import UserRegistration, UserRegistrationResponse, UserLoginRequest
from databases.db_models.base_tables import Base
from services.authentication.default_auth_service import BaseAuthentication
from services.doctor_services import DoctorService
from services.Profile.profiles_services import ProfileServices
from models.commons import convert_patient_reponse, convert_doctor_response, convert_insurer_response, \
    get_http_response, StandardHttpResponse

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
    return {"message": "Hello World"}