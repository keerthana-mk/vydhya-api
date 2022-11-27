from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT
from databases.base_class import Base
from uuid import uuid4, UUID

class AppointmentFeedback(Base):
    appointment_id = Column(String, primary_key = True, default= uuid4)
    doctor_id = Column(String, nullable=False)
    patient_id = Column(String, nullable=False)
    feedback = Column(String)
    rating = Column(FLOAT)
    submitted_at = Column(String, default=datetime.now().strftime('%y-%m-%d %H:%M:%S'))

