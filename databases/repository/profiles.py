import logging

from databases.db_models.profiles import PatientProfile, DoctorProfile, InsurerProfile
from app.config import get_db_actual
from sqlalchemy.orm import Session
from databases.db_models.users import UserLogin

class PatientProfileRepository:
    database: Session = get_db_actual()

    @staticmethod
    def create_user_profile(user_id, user_email, user_role, theme):
        new_user_profile = PatientProfile(
            user_id=user_id,
            contact_email=user_email,
            theme=theme
        )
        try:
            PatientProfileRepository.database.add(new_user_profile)
            PatientProfileRepository.database.commit()
        except Exception as e:
            PatientProfileRepository.database.rollback()
            error_message = f'error while inserting to database: {str(e)}'
            raise Exception(error_message)
        
    @staticmethod
    def get_patient_profile(user_id):
        patient_query = PatientProfileRepository.database.query(PatientProfile).filter(
            (PatientProfile.user_id == user_id))
        patient_query = patient_query.all()
        logging.info(f'patient query in patient repository = {patient_query}')
        return patient_query

    @staticmethod
    def update_patient_profile(user_id, user_profile_details):
        try:
            PatientProfileRepository.database.query(PatientProfile).filter(PatientProfile.user_id == user_id).update(
                user_profile_details)
            PatientProfileRepository.database.commit()
        except Exception as e:
            PatientProfileRepository.database.rollback()
            raise BaseException(e)
    @staticmethod
    def enroll_in_healthcare_plan(patient_id, plan_id):
        try:
            DoctorProfileRepository.database.query(PatientProfile).filter(PatientProfile.user_id == patient_id).update({PatientProfile.health_plan_id : plan_id})
            DoctorProfileRepository.database.commit()
            return {"message" : f'Enrolled in plan {plan_id} successfully'}
        except Exception as e:
            PatientProfileRepository.database.rollback()
            raise BaseException(e)

class DoctorProfileRepository:
    database: Session = get_db_actual()

    @staticmethod
    def create_user_profile(user_id, fullname, user_email, user_role, theme):
        try:
            new_user_profile = DoctorProfile(
                user_id=user_id,
                full_name = fullname,
                contact_email=user_email,
                theme=theme
            )
            DoctorProfileRepository.database.add(new_user_profile)
            DoctorProfileRepository.database.commit()
        except Exception as e:
            DoctorProfileRepository.database.rollback()
            error_message = "Error while creating doctor profile :{}".format(e)
            raise(error_message)
    
            
    @staticmethod
    def get_doctor_profile(user_id):
        doctor_query = DoctorProfileRepository.database.query(DoctorProfile).filter((DoctorProfile.user_id == user_id))
        doctor_query = doctor_query.all()
        logging.info(f'doctor query in patient repository = {doctor_query}')
        return doctor_query

    @staticmethod
    def update_doctor_profile(user_id, user_profile_details):
        try:
            DoctorProfileRepository.database.query(DoctorProfile).filter(DoctorProfile.user_id == user_id).update(
                user_profile_details)
            DoctorProfileRepository.database.commit()
        except Exception as e:
            DoctorProfileRepository.database.rollback()
            error_message = "Error while updating doctor profile : {}".format(e)
            logging.info(error_message)
            raise BaseException(error_message)

    @staticmethod
    def get_doctor_by_name(name):
        try:
            name_like = f'%{name}%'
            query_result = DoctorProfileRepository.database.query(DoctorProfile).\
                filter(DoctorProfile.full_name.ilike(name_like)).all()
            logging.info("doctor search =={}".format(query_result))
            return query_result
        except Exception as e:
            logging.error("Error while search name of doctor",e)
            raise BaseException(e)

    @staticmethod
    def get_doctor_by_speciality(speciality):
        try:
            speciality_like = f'%{speciality}%'
            query_result = DoctorProfileRepository.database.query(DoctorProfile)\
                .filter(DoctorProfile.speciality.ilike(speciality_like)).all()
            return query_result
        except Exception as e:
            logging.error(e)
            raise BaseException(e)

    

class InsurerProfileRepository:
    database: Session = get_db_actual()

    @staticmethod
    def create_user_profile(user_id, name, user_email, role, theme):
        try:
            new_user_profile = InsurerProfile(
                user_id=user_id,
                insurer_name=name,
                contact_email=user_email,
                theme=theme,
                
            )
            logging.info(f'insurer_profile: {new_user_profile}')
            InsurerProfileRepository.database.add(new_user_profile)
            InsurerProfileRepository.database.commit()
        except Exception as e:
            InsurerProfileRepository.database.rollback()
            error_message = "error while creating insurer profile: {}".format(e)
            logging.error(error_message)
            raise Exception(error_message)
        
    @staticmethod
    def get_insurer_profile(user_id):
        insurer_query = InsurerProfileRepository.database.query(InsurerProfile).filter(
            (InsurerProfile.user_id == user_id))
        insurer_query = insurer_query.all()
        logging.info(f'insurer query in insurer repository = {insurer_query}')
        return insurer_query

    @staticmethod
    def update_insurer_profile(user_id, user_profile_details):
        try:
            InsurerProfileRepository.database.query(InsurerProfile).filter(InsurerProfile.user_id == user_id).update(
                user_profile_details)
            InsurerProfileRepository.database.commit()
        except Exception as e:
            InsurerProfileRepository.database.rollback()
            raise BaseException(e)
