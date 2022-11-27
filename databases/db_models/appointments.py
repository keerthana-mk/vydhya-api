# from datetime import datetime
from email.policy import default
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT
from databases.base_class import Base
from databases.db_models.profiles import DoctorProfile, PatientProfile

class Appointments(Base): #Add appointment ID.
    appointment_id=Column(String, primary_key=True)
    doctor_id=Column(String, foreign_key=ForeignKey(DoctorProfile.user_id))
    patient_id=Column(String, foreign_key=ForeignKey(PatientProfile.user_id))
    appointment_start_time=Column(String)
    duration= Column(String) #change it to duration. 
    feedback= Column(String)
    rating=Column(Integer, default=0)
    appointment_attended= Column(Boolean, default=False) 


class Schedule(Base):
    doctor_id=Column(String, primary_key=True, foreign_key=ForeignKey(DoctorProfile.user_id), index=True)
    schedule_date= Column(String) #11/01/2022 .time
    start_time=Column(String) #9, 10 (24 hr format)
    end_time= Column(String) #


class CovidQuestionnaire(Base):
    user_id=Column(String, primary_key=True, foreign_key=ForeignKey(PatientProfile.user_id))
    name=Column(String)
    email=Column(String)
    age=Column(Integer)
    has_cold=Column(Integer)
    has_fever=Column(Integer)
    has_cough=Column(Integer)
    has_weakness=Column(Integer)
    has_sour_throat=Column(Integer)
    has_body_pains=Column(Integer)
    other_symptoms=Column(String)
    covid_test=Column(Integer)
    updated_at=Column(String)
    