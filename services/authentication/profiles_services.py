from collections import defaultdict

from databases.repository.profiles import PatientProfileRepository


class ProfileServices:

    def validate_user_role(self, user_role):
        if user_role not in ['patient', 'doctor', 'insurer']:
            raise Exception(f'invalid user role: {user_role}')

    def create_user_profile(self, user_id, user_name, user_email, user_role, theme="primary"):
        self.validate_user_role(user_role)
        if user_role == 'patient':
            PatientProfileRepository.create_user_profie(user_id, user_name, user_email, theme)
        # elif user_role == 'doctor':
        #     DoctorProfileRepository...

    def get_user_profile(self, user_id, user_role):
        if user_role not in ['patient', 'doctor', 'insurer']:
            raise Exception(f'invalid user role: {user_role}')
        if user_role == 'patient':
            patient_details = PatientProfileRepository.get_patient_profile(user_id)
        return patient_details
        # elif user_role == ''

    def update_user_profile(self, user_id, user_role, user_profile_details):
        filterd_user_details = defaultdict()
        for key, val in user_profile_details.items():
            if val is not None:
                filterd_user_details.add(key, val)
        try:
            if user_role == 'patient':
                PatientProfileRepository.update_patient_profile(user_id, filterd_user_details)
            # elif user_role ==:

            return self.get_user_profile(user_id, user_role)
        except BaseException as e:
            error_message = f'user profile updation failed for {user_id}: {str(e)}'
            print(error_message)
            raise BaseException(error_message)
