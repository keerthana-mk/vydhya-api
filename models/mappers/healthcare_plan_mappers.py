from databases.db_models.insurers import HealthcarePlan
from models.healthcare_plans import HealthcarePlanResponse

class HealthcarePlanMapper:

    @staticmethod
    def map_to_healthcare_plan(plan_details: HealthcarePlan):
        return HealthcarePlanResponse(
            plan_id=plan_details.plan_id,
            insurer_id=plan_details.insurer_id,
            plan_name=plan_details.plan_name,
            plan_display_name=plan_details.plan_display_name,
            plan_description=plan_details.plan_description,
            plan_exceptions=plan_details.plan_exceptions,
            premium=plan_details.premium,
            coverage=plan_details.coverage,
            duration_years=plan_details.duration_years,
            deductible_amt=plan_details.deductible_amt,
            is_monthly=plan_details.is_monthly
            )
