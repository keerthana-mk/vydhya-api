from asyncio.log import logger
from databases.db_models.appointments import Appointments
import logging
from databases.repository.appointments import AppointmentsRepository, ScheduleRepository


class ManageAppointments:

    def add_appointment(appointment_id, doctor_id, patient_id, appointment_start_time, duration, feedback, rating, appointment_attended):

        try:
            logging.error("Creating Appointment - 2...")
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
            logging.error(error_message)
            raise BaseException(error_message)

    def add_covid_appointment(appointment_id, doctor_id, patient_id, appointment_start_time, duration, appointment_attended):
        try:
            logging.error("Creating Appointment - 2...")
            AppointmentsRepository.add_covid_appointment(appointment_id,
            doctor_id,
            patient_id,
            appointment_start_time,
            duration,
            appointment_attended)
            return {"message": f"Covid test scheduled on {appointment_start_time} Successfully"}
        except BaseException as e:
            error_message = f'Failed to schedule covid test: {str(e)}'
            logging.error(error_message)
            raise BaseException(error_message)

    def update_appointment(doctor_id, patient_id, old_time, new_time):
        try:
            AppointmentsRepository.update_appointment(doctor_id,patient_id,old_time,new_time)
            return {"message":"Appointment Updated Successfully"}
        except BaseException as e:
            error_message = f'Failed to Update Appointment {str(e)}'
            logging.error(error_message)
            raise BaseException(error_message)


    def delete_appointment(doctor_id, patient_id, appointment_time):
        try:
            AppointmentsRepository.delete_appointment(doctor_id, patient_id, appointment_time)
            return {"message": "Appointment Deleted Successfully"}
        except BaseException as e:
            error_message = f'Failed to Delete Appointment {str(e)}'
            logging.error(error_message)
            raise BaseException(error_message)

    def add_covid_questionnaire(user_id, name, email, age, has_cold, has_fever, has_cough, has_weakness, has_sour_throat, has_body_pains, other_symptoms, covid_test, updated_at):

        try:
            AppointmentsRepository.add_covid_questionnaire(user_id, name, email, age, has_cold, has_fever, has_cough, has_weakness, has_sour_throat,has_body_pains,other_symptoms, covid_test, updated_at)
            return {"message": "Covid Questionnaire Added Successfully"}

        except BaseException as e:
            error_message= f'Failed to add covid questionnaire {str(e)}'
            logging.error(error_message)
            raise BaseException(error_message)

    def get_covid_details(user_id):
        try:
            data=AppointmentsRepository.get_covid_details(user_id)
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            for message in data:
                return {'message': message}
        except BaseException as e:
            error_message=f'Failed to get Covid details {str(e)}'
            logging.error(error_message)
            raise BaseException(error_message)

    
    def get_upcoming_appointments(user_id):
        try:
            message=[]
            data=AppointmentsRepository.get_upcoming_appointments(user_id)
            for i in data:
                message.append(i)
            return {'message': data}

        except BaseException as e:
            error_message=f'Failed to get upcoming appointments {str(e)}'
            logging.error(error_message)
            raise BaseException(error_message)

    def add_schedule(doctor_id, schedule_time, end_time,is_available):
        try:
            data=ScheduleRepository.add_schedule(
                doctor_id, schedule_time, end_time,is_available
            )

            return {'message':data}

        except BaseException as e:
            error_message=f'Failed to add the Schedule {str(e)}'
            raise BaseException(error_message)

    def get_schedule(doctor_id):
        try:
            data=ScheduleRepository.get_schedule(doctor_id)
            return {'message': data}

        except BaseException as e:
            error_message=f'Failed to get the Schedule {str(e)}'
            raise BaseException(error_message)

