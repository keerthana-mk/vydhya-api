from pydantic import BaseModel
from typing import Union, List


class UpdatePatientProfileRequest(BaseModel):
    user_email : Union[str, None]
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
    user_name : str
    user_email: Union[str, None]
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

class UserProfileResponse(BaseModel):
    patient: PatientProfileResponse

class UserProfileRequests(BaseModel):
    patient : UpdatePatientProfileRequest