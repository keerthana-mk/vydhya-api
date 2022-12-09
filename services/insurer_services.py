import logging

from databases.repository.insurers import HealthcarePlanRepository
from models.healthcare_plans import InsurerPlanDetails, AddHealthcarePlanRequest, UpdateHealthcarePlanRequest
from models.mappers.healthcare_plan_mappers import *

class InsurerServices:

    @staticmethod
    def plan_exists(insurer_id, plan_name):
        try:
            plans = HealthcarePlanRepository.get_plans_by_insurer_and_plan_name(insurer_id, plan_name)
            return len(plans) > 0
        except Exception as e:
            error_message = f'error while fetching insurance plan {plan_name} for {insurer_id}: {str(e)}'
            logging.error(error_message)
            logging.exception(e)
            raise BaseException(e)


    @staticmethod
    def get_healthcare_plans(insurer_id):
        try:
            plan_details_list = HealthcarePlanRepository.get_plans_by_insurer(insurer_id)
            result = []
            for plan_details in plan_details_list:
                result.append(HealthcarePlanMapper.map_to_healthcare_plan(plan_details))
            return InsurerPlanDetails(plans=result, num_plans=len(result), message=f'found {len(result)} plans for insurer {insurer_id}')

        except Exception as e:
            error_message = f'error while fetching insurance plans for {insurer_id}: {str(e)}'
            logging.error(error_message)
            logging.exception(e)
            raise BaseException(e)

    @staticmethod
    def get_all_healthcare_plans():
        try:
            plans_query = HealthcarePlanRepository.get_all_plans()
            all_plans =[]
            for plan in plans_query:
                all_plans.append(HealthcarePlanMapper.map_to_healthcare_plan(plan))
            return InsurerPlanDetails(plans=all_plans, num_plans = len(all_plans), message=f'Found {len(all_plans)} plans')
        except Exception as e:
            error_message = f'error while fetching all insuerer details and their plans: {str(e)}'
            logging.error(error_message)
            logging.exception(e)
            raise BaseException(e)
    @staticmethod
    def create_healthcare_plan(insurer_id, plan_request: AddHealthcarePlanRequest):
        try:
            existing_plans = HealthcarePlanRepository.get_by_plan_name(plan_request.plan_name)
            if len(existing_plans) > 0:
                error_message = f'plan {plan_request.plan_name} already exists'
                raise Exception(error_message)

            plan_id = HealthcarePlanRepository.create_insurance_plan(plan_request.plan_name, plan_request.plan_display_name,
                                                                     insurer_id, plan_request.plan_description, plan_request.premium, plan_request.coverage,
                                                                     plan_request.deductible_amt, plan_request.duration_years,
                                                                     plan_request.is_monthly, plan_request.plan_exceptions)
            return plan_id
        except Exception as e:
            error_message = f'error while inserting insurance plans for {plan_request.insurer_id}: {str(e)}'
            logging.error(error_message)
            logging.exception(e)
            raise BaseException(e)

    @staticmethod
    def update_healthcare_plan(insurer_id, plan_name, update_plan_request: UpdateHealthcarePlanRequest):
        try:
            filterd_user_details = {}
            for key, val in update_plan_request.__dict__.items():
                if val is not None:
                    filterd_user_details[key] = val
            HealthcarePlanRepository.update_insurance_plan(insurer_id, plan_name, filterd_user_details)
            return HealthcarePlanMapper.map_to_healthcare_plan(HealthcarePlanRepository.get_by_plan_name(plan_name)[0])
        except Exception as e:
            error_message = f'error while deleting plan {plan_name} for insurer {insurer_id}: {str(e)}'
            logging.error(error_message)
            logging.exception(e)
            raise BaseException(e)

    @staticmethod
    def delete_healthcare_plan(insurer_id, plan_name):
        try:
            HealthcarePlanRepository.delete_by_plan_name_and_insurer(insurer_id, plan_name)
        except Exception as e:
            error_message = f'error while deleting plan {plan_name} for insurer {insurer_id}: {str(e)}'
            logging.error(error_message)
            logging.exception(e)
            raise BaseException(e)