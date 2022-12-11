import logging
from sqlalchemy import or_, and_
from datetime import datetime
from pytz import timezone
from databases.db_models.appointments import Appointments, Schedule, CovidQuestionnaire
from app.config import get_db_actual
from sqlalchemy.orm import Session
from models.appointments import UpdateAppointment
import logging
from models import commons


class AppointmentsRepository:
    database: Session = get_db_actual()

    @staticmethod
    def add_appointment(appointment_id, doctor_id, patient_id, start_time, duration, feedback, rating,
                        appointment_attended):
        logging.error("Creating Appointment - 3...")

        # Validation to check whether Appointment time is in future or not.
        appointment_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        current_time = str(datetime.now(timezone('US/Eastern')))
        current_time = current_time[:-16]
        current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M')
        if appointment_time > current_time:
            print("___________________________________________________________________")
            last_appointment_id = AppointmentsRepository.get_last_appointmnet()
            print(last_appointment_id)
            # last_appointment_id=str(last_appointment_id)
            if last_appointment_id == None:
                id = 1000
            else:
                last_appointment_id = str(last_appointment_id)
                b = ""
                for i in last_appointment_id:
                    if i.isnumeric():
                        b = b + i
                print(b)
                id = int(b)
                id = id + 1

            new_appointment_id = id
            new_appointment = Appointments(
                appointment_id=new_appointment_id,
                doctor_id=doctor_id,
                patient_id=patient_id,
                appointment_start_time=start_time,
                duration=duration,
                feedback=feedback,
                rating=rating,
                appointment_attended=appointment_attended
            )
            query_result = AppointmentsRepository.database.query(Appointments).filter(
                or_(Appointments.doctor_id == doctor_id, Appointments.patient_id == patient_id))
            query_result = query_result.all()
            try:  # Validation to check whether there is an appointment at same time
                for i in range(0, len(query_result)):
                    if query_result[i].appointment_start_time == start_time:
                        print("There is an appointment shceduled at same time.")
                        raise BaseException("Doctor or patient has similar appointment scheduled.")
                else:
                    AppointmentsRepository.database.add(new_appointment)
                    AppointmentsRepository.database.commit()
            except BaseException as e:
                AppointmentsRepository.database.rollback()
                error_message = e
                logging.error(error_message)
                raise BaseException(error_message)
        else:
            AppointmentsRepository.database.rollback()
            raise BaseException("Appointment Time must be of Future Time")

    def add_covid_appointment(appointment_id, doctor_id, patient_id, start_time, duration, appointment_attended):
        logging.error("Creating Appointment - 3...")

        # Validation to check whether Appointment time is in future or not.
        appointment_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        current_time = str(datetime.now(timezone('US/Eastern')))
        current_time = current_time[:-16]
        current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M')
        if appointment_time > current_time:
            print("___________________________________________________________________")
            last_appointment_id = AppointmentsRepository.get_last_appointmnet()
            print(last_appointment_id)
            # last_appointment_id=str(last_appointment_id)
            if last_appointment_id is None:
                id = 1000
            else:
                last_appointment_id = str(last_appointment_id)
                b = ""
                for i in last_appointment_id:
                    if i.isnumeric():
                        b = b + i
                print(b)
                id = int(b)
                id = id + 1

            new_appointment_id = appointment_id + "_" + str(id)
            new_appointment = Appointments(
                appointment_id=new_appointment_id,
                doctor_id=doctor_id,
                patient_id=patient_id,
                appointment_start_time=start_time,
                duration=duration,
                feedback="None",
                rating=0,
                appointment_attended=appointment_attended
            )
            query_result = AppointmentsRepository.database.query(Appointments).filter(
                or_(Appointments.doctor_id == doctor_id, Appointments.patient_id == patient_id))
            query_result = query_result.all()
            try:  # Validation to check whether there is an appointment at same time
                for i in range(0, len(query_result)):
                    if query_result[i].appointment_start_time == start_time:
                        print("There is an appointment shceduled at same time.")
                        raise BaseException("Doctor or patient has similar appointment scheduled.")
                else:
                    AppointmentsRepository.database.add(new_appointment)
                    AppointmentsRepository.database.commit()
            except BaseException as e:
                AppointmentsRepository.database.rollback()
                error_message = e
                logging.error(error_message)
                raise BaseException(error_message)
        else:
            AppointmentsRepository.database.rollback()
            raise BaseException("Appointment Time must be of Future Time")

    @staticmethod
    def get_last_appointmnet():
        query_result = AppointmentsRepository.database.query(Appointments.appointment_id)
        query_result = query_result.all()
        # query_result=query_result.sort()
        print(query_result)
        length = len(query_result)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(query_result[length-1])
        if length == 0:
            return None
        else:
            return query_result[length - 1]

    @staticmethod
    def update_appointment(doctor_id, patient_id, old_time, new_time):
        try:
            appointment_time = datetime.strptime(new_time, '%Y-%m-%d %H:%M')
            current_time = str(datetime.now(timezone('US/Eastern')))
            current_time = current_time[:-16]
            current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M')
            if appointment_time > current_time:
                query_result = AppointmentsRepository.database.query(Appointments).filter(
                    or_(Appointments.doctor_id == doctor_id, Appointments.patient_id == patient_id))
                query_result = query_result.all()

                for i in range(0, len(query_result)):
                    if query_result[i].appointment_start_time == new_time:
                        print("There is an appointment shceduled at same time.")
                        raise BaseException("Doctor or patient has similar appointment scheduled.")
                else:
                    AppointmentsRepository.database.query(Appointments).filter(
                        and_(Appointments.patient_id == patient_id, Appointments.appointment_start_time == old_time)
                    ).update({"appointment_start_time": new_time})
                    print("Updating the Appointment")
                    AppointmentsRepository.database.commit()
            else:
                raise BaseException("Appointment Time must be of Future Time")
        except Exception as e:
            AppointmentsRepository.database.rollback()
            error_message = e
            logging.error(error_message)
            raise BaseException(error_message)

    @staticmethod
    def delete_appointment(doctor_id, patient_id, appointment_time):
        try:
            AppointmentsRepository.database.query(Appointments).filter(
                and_(Appointments.doctor_id == doctor_id, Appointments.patient_id == patient_id,
                     Appointments.appointment_start_time == appointment_time)
            ).delete()
            AppointmentsRepository.database.commit()
        except Exception as e:
            AppointmentsRepository.database.rollback()
            raise BaseException(e)

    @staticmethod
    def add_covid_questionnaire(user_id, name, email, age, has_cold, has_fever, has_cough, has_weakness,
                                has_sour_throat, has_body_pains, other_symptoms, covid_test, updated_at):
        try:
            # time1=datetime.now
            covid_details = CovidQuestionnaire(
                user_id=user_id,
                name=name,
                email=email,
                age=age,
                has_cold=has_cold,
                has_fever=has_fever,
                has_cough=has_cough,
                has_weakness=has_weakness,
                has_sour_throat=has_sour_throat,
                has_body_pains=has_body_pains,
                other_symptoms=other_symptoms,
                covid_test=covid_test,
                updated_at=updated_at
            )

            AppointmentsRepository.database.add(covid_details)
            AppointmentsRepository.database.commit()
        except Exception as e:
            AppointmentsRepository.database.rollback()
            raise BaseException(e)

    @staticmethod
    def get_covid_details(user_id):
        try:

            query_result = AppointmentsRepository.database.query(CovidQuestionnaire).filter(
                CovidQuestionnaire.user_id == user_id)
            query_result = query_result.all()
            return query_result

        except Exception as e:
            raise BaseException(e)

    @staticmethod
    def add_feedback_by_appointment(appointment_id, feedback_response):
        try:
            logging.info("feedback response format:", feedback_response)
            AppointmentsRepository.database.query(Appointments).filter(
                Appointments.appointment_id == appointment_id).update(
                {"appointment_attended": feedback_response.appointment_attended,
                 "feedback": feedback_response.feedback,
                 "rating": feedback_response.rating})
            AppointmentsRepository.database.commit()
            return {"message": f'updated feedback for doctor appointment id ={appointment_id}'}
        except Exception as e:
            AppointmentsRepository.database.rollback()
            error_message = f'error while adding feedback for appoinment id ={appointment_id}  : {e}'
            logging.info(e)
            raise BaseException(error_message)

    @staticmethod
    def get_all_appointmentsby_doctor_id(user_logged_id):
        try:
            user_id = str(user_logged_id)
            print("###############################################################################")
            query_result = AppointmentsRepository.database.query(Appointments).filter(Appointments.doctor_id == user_id)
            query_result = query_result.all()
            # AppointmentsRepository.database.commit()
            for i in query_result:
                print(i)
            return query_result
        except Exception as e:
            raise BaseException(e)

    @staticmethod
    def get_upcoming_appointments(user_id):
        try:
            search_word = '%covid_test%'
            query_result = AppointmentsRepository.database.query(Appointments).filter(
               and_(or_(Appointments.doctor_id == user_id, Appointments.patient_id == user_id), Appointments.appointment_id.not_ilike(search_word)))
            query_result = query_result.all()
            return query_result
        except Exception as e:
            raise BaseException(e)

    @staticmethod
    def get_covid_tests(user_id):
        try:
            search_word = '%covid_test%'
            query_result = AppointmentsRepository.database.query(Appointments).filter(and_(Appointments.patient_id==user_id,  Appointments.appointment_id.ilike(search_word)))
            tests = []
            for i in query_result:
                tests.append(i)
            return {"message" : tests}
        except BaseException as e:
            error_message = f'Error while fetching covid test for patient = {user_id}'
            logging.error(error_message)
            raise BaseException(error_message)

