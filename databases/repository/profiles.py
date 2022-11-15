import logging

from databases.db_models.profiles import PatientProfile, DoctorProfile, InsurerProfile
from app.config import get_db_actual
from sqlalchemy.orm import Session
from models.logging import logger


class PatientProfileRepository:
    database: Session = get_db_actual()

    @staticmethod
    def create_user_profile(user_id, user_email, user_role, theme):
        new_user_profile = PatientProfile(
            user_id=user_id,
            contact_email=user_email,
            theme=theme
        )
        PatientProfileRepository.database.add(new_user_profile)
        PatientProfileRepository.database.commit()

    @staticmethod
    def get_patient_profile(user_id):
        patient_query = PatientProfileRepository.database.query(PatientProfile).filter(
            (PatientProfile.user_id == user_id))
        patient_query = patient_query.all()
        logger.info(f'patient query in patient repository = {patient_query}')
        return patient_query

    @staticmethod
    def update_patient_profile(user_id, user_profile_details):
        try:
            PatientProfileRepository.database.query(PatientProfile).filter(PatientProfile.user_id == user_id).update(
                user_profile_details)
            PatientProfileRepository.database.commit()
        except Exception as e:
            raise BaseException(e)


class DoctorProfileRepository:
    database: Session = get_db_actual()

    @staticmethod
    def create_user_profile(user_id, user_email, user_role, theme):
        new_user_profile = DoctorProfile(
            user_id=user_id,
            contact_email=user_email,
            theme=theme
        )
        DoctorProfileRepository.database.add(new_user_profile)
        DoctorProfileRepository.database.commit()

    @staticmethod
    def get_doctor_profile(user_id):
        doctor_query = DoctorProfileRepository.database.query(DoctorProfile).filter((DoctorProfile.user_id == user_id))
        doctor_query = doctor_query.all()
        logger.info(f'doctor query in patient repository = {doctor_query}')
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
            logger.info(error_message)
            raise BaseException(error_message)

    @staticmethod
    def get_doctor_by_name(name):
        try:
            name_like = f'%{name}%'
            query_result = DoctorProfileRepository.database.query(DoctorProfile).\
                filter(DoctorProfile.full_name.ilike(name_like)).all()
            return query_result
        except Exception as e:
            logging.error(e)
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
    def create_user_profile(insurer_id, user_id, user_email, user_role, theme):
        new_user_profile = InsurerProfile(
            insurer_id=insurer_id,
            user_id=user_id,
            contact_email=user_email,
            theme=theme
        )
        InsurerProfileRepository.database.add(new_user_profile)
        InsurerProfileRepository.database.commit()

    @staticmethod
    def get_insurer_profile(user_id):
        insurer_query = InsurerProfileRepository.database.query(InsurerProfile).filter(
            (InsurerProfile.user_id == user_id))
        insurer_query = insurer_query.all()
        logger.info(f'insurer query in insurer repository = {insurer_query}')
        return insurer_query

    @staticmethod
    def update_insurer_profile(user_id, user_profile_details):
        try:
            InsurerProfileRepository.database.query(InsurerProfile).filter(InsurerProfile.user_id == user_id).update(
                user_profile_details)
            InsurerProfileRepository.database.commit()
        except Exception as e:
            raise BaseException(e)
