import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, databases
from sqlalchemy.orm import sessionmaker

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class DatabaseSetting:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = DatabaseSetting()
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
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
