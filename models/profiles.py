from pydantic import BaseModel
from typing import Union, List


class UpdatePatientProfileRequest(BaseModel):
    contact_email: Union[str, None]
    theme: Union[str, None]
    gender: Union[str, None]
    dob: Union[str, None]
    height: Union[int, None]
    weight: Union[float, None]
    vaccinations: Union[List[str], None]
    blood_type: Union[str, None]
    allergies: Union[List[str], None]
    medications: Union[List[str], None]
    blood_pressure: Union[str, None]
    preexist_conditions: Union[List[str], None]
    health_plan_id: Union[str, None]
    monthly_medical_expense: Union[str, None]


class PatientProfileResponse(BaseModel):
    user_id: str
    contact_email: Union[str, None]
    theme: Union[str, None]
    gender: Union[str, None]
    dob: Union[str, None]
    height: Union[int, None]
    weight: Union[float, None]
    vaccinations: Union[List[str], None]
    blood_type: Union[str, None]
    allergies: Union[List[str], None]
    medications: Union[List[str], None]
    blood_pressure: Union[str, None]
    preexist_conditions: Union[List[str], None]
    health_plan_id: Union[str, None]
    monthly_medical_expense: Union[str, None]


class UpdateDoctorProfileRequest(BaseModel):
    contact_email: Union[str, None]
    contact_phone : Union[str, None]
    theme: Union[str, None]
    gender: Union[str, None]
    dob: Union[str, None]
    experience: Union[float, None]
    hospital_name: Union[str]
    hospital_address: Union[str, None]
    speciality: Union[str]
    is_hosp_covid_supported: Union[int, None]
    num_covid_beds_available: Union[int, None]
    insurance_accepted: Union[int, None]


class DoctorProfileResponse(BaseModel):
    user_id: str
    contact_email: Union[str, None]
    contact_phone: Union[str, None]
    theme: Union[str, None]
    gender: Union[str, None]
    dob: Union[str, None]
    experience: Union[float, None]
    hospital_name: Union[str, None]
    hospital_address: Union[str, None]
    speciality: Union[str, None]
    is_hosp_covid_supported: Union[int, None] #1 or 0
    num_covid_beds_available: Union[int, None]
    insurance_accepted: Union[int, None] # 1or 0


class InsurerProfileResponse(BaseModel):
    user_id: str
    contact_email: Union[str, None]
    theme: Union[str, None]
    insurer_name: Union[str, None]
 


class UpdateInsurerProfileRequest(BaseModel):
    user_id: Union[str, None]
    contact_email: Union[str, None]
    theme: Union[str, None]
    insurer_name: Union[str, None]


class UserProfileResponse(BaseModel):
    patient: Union[PatientProfileResponse, None]
    doctor: Union[DoctorProfileResponse, None]
    insurer: Union[InsurerProfileResponse, None]


class UserProfileRequests(BaseModel):
    patient: Union[UpdatePatientProfileRequest, None]
    doctor: Union[UpdateDoctorProfileRequest, None]
    insurer: Union[UpdateInsurerProfileRequest, None]


class SearchDoctorRequest(BaseModel):
    search_by: str
    search_string: str
    covid_support: bool


class DoctorDetails(BaseModel):
    name: str
    is_hosp_covid_supported: int
    contact_email: str
    contact_phone: str
    experience: float
    hospital_name: str
    hospital_address: str
    speciality: str
    insurance_accepted: int
    gender: str
