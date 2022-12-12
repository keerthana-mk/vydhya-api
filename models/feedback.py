from typing import Union, Optional

from pydantic import BaseModel
from pydantic.fields import List


# class AppointmentFeedback(Base):
#     appointment_id = Column(String, primary_key = True)
#     doctor_id = Column(String, nullable=False)
#     patient_id = Column(String, nullable=False)
#     feedback = Column(String)
#     rating = Column(FLOAT)
#     submitted_at = Column(String, default=datetime.now().strftime('%y-%m-%d %H:%M:%S'))

class FeedbackRequest(BaseModel):
    appointment_attended : Optional[Union[bool,None]] = False
    feedback : Union[str, None]
    rating : float
    
    