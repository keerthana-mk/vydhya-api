from pydantic import BaseModel
from typing import Union, List

class Appointments(BaseModel):
    appointment_id: str
    doctor_id: str
    # patient_id: str
    appointment_start_time: str
    duration: str
    feedback: Union[str, None]
    rating: Union[float, None]
    appointment_attended: Union[bool, None]

class UpdateAppointment(BaseModel):
    doctor_id: str
    # patient_id: str
    old_time: str
    new_time: str

class DeleteAppointment(BaseModel):
    doctor_id: str
    # patient_id: str
    appointment_time: str

class Schedule(BaseModel):
    schedule_id: str
    # doctor_id: str
    schedule_start_date_time: str
    schedule_end_date_time: str
    is_available: bool



class CovidQuestionnaire(BaseModel):
    # user_id: str
    name: str
    email: str
    age: int
    has_cold: int
    has_fever: int
    has_cough: int
    has_weakness: int
    has_sour_throat: int
    has_body_pains: int
    other_symptoms: str
    covid_test: int
    updated_at: str



class AppointmentResponseMessage(BaseModel):
    message: str

class AppointmentResponse(BaseModel):
    status: int
    error: str
    data: AppointmentResponseMessage

class CovidTestScheduleRequest(BaseModel):
    appointment_start_time: str
    duration: str