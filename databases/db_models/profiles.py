from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT

from databases.base_class import Base
from databases.db_models.users import UserLogin


class PatientProfile(Base):
    user_id = Column(String, primary_key=True, foreign_key=ForeignKey(UserLogin.user_id), index=True)
    # full_name = Column(String, default = UserLogin.first_name+" "+UserLogin.last_name, nullable=False)
    full_name = Column(String, nullable=True)
    contact_email = Column(String)
    theme = Column(String, default='primary')
    gender = Column(String)
    dob = Column(String)
    height = Column(String)
    weight = Column(String)
    vaccinations = Column(ARRAY(String))
    blood_type = Column(String)
    allergies = Column(ARRAY(String))
    medications = Column(ARRAY(String))
    blood_pressure = Column(String)
    preexist_conditions = Column(ARRAY(String))
    health_plan_id = Column(String)
    monthly_medical_expense = Column(String)


class DoctorProfile(Base):
    user_id = Column(String, primary_key=True, foreign_key=ForeignKey(UserLogin.user_id), index=True)
    full_name = Column(String, nullable=True)
    contact_email = Column(String)
    contact_phone = Column(String)
    theme = Column(String, default='primary')
    gender = Column(String)
    dob = Column(String)
    experience = Column(FLOAT, default=0, nullable=False)
    hospital_name = Column(String)
    hospital_address = Column(String)
    speciality = Column(String)
    is_hosp_covid_supported = Column(Integer, default=0)
    num_covid_beds_available = Column(Integer, default=0)
    insurance_accepted = Column(Integer, default=0)


class InsurerProfile(Base):
    user_id = Column(String, primary_key=True, foreign_key=ForeignKey(UserLogin.user_id))
    insurer_name = Column(String)
    contact_email = Column(String)
    theme = Column(String, default='primary')

