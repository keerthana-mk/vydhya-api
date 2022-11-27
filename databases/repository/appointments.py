import logging
from sqlalchemy import or_, and_
from datetime import datetime
from pytz import timezone
from databases.db_models.appointments import Appointments, Schedule, CovidQuestionnaire
from app.config import get_db_actual
from sqlalchemy.orm import Session
from models.appointments import UpdateAppointment
from models.logging import logger


class AppointmentsRepository:
    database: Session = get_db_actual()

    @staticmethod
    def add_appointment(appointment_id,doctor_id, patient_id, start_time, duration, feedback, rating, appointment_attended):
        logger.error("Creating Appointment - 3...")

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
            new_appointment=Appointemnts(
                appointment_id=new_appointment_id,
                doctor_id=doctor_id,
                patient_id=patient_id,
                appointment_start_time= start_time,
                duration=duration,
                feedback=feedback,
                rating=rating,
                appointment_attended=appointment_attended
            )
            query_result = AppointmentsRepository.database.query(Appointemnts).filter(
                or_(Appointemnts.doctor_id == doctor_id, Appointemnts.patient_id == patient_id))
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
                logger.error(error_message)
                raise BaseException(error_message)
        else:
            raise BaseException("Appointment Time must be of Future Time")


    @staticmethod
    def get_last_appointmnet():
        query_result = AppointmentsRepository.database.query(Appointemnts.appointment_id)
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
                query_result = AppointmentsRepository.database.query(Appointemnts).filter(
                    or_(Appointemnts.doctor_id == doctor_id, Appointemnts.patient_id == patient_id))
                query_result=query_result.all()

                for i in range(0,len(query_result)):
                    if query_result[i].appointment_start_time==new_time:
                        print("There is an appointment shceduled at same time.")
                        raise BaseException("Doctor or patient has similar appointment scheduled.")
                else:
                    AppointmentsRepository.database.query(Appointemnts).filter(
                        and_(Appointemnts.patient_id == patient_id,Appointemnts.appointment_start_time == old_time)
                        ).update({"appointment_start_time":new_time})
                    print("Updating the Appointment")
                    AppointmentsRepository.database.commit()
            else:
                raise BaseException("Appointment Time must be of Future Time")
        except Exception as e:
            error_message= e
            logger.error(error_message)
            raise BaseException(error_message)


    @staticmethod
    def delete_appointment(doctor_id, patient_id, appointment_time):
        try:
            AppointmentsRepository.database.query(Appointemnts).filter(
                and_(Appointemnts.doctor_id==doctor_id, Appointemnts.patient_id==patient_id, Appointemnts.appointment_start_time==appointment_time)
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