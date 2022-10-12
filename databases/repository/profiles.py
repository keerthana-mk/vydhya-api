from databases.db_models.profiles import PatientProfile, DoctorProfile, InsurerProfile
import sqlalchemy.sql.expression.*

class PatientProfileRepository:
    database: Session = get_db_actual()

    @staticmethod
    def create_user_profile(user_id, user_email, user_role, theme):
        new_user_profile = PatientProfile(
            user_id=user_id,
            user_name=user_email,
            user_email=user_email,
            theme=theme
        )
        PatientProfileRepository().database.add(new_user_profile)
        PatientProfileRepository().database.commit()

    
    @staticmethod
    def get_patient_profile(user_id):
        patient_query = PatientProfileRepository.database.query(PatientProfile).filter((PatientProfile.user_id == user_id))
        patient_query = patient_query.all()
        return patient_query

    @staticmethod
    def update_patient_profile(user_id, user_profile_details):
        try:
            PatientProfileRepository.database.query(PatientProfile).filter(PatientProfile.user_id == user_id).update(user_profile_details)
            PatientProfileRepository.database.commit()
        except Exception as e:
            raise BaseException(e)