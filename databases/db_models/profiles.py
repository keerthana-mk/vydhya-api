from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY


from databases.base_class import Base
from databases.db_models.users import UserLogin


# class ListDetails:
#     list_details = []

class PatientProfile(Base):
    user_id = Column(String, primary_key=True, index=True)
    user_name = Column(String, default = UserLogin.first_name+" "+UserLogin.last_name, nullable=False)
    gender = Column(String, nullable=False)
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
    user_id = Column(String, primary_key=True, index=True)
    user_name = Column(String, default = UserLogin.first_name+" "+UserLogin.last_name, nullable=False)
    experience = Column(Integer, nullable=False)
    hospital_name = Column(String)
    speciality = Column(String)
    is_hosp_covid_supported = Column(Boolean, default=False)
    num_covid_beds_available = Column(Integer, default=0)
    insurance_accepted = Column(Boolean)

class InsurerProfile(Base):
    insurer_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey(UserLogin.user_id))
    insurance_name = Column(String)
    plan_id = Column(String)




