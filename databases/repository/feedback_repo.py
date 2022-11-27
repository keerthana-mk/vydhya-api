import logging

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from databases.db_connection import get_db_actual
from databases.db_models.appointment_feedback import AppointmentFeedback
from databases.db_models.appointments import Appointments
from models import commons
class AppointmentFeedbackRepository:
    database: Session = get_db_actual()
    
    @staticmethod
    def create_feedback(doctor_id, patient_id,feedback_request_details):
        try:
            new_feedback =  AppointmentFeedback(
                doctor_id = doctor_id,
                patient_id = patient_id,
                feedback = feedback_request_details.feedback,
                rating = feedback_request_details.rating
            )
         
            AppointmentFeedbackRepository.database.add(new_feedback)
            AppointmentFeedbackRepository.database.commit()
            return {"message": f"Feedback for doctor {doctor_id} added successfully"}
        except Exception as e:
            AppointmentFeedbackRepository.database.rollback()
            error_message = f'error while inserting doctor feedback into database: {str(e)}'
            raise Exception(error_message)
        
    @staticmethod
    def fetch_feedback_by_doctor(doctor_id):
        feedback_query =  AppointmentFeedbackRepository.database.query(AppointmentFeedback).filter(
            (AppointmentFeedback.doctor_id == doctor_id)).all()
        feedback_query_sum =  AppointmentFeedbackRepository.database.query(func.avg(AppointmentFeedback.rating)).filter(
            (AppointmentFeedback.doctor_id == doctor_id))
        feedback_query_sum = feedback_query_sum.scalar()
        doctor_feedbacks =[]
        for f in feedback_query:
            doctor_feedbacks.append(commons.generate_feedback_response(f))
        return {doctor_id : doctor_feedbacks, "total rating " : feedback_query_sum}
            
    
            