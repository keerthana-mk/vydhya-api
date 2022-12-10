from pydantic import BaseModel, validator
from datetime import datetime

from databases.db_models.profiles import DoctorProfile
from databases.db_models.appointment_feedback import AppointmentFeedback
from databases.db_models.appointments import Appointments
from .profiles import UserProfileResponse, PatientProfileResponse, DoctorProfileResponse, InsurerProfileResponse, \
    DoctorDetails
from typing import Union, List, Dict
from fastapi.encoders import jsonable_encoder


class DateTimeModel(BaseModel):
    created_at: datetime
    updated_at: datetime

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(
            cls,
            value: datetime,
    ) -> datetime:
        return value or datetime.now().strftime('%y-%m-%d %H:%M:%S')


class StandardHttpResponse(BaseModel):
    status: int
    error: Union[str, None]
    data: Union[dict, None]

def convert_patient_reponse(patient_data_obj):
    return UserProfileResponse(patient=PatientProfileResponse(user_id=patient_data_obj.user_id,
                                                              contact_email=patient_data_obj.contact_email,
                                                              theme=patient_data_obj.theme,
                                                              gender=patient_data_obj.gender,
                                                              dob=patient_data_obj.dob,
                                                              height=patient_data_obj.height,
                                                              weight=patient_data_obj.weight,
                                                              vaccinations=patient_data_obj.vaccinations,
                                                              blood_type=patient_data_obj.blood_type,
                                                              allergies=patient_data_obj.allergies,
                                                              medications=patient_data_obj.medications,
                                                              blood_pressure=patient_data_obj.blood_pressure,
                                                              preexist_conditions=patient_data_obj.preexist_conditions,
                                                              health_plan_id=patient_data_obj.health_plan_id,
                                                              monthly_medical_expense=patient_data_obj.monthly_medical_expense))


def convert_doctor_response(doctor_data_obj):
    return UserProfileResponse(doctor=DoctorProfileResponse(
        user_id=doctor_data_obj.user_id,
        contact_email=doctor_data_obj.contact_email,
        contact_phone=doctor_data_obj.contact_phone,
        theme=doctor_data_obj.theme,
        gender=doctor_data_obj.gender,
        dob=doctor_data_obj.dob,
        experience=doctor_data_obj.experience,
        hospital_name=doctor_data_obj.hospital_name,
        hospital_address=doctor_data_obj.hospital_address,
        speciality=doctor_data_obj.speciality,
        is_hosp_covid_supported=doctor_data_obj.is_hosp_covid_supported,
        num_covid_beds_available=doctor_data_obj.num_covid_beds_available,
        insurance_accepted=doctor_data_obj.insurance_accepted
    ))


def convert_insurer_response(insurer_data_obj):
    return UserProfileResponse(insurer=InsurerProfileResponse(
        # insurer_id=insurer_data_obj.insurer_id
        insurer_id=insurer_data_obj.user_id,
        user_id=insurer_data_obj.user_id,
        contact_email=insurer_data_obj.contact_email,
        theme=insurer_data_obj.theme,
        insurer_name=insurer_data_obj.insurer_name
        # plan_id=insurer_data_obj.plan_id
    ))


def generate_doctor_details(doctor_profile: DoctorProfile):
    return DoctorDetails(
        name=doctor_profile.full_name,
        gender=doctor_profile.gender,
        experience=doctor_profile.experience,
        contact_email=doctor_profile.contact_email,
        contact_phone=doctor_profile.contact_phone,
        speciality=doctor_profile.speciality,
        hospital_address=doctor_profile.hospital_address,
        hospital_name=doctor_profile.hospital_name,
        is_hosp_covid_supported=doctor_profile.is_hosp_covid_supported,
        insurance_accepted=doctor_profile.insurance_accepted
    )
    
def generate_feedback_response(feedback_details: AppointmentFeedback):
    return AppointmentFeedback(
        patient_id = feedback_details.patient_id,
        feedback = feedback_details.feedback,
        rating = feedback_details.rating,
        submitted_at = feedback_details.submitted_at
    )

def generate_feedback_by_appointment(feedback :Appointments):
    return Appointments(
        feedback = feedback.feedback,
        rating = feedback.rating
    )


def get_http_response(data, status, error=None):
    if error is not None:
        return jsonable_encoder(StandardHttpResponse(status=int(status), data=data, error=error))
    else:
        return jsonable_encoder(StandardHttpResponse(status=int(status), data=data))
