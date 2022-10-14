from pydantic import BaseModel
from typing import Union, List


class UpdatePatientProfileRequest(BaseModel):
    contact_email : Union[str, None]
    theme : Union[str, None]
    gender : Union[str, None]
    dob : Union[str, None]
    height : Union[int, None]
    weight : Union[float, None]
    vaccinations : Union[List[str], None]
    blood_type : Union[str, None]
    allergies : Union[List[str], None]
    medications : Union[List[str], None]
    blood_pressure : Union[str, None]
    preexist_conditions : Union[List[str], None]
    health_plan_id :Union[str, None]
    monthly_medical_expense : Union[str, None]

class PatientProfileResponse(BaseModel):
    user_id : str
    contact_email: Union[str, None]
    theme : Union[str, None]
    gender : Union[str, None]
    dob : Union[str, None]
    height : Union[int, None]
    weight : Union[float, None]
    vaccinations : Union[List[str], None]
    blood_type : Union[str, None]
    allergies : Union[List[str], None]
    medications : Union[List[str], None]
    blood_pressure : Union[str, None]
    preexist_conditions : Union[List[str], None]
    health_plan_id :Union[str, None]
    monthly_medical_expense : Union[str, None]

class UpdateDoctorProfileRequest(BaseModel):
    contact_email : Union[str, None]
    theme : Union[str, None]
    gender : Union[str, None]
    dob : Union[str, None]
    experience : Union[float, None]
    hospital_name : Union[str]
    speciality : Union[str]
    is_hosp_covid_supported : Union[str, None]
    num_covid_beds_available : Union[int, None]
    insurance_accepted : Union[str, None]

class DoctorProfileResponse(BaseModel):
    user_id : str
    contact_email : Union[str, None]
    theme : Union[str, None]
    gender : Union[str, None]
    dob : Union[str, None]
    experience : Union[float, None]
    hospital_name : Union[str, None]
    speciality : Union[str, None]
    is_hosp_covid_supported : Union[str, None]
    num_covid_beds_available : Union[int, None]
    insurance_accepted : Union[str, None]
class InsurerProfileResponse(BaseModel):
    insurer_id : str
    user_id : str
    contact_email : Union[str, None]
    theme : Union[str, None]
    insurance_name : Union[str, None]
    plan_id : Union[str, None]

class UpdateInsurerProfileRequest(BaseModel):
    insurer_id : str
    contact_email : Union[str, None]
    theme : Union[str, None]
    insurance_name : Union[str, None]
class UserProfileResponse(BaseModel):
    patient: Union[PatientProfileResponse, None]
    doctor : Union[DoctorProfileResponse, None]
    insurer : Union[InsurerProfileResponse, None]

class UserProfileRequests(BaseModel):
    patient : Union[UpdatePatientProfileRequest, None]
    doctor : Union[UpdateDoctorProfileRequest, None]
    insurer : Union[UpdateInsurerProfileRequest, None]