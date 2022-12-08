import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, databases
from sqlalchemy.orm import sessionmaker
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from starlette.config import Config
from httpx import AsyncClient, Auth, Client, Request, Response
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import logging
from logging.config import dictConfig
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
# env_path = Path('../') / '.env'
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)
class DatabaseSetting:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD:str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

class OauthSettings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRATION = 10
    if SECRET_KEY is None:
        raise BaseException('Secret Key missing in env')

class GoogleOauthSettings:
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID") or None
    GOOGLE_SECRET = os.getenv("GOOGLE_SECRET") or None
    GOOGLE_OAUTH_STRING = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_SECRET': GOOGLE_SECRET}
    if GOOGLE_CLIENT_ID is None or GOOGLE_SECRET is None:
        raise BaseException('Google credentials missing in env')
######################################OAuth settings##################################
Oauth_settings = OauthSettings()


######################################Google OAuth settings##################################
google_Oauth_settings = GoogleOauthSettings()
g_config = Config(environ=google_Oauth_settings.GOOGLE_OAUTH_STRING)
goauth = OAuth(g_config)
goauth.register(name ='google',
                server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
                client_kwargs={'scope': 'openid email profile'})
######################################Frontend##################################

FRONTEND_URL = os.environ.get('FRONTEND_URL') or 'http://127.0.0.1:7000/token'
######################################Database settings##################################

DBsettings = DatabaseSetting()
SQLALCHEMY_DATABASE_URL = DBsettings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_actual():
    db = SessionLocal()
    return db

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def check_db_connected():
    try:
        if not str(SQLALCHEMY_DATABASE_URL).__contains__('postgressql'):
            database = databases.Database(SQLALCHEMY_DATABASE_URL)
            if not database.is_connected:
                await database.connect()
                await database.execute("SELECT 1")
        print("Database is connected (^_^)")
    except Exception as e:
        print("Looks like there is some problem in connection,see below traceback")
        raise e
    
######################################Email settings##################################
class EmailSettings:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')

emailsettings = EmailSettings()
mail_config = ConnectionConfig(
    MAIL_USERNAME=emailsettings.MAIL_USERNAME,
    MAIL_PASSWORD=emailsettings.MAIL_PASSWORD,
    MAIL_FROM=emailsettings.MAIL_FROM,
    MAIL_PORT=emailsettings.MAIL_PORT,
    MAIL_SERVER=emailsettings.MAIL_SERVER,
    MAIL_FROM_NAME=emailsettings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    # SUPPRESS_SEND = 0,
    TEMPLATE_FOLDER='./templates'
)
