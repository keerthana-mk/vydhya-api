import logging

from sqlalchemy import and_
from sqlalchemy.orm import Session

from databases.db_connection import get_db_actual
from databases.db_models.insurers import HealthcarePlan

class HealthcarePlanRepository:
    database: Session = get_db_actual()

    healthcare_plan_details_column_names = ['plan_name', 'insurer_id', 'plan_display_name', 'plan_exceptions', 'premium', 'coverage',
                                            'duration_years', 'deductible_amt', 'is_monthly']

    healthcare_plan_details_mandatory_cols = ['plan_name', 'insurer_id', 'plan_display_name', 'premium', 'coverage',
                                              'duration_years', 'deductible_amt', 'is_monthly']

    healthcare_plan_immutables = ['plan_name', 'insurer_id']

    @staticmethod
    def get_by_plan_name(plan_name):
        query_result = HealthcarePlanRepository.database.query(HealthcarePlan).filter(HealthcarePlan.plan_name == plan_name).all()
        return query_result

    @staticmethod
    def get_plans_by_insurer(insurer_id):
        query_result = HealthcarePlanRepository.database.query(HealthcarePlan).filter(HealthcarePlan.insurer_id == insurer_id).all()
        return query_result
    
    @staticmethod
    def get_all_plans():
        query_result = HealthcarePlanRepository.database.query(HealthcarePlan).all()
        return query_result
    
    @staticmethod
    def get_plans_by_insurer_and_plan_name(insurer_id, plan_name):
        query_result = HealthcarePlanRepository.database.query(HealthcarePlan). \
            filter(and_(HealthcarePlan.insurer_id == insurer_id, HealthcarePlan.plan_name == plan_name)).all()
        logging.info("getall plans")
        return query_result

    @staticmethod
    def generate_plan_id(insurer_id):
        plan_num = HealthcarePlanRepository.get_last_plan_number(insurer_id) + 1
        return f'plan_{insurer_id}_{plan_num}'

    @staticmethod
    def get_last_plan_number(insurer_id):
        query_result = HealthcarePlanRepository.database.query(HealthcarePlan).filter(HealthcarePlan.insurer_id == insurer_id).order_by(
            HealthcarePlan.plan_id)
        query_result = query_result.all()
        return int(query_result[len(query_result) - 1].plan_id.split('_')[-1]) if len(query_result) > 0 else 0

    @staticmethod
    def create_insurance_plan(plan_name, plan_display_name, insurer_id, description, premium, coverage, deductible_amt, duration_years=1, is_monthly=True,
                              plan_exceptions=None):
        plan_id = HealthcarePlanRepository.generate_plan_id(insurer_id)
        new_healthcare_plan = HealthcarePlan(plan_id=plan_id, plan_name=plan_name, plan_display_name=plan_display_name, insurer_id=insurer_id,
                                             plan_exceptions=plan_exceptions,plan_description=description, premium=premium, coverage=coverage, deductible_amt=deductible_amt,
                                             duration_years=duration_years, is_monthly=is_monthly)
        try:
            HealthcarePlanRepository.database.add(new_healthcare_plan)
            HealthcarePlanRepository.database.commit()
            return plan_id
        except Exception as e:
            HealthcarePlanRepository.database.rollback()
            error_message = f'error while inserting to database: {str(e)}'
            raise Exception(error_message)

    @staticmethod
    def update_insurance_plan(insurer_id, plan_name, update_plan_details):
        for immutable_col in HealthcarePlanRepository.healthcare_plan_immutables:
            if immutable_col in update_plan_details.keys():
                raise Exception(f'cannot update {immutable_col}')
        try:
            HealthcarePlanRepository.database.query(HealthcarePlan).filter(
                and_(HealthcarePlan.insurer_id == insurer_id, HealthcarePlan.plan_name == plan_name)).update(update_plan_details)
            HealthcarePlanRepository.database.commit()
        except Exception as e:
            HealthcarePlanRepository.database.rollback()
            raise BaseException(e)

    @staticmethod
    def delete_by_plan_name_and_insurer(insurer_id, plan_name):
        try:
            query_result = HealthcarePlanRepository.database.query(HealthcarePlan).filter(
                and_(HealthcarePlan.insurer_id == insurer_id, HealthcarePlan.plan_name == plan_name)).first()

            logging.info(f"logging from delete_by_plan_name_and_insurer ={query_result}")

            HealthcarePlanRepository.database.delete(query_result)    
            HealthcarePlanRepository.database.commit()
        except Exception as e:
            HealthcarePlanRepository.database.rollback()
            raise BaseException(e)

    