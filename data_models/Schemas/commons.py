from pydantic import BaseModel, validator
from datetime import datetime
from .profiles import UserProfileResponse, PatientProfileResponse, DoctorProfileResponse, InsurerProfileResponse


class DateTimeModel(BaseModel):
    created_at: datetime
    updated_at: datetime

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(
            cls,
            value: datetime,
    ) -> datetime:
        return value or datetime.now().strftime('%y-%m-%d %H:%M:%S')

def convert_patient_reponse(patient_data_obj):
     return UserProfileResponse(patient = PatientProfileResponse(user_id = patient_data_obj.user_id,
        contact_email = patient_data_obj.contact_email,
        theme = patient_data_obj.theme,
        gender = patient_data_obj.gender,
        dob = patient_data_obj.dob,
        height = patient_data_obj.height,
        weight = patient_data_obj.weight,
        vaccinations = patient_data_obj.vaccinations,
        blood_type = patient_data_obj.blood_type,
        allergies = patient_data_obj.allergies,
        medications = patient_data_obj.medications,
        blood_pressure = patient_data_obj.blood_pressure,
        preexist_conditions = patient_data_obj.preexist_conditions,
        health_plan_id = patient_data_obj.health_plan_id,
        monthly_medical_expense = patient_data_obj.monthly_medical_expense))

def convert_doctor_response(doctor_data_obj):
    return UserProfileResponse(doctor = DoctorProfileResponse(
        user_id = doctor_data_obj.user_id,
        contact_email = doctor_data_obj.contact_email,
        theme = doctor_data_obj.theme,
        gender = doctor_data_obj.gender,
        dob = doctor_data_doctor_data_objobj.dob,
        experience = doctor_data_obj.experience,
        hospital_name = doctor_data_obj.hospital_name,
        speciality = doctor_data_obj.speciality,
        is_hosp_covid_supported = doctor_data_obj.is_hosp_covid_supported,
        num_covid_beds_available = doctor_data_obj.num_covid_beds_available,
        insurance_accepted =doctor_data_obj.insurance_accepted
    ))
    
def convert_insurer_response(insurer_data_obj):
    return UserProfileResponse(insurer = InsurerProfileResponse(
        insurer_id = insurer_data_obj.insurer_id,
        user_id = insurer_data_obj.user_id,
        contact_email = insurer_data_obj.contact_email,
        theme = insurer_data_obj.theme,
        insurance_name = insurer_data_obj.insurance_name,
        plan_id = insurer_data_obj.plan_id
    ))