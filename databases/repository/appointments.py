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
    def add_appointment(appointment_id,doctor_id, patient_id, start_time, duration, feedback, rating, appointment_attended):
        logging.error("Creating Appointment - 3...")

        #Validation to check whether Appointment time is in future or not.
        appointment_time=datetime.strptime(start_time,'%Y-%m-%d %H:%M')
        current_time=str(datetime.now(timezone('US/Eastern')))
        current_time=current_time[:-16]
        current_time=datetime.strptime(current_time,'%Y-%m-%d %H:%M')
        if appointment_time>current_time:
            print("___________________________________________________________________")
            last_appointment_id=AppointmentsRepository.get_last_appointmnet()
            print(last_appointment_id)
            # last_appointment_id=str(last_appointment_id)
            if last_appointment_id==None:
                id=1000
            else:
                last_appointment_id=str(last_appointment_id)
                b=""
                for i in last_appointment_id:
                    if i.isnumeric():
                        b=b+i
                print(b)
                id=int(b)
                id=id+1

            new_appointment_id=id
            new_appointment=Appointments(
                appointment_id=new_appointment_id,
                doctor_id=doctor_id,
                patient_id=patient_id,
                appointment_start_time= start_time,
                duration=duration,
                feedback=feedback,
                rating=rating,
                appointment_attended=appointment_attended
            )
            query_result = AppointmentsRepository.database.query(Appointments).filter(
                or_(Appointments.doctor_id == doctor_id, Appointments.patient_id == patient_id))
            query_result=query_result.all()
            try: #Validation to check whether there is an appointment at same time
                for i in range(0,len(query_result)):
                    if query_result[i].appointment_start_time==start_time:
                        print("There is an appointment shceduled at same time.")
                        raise BaseException("Doctor or patient has similar appointment scheduled.")
                else:
                    AppointmentsRepository.database.add(new_appointment) 
                    AppointmentsRepository.database.commit()
            except BaseException as e:
                error_message= e
                logging.error(error_message)
                raise BaseException(error_message)
        else:
            raise BaseException("Appointment Time must be of Future Time")


    @staticmethod
    def get_last_appointmnet():
        query_result = AppointmentsRepository.database.query(Appointments.appointment_id)
        query_result = query_result.all()
        # query_result=query_result.sort()
        print(query_result)
        length=len(query_result)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # print(query_result[length-1])
        if length==0:
            return None
        else:
            return query_result[length-1]

   
    @staticmethod
    def update_appointment(doctor_id, patient_id, old_time, new_time):
        try:
            appointment_time=datetime.strptime(new_time,'%Y-%m-%d %H:%M')
            current_time=str(datetime.now(timezone('US/Eastern')))
            current_time=current_time[:-16]
            current_time=datetime.strptime(current_time,'%Y-%m-%d %H:%M')
            if appointment_time>current_time:
                query_result = AppointmentsRepository.database.query(Appointments).filter(
                    or_(Appointments.doctor_id == doctor_id, Appointments.patient_id == patient_id))
                query_result=query_result.all()

                for i in range(0,len(query_result)):
                    if query_result[i].appointment_start_time==new_time:
                        print("There is an appointment shceduled at same time.")
                        raise BaseException("Doctor or patient has similar appointment scheduled.")
                else:
                    AppointmentsRepository.database.query(Appointments).filter(
                        and_(Appointments.patient_id == patient_id,Appointments.appointment_start_time == old_time)
                        ).update({"appointment_start_time":new_time})
                    print("Updating the Appointment")
                    AppointmentsRepository.database.commit()
            else:
                raise BaseException("Appointment Time must be of Future Time")
        except Exception as e:
            error_message= e
            logging.error(error_message)
            raise BaseException(error_message)


    @staticmethod
    def delete_appointment(doctor_id, patient_id, appointment_time):
        try:
            AppointmentsRepository.database.query(Appointments).filter(
                and_(Appointments.doctor_id==doctor_id, Appointments.patient_id==patient_id, AppoAppointmentsintemnts.appointment_start_time==appointment_time)
                ).delete()
            AppointmentsRepository.database.commit()
        except Exception as e:
            raise BaseException(e)  

    @staticmethod
    def add_covid_questionnaire(user_id, name, email, age, has_cold, has_fever, has_cough, has_weakness, has_sour_throat, has_body_pains, other_symptoms, covid_test, updated_at):
        try:
            # time1=datetime.now
            covid_details=CovidQuestionnaire(
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
            raise BaseException(e)



    @staticmethod
    def get_covid_details(user_id):
        try:

            query_result= AppointmentsRepository.database.query(CovidQuestionnaire).filter(CovidQuestionnaire.user_id==user_id)
            query_result=query_result.all()
            return query_result
        
        except Exception as e:
            raise BaseException(e)
    @staticmethod
    def add_feedback_by_appointment(appointment_id, feedback_response):
        try:
            logging.info("feedback response format:",feedback_response)
            AppointmentsRepository.database.query(Appointments).filter(Appointments.appointment_id == appointment_id).update({"feedback": feedback_response.feedback,
                                                                                                                               "rating" : feedback_response.rating})
            AppointmentsRepository.database.commit()
            return {"message" : f'updated feedback for doctor appointment id ={appointment_id}'}
        except Exception as e:
            AppointmentsRepository.database.rollback()
            error_message = f'error while adding feedback for appoinment id ={appointment_id}  : {e}'
            logging.info(e)
            raise BaseException(error_message)
        
    @staticmethod
    def get_all_appointmentsby_doctor_id(user_logged_id):
        try:
            query_result = AppointmentsRepository.database.query(Appointments).filter(or_(Appointments.doctor_id == user_logged_id, Appointments.patient_id == user_logged_id)).all()
            return query_result
        except Exception as e:
            raise BaseException(e)