class ScheduleRepository:
    database: Session = get_db_actual()

    @staticmethod
    def get_schedule_id():
        query_result = ScheduleRepository.database.query(Schedule.schedule_id)
        query_result = query_result.all()
        # query_result=query_result.sort()
        print(query_result)
        length = len(query_result)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(query_result[length-1])
        if length == 0:
            return None
        else:
            return query_result[length - 1]

    @staticmethod
    def add_schedule(doctor_id, schedule_time, end_time, is_available):

        s_time = datetime.strptime(schedule_time, '%Y-%m-%d %H:%M')
        current_time = str(datetime.now(timezone('US/Eastern')))
        current_time = current_time[:-16]
        current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M')

        last_schedule_id = ScheduleRepository.get_schedule_id()
        print(last_schedule_id)
        if last_schedule_id == None or last_schedule_id == []:
            id = 1000
        else:
            last_schedule_id = str(last_schedule_id)
            b = ""
            for i in last_schedule_id:
                if i.isnumeric():
                    b = b + i
            print("######################################")
            print(b)
            id = int(b)
            id = id + 1

        new_id = id
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # print(new_id)
        if s_time > current_time:
            new_schedule = Schedule(
                schedule_id=new_id,
                doctor_id=doctor_id,
                schedule_start_date_time=schedule_time,
                schedule_end_date_time=end_time,
                is_available=is_available
            )
            query_result = ScheduleRepository.database.query(Schedule).filter(Schedule.doctor_id == doctor_id)
            query_result = query_result.all()
            print(query_result)
            try:  # Validation to check whether there is an existing entry at same time or not
                if len(query_result) > 0:
                    for i in range(0, len(query_result)):
                        print(query_result[i])
                        if query_result[i].schedule_start_date_time == schedule_time:
                            print("There is an existing slot at same time.")
                            raise BaseException("There is an existing slot at same time.")

                ScheduleRepository.database.add(new_schedule)
                print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
                ScheduleRepository.database.commit()
                return {'message': f'Added the new schedule for doctor {str(doctor_id)}'}
            except Exception as e:
                ScheduleRepository.database.rollback()
                raise BaseException(e)
        else:
            ScheduleRepository.database.rollback()
            raise BaseException("Schedule Time must be of Future Time")

    @staticmethod
    def get_schedule(doctor_id):
        try:
            query_result = ScheduleRepository.database.query(Schedule).filter(Schedule.doctor_id == doctor_id)
            query_result = query_result.all()
            # ScheduleRepository.database.commit()
            # logging.info("##########  Get Scedule", query_result[0])
            return query_result

        except BaseException as e:
            # ScheduleRepository.database.rollback()
            error_message = f'error while getting schedule for doctor id ={doctor_id}  : {e}'
            logging.info(e)
            raise BaseException(error_message)






