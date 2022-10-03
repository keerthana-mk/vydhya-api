from databases.db_models.base_tables import Base
from fastapi import FastAPI, Depends
from databases.db_connection import engine, get_db, SessionLocal, check_db_connected
from data_models.Schemas.Users import UsersRegistration
from data_models.Schemas.commons import DateTimeModel
from sqlalchemy.orm import Session
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
    return check_db_connected()
    return {"message": "Hello World"}


@app.post("/user_registration", response_model = UsersRegistration, tags='User Registration and Login')
def create_user(user : UsersRegistration,datetimeobj: DateTimeModel,db: Session = Depends(get_db)):
    user = create_new_user(user=user,datetimeobj=datetimeobj,db=db)
    return user