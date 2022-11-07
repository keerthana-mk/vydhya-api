from typing import Union

from pydantic import BaseModel
from pydantic.fields import List

class AddHealthcarePlanRequest(BaseModel):
    insurer_id: str
    plan_name: str
    plan_display_name: str
    plan_description: str
    plan_exceptions: Union[List[str], None]
    premium: float
    coverage: float
    duration_years: float
    deductible_amt: float
    is_monthly = True

class UpdateHealthcarePlanRequest(BaseModel):
    plan_display_name: Union[str, None]
    plan_description: Union[str, None]
    plan_exceptions: Union[List[str], None]
    premium: Union[str, None]
    coverage: Union[str, None]
    duration_years: Union[str, None]
    deductible_amt: Union[str, None]
    is_monthly: Union[str, None]

class AddHealthcarePlanResponse(BaseModel):
    plan_id: str

class HealthcarePlanResponse(BaseModel):
    plan_id: str
    insurer_id: str
    plan_name: str
    plan_display_name: str
    plan_description: Union[str, None]
    plan_exceptions: Union[List[str], None]
    premium: float
    coverage: float
    duration_years: float
    deductible_amt: float
    is_monthly = True

class InsurerPlanDetails(BaseModel):
    num_plans: int
    message: str
    plans: List[HealthcarePlanResponse]
