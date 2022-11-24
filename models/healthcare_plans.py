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
    is_monthly : bool

class UpdateHealthcarePlanRequest(BaseModel):
    plan_display_name: Union[str, None]
    plan_description: Union[str, None]
    plan_exceptions: Union[List[str], None]
    premium: Union[float, None]
    coverage: Union[float, None]
    duration_years: Union[float, None]
    deductible_amt: Union[float, None]
    is_monthly: Union[bool, None]

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
    is_monthly : bool

class InsurerPlanDetails(BaseModel):
    num_plans: int
    message: str
    plans: List[HealthcarePlanResponse]
