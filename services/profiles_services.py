from databases.repository.profiles import PatientProfileRepository, DoctorProfileRepository, InsurerProfileRepository
from databases.repository.users import UserLoginRepository
import logging
from databases.db_models.profiles import InsurerProfile

class ProfileServices:
  
    def validate_user_role(self, user_role):
        if user_role not in ['patient', 'doctor', 'insurer']:
            raise Exception(f'invalid user role: {user_role}')
        
    def generate_insurer_id(self):
        query_result = InsurerProfileRepository.database.query(InsurerProfile.user_id).order_by(InsurerProfile.user_id)
        query_result = query_result.all()
        logging.info("query from generate_insurer_id={}".format(query_result[len(query_result)-1]))
        return query_result[len(query_result) - 1] if len(query_result) > 0 else 0
        
    def create_user_profile(self, user_id, fullname, user_email, user_role, theme="primary"):
        self.validate_user_role(user_role)
        if user_role == 'patient':
            PatientProfileRepository.create_user_profile(user_id, user_email, user_role, theme)
        if user_role == 'doctor':
            DoctorProfileRepository.create_user_profile(user_id, fullname, user_email, user_role, theme)
        if user_role == 'insurer':
            logging.info("am i coming here in insurer profile")
            # insurer_id = self.generate_insurer_id()
            InsurerProfileRepository.create_user_profile(user_id, fullname, user_email, user_role, theme)

    def get_user_profile(self, user_id, user_role):
        logging.info("here??")
        user_login = UserLoginRepository.get_user_login(user_id)
        if user_role not in ['patient', 'doctor', 'insurer']:
            raise Exception(f'invalid user role: {user_role}')
        user_details = None
        if user_login.user_id is None:
            logging.info('unable to find user')
            raise Exception(f'unable to find user {user_id}')
        if user_role == 'patient':
            user_details = PatientProfileRepository.get_patient_profile(user_login.user_id)
        if user_role == 'doctor':
            user_details = DoctorProfileRepository.get_doctor_profile(user_login.user_id)
        if user_role =='insurer':
            user_details = InsurerProfileRepository.get_insurer_profile(user_login.user_id) 
               
        logging.info(f'user_details = {user_details} for patient')     
        if user_details is None or len(user_details) == 0:
            raise Exception(f'unable to find user {user_id}')
        return user_details[0]
        # elif user_role == ''

    def update_user_profile(self, user_id, user_role, user_profile_details):
        filterd_user_details = {}
        user_login = UserLoginRepository.get_user_login(user_id)
        print(f"in insurer profile :{user_login.user_id}")
        if user_login is None:
            raise Exception(f'unable to find user {user_id}')
        for key, val in user_profile_details.__dict__.items():
            if val is not None and key != 'user_id':
                # logging.info(f'{key}: {val}')
                filterd_user_details[key] = val
        try:
            logging. info(f"filtered user details:{filterd_user_details}")
            if user_role == 'patient':
                PatientProfileRepository.update_patient_profile(user_login.user_id, filterd_user_details)
            if user_role == 'doctor':
                DoctorProfileRepository.update_doctor_profile(user_login.user_id, filterd_user_details)
            if user_role == "insurer":
                logging.info(" am i comming here in infrer profile update")
                InsurerProfileRepository.update_insurer_profile(user_id, filterd_user_details)
            return self.get_user_profile(user_id, user_role)
        except BaseException as e:
            error_message = f'user profile updation failed for {user_id}: {str(e)}'
            logging.error(error_message)
            raise BaseException(error_message)
