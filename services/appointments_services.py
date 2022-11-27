from databases.db_models.appointments import Appointments
from models.logging import logger
from databases.repository.appointments import AppointmentsRepository


class ManageAppointments:

    def add_appointment(appointment_id, doctor_id, patient_id, appointment_start_time, duration, feedback, rating, appointment_attended):

        try:
            logger.error("Creating Appointment - 2...")
            AppointmentsRepository.add_appointment(appointment_id,
            doctor_id,
            patient_id,
            appointment_start_time,
            duration,
            feedback,
            rating,
            appointment_attended)
            return {"message": "Appointment Added Successfully"}
        except BaseException as e:
            error_message = f'Failed to Add Appointment {str(e)}'
            logger.error(error_message)
            raise BaseException(error_message)

    def update_appointment(doctor_id, patient_id, old_time, new_time):
        try:
            AppointmentsRepository.update_appointment(doctor_id,patient_id,old_time,new_time)
            return {"message":"Appointment Updated Successfully"}
        except BaseException as e:
            error_message = f'Failed to Update Appointment {str(e)}'
            logger.error(error_message)
            raise BaseException(error_message)


    def delete_appointment(doctor_id, patient_id, appointment_time):
        try:
            AppointmentsRepository.delete_appointment(doctor_id, patient_id, appointment_time)
            return {"message": "Appointment Deleted Successfully"}
        except BaseException as e:
            error_message = f'Failed to Delete Appointment {str(e)}'
            logger.error(error_message)
            raise BaseException(error_message)

    def add_covid_questionnaire(user_id, name, email, age, has_cold, has_fever, has_cough, has_weakness, has_sour_throat, has_body_pains, other_symptoms, covid_test, updated_at):

        try:
            AppointmentsRepository.add_covid_questionnaire(user_id, name, email, age, has_cold, has_fever, has_cough, has_weakness, has_sour_throat,has_body_pains,other_symptoms, covid_test, updated_at)
            return {"message": "Covid Questionnaire Added Successfully"}

        except BaseException as e:
            error_message= f'Failed to add covid questionnaire {str(e)}'
            logger.error(error_message)
            raise BaseException(error_message)

    def get_covid_details(user_id):
        try:
            data=AppointmentsRepository.get_covid_details(user_id)
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            for message in data:
                return {'message': message}
        except BaseException as e:
            error_message=f'Failed to get Covid details {str(e)}'
            logger.error(error_message)
            raise BaseException(error_message)

