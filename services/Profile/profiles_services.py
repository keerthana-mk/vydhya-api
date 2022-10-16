from collections import defaultdict
from databases.repository.profiles import PatientProfileRepository, DoctorProfileRepository, InsurerProfileRepository
from databases.repository.users import UserLoginRepository, UserProfileRepository
from data_models.Schemas.logging import logger
from databases.db_models.profiles import InsurerProfile

class ProfileServices:
  
    def validate_user_role(self, user_role):
        if user_role not in ['patient', 'doctor', 'insurer']:
            raise Exception(f'invalid user role: {user_role}')
        
    def generate_insurer_id(self):
        query_result = InsurerProfileRepository.database.query(InsurerProfile.user_id).order_by(InsurerProfile.insurer_id)
        query_result = query_result.all()
        return query_result[len(query_result) - 1] if len(query_result) > 0 else 0
        
    def create_user_profile(self, user_id, user_email, user_role, theme="primary"):
        self.validate_user_role(user_role)
        if user_role == 'patient':
            PatientProfileRepository.create_user_profile(user_id, user_email, user_role, theme)
        if user_role == 'doctor':
            DoctorProfileRepository.create_user_profile(user_id, user_email, user_role, theme)
        if user_role == 'insurer':
            insurer_id = self.generate_insurer_id()
            InsurerProfileRepository.create_user_profile('insurance_id_'+str(insurer_id), user_id, user_email, user_role, theme)

    def get_user_profile(self, user_id, user_role):
        logger.info("here??")
        user_login = UserLoginRepository.get_user_login(user_id, user_id)
        logger.info('am i coming here?')
        if user_role not in ['patient', 'doctor', 'insurer']:
            raise Exception(f'invalid user role: {user_role}')
        user_details = None
        if user_login is None:
            logger.info('unable to find user')
            raise Exception(f'unable to find user {user_id}')
        if user_role == 'patient':
            user_details = PatientProfileRepository.get_patient_profile(user_login.user_id)
        if user_role == 'doctor':
            user_details = DoctorProfileRepository.get_doctor_profile(user_login.user_id)
        if user_role =='insurer':
            user_details = InsurerProfileRepository.get_insurer_profile(user_login.user_id) 
               
        logger.info(f'user_details = {user_details} for patient')     
        if user_details is None or len(user_details) == 0:
            raise Exception(f'unable to find user {user_id}')
        return user_details[0]
        # elif user_role == ''
    def update_user_profile(self, user_id, user_role, user_profile_details):
        filterd_user_details = {}
        user_login = UserLoginRepository.get_user_login(user_id, user_id)
        if user_login is None:
            raise Exception(f'unable to find user {user_id}')
        for key, val in user_profile_details.__dict__.items():
            if val is not None:
                filterd_user_details[key] = val
        try:
            if user_role == 'patient':
                PatientProfileRepository.update_patient_profile(user_login.user_id, filterd_user_details)
            if user_role == 'doctor':
                DoctorProfileRepository.update_doctor_profile(user_login.user_id, filterd_user_details)
            if user_role == "insurer":
                InsurerProfileRepository.update_insurer_profile(user_login.user_id, filterd_user_details)
            return self.get_user_profile(user_id, user_role)
        except BaseException as e:
            error_message = f'user profile updation failed for {user_id}: {str(e)}'
            logger.error(error_message)
            raise BaseException(error_message)
