from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT
from databases.base_class import Base


class HealthcarePlans(Base):
    
    plan_id = Column(String, primary_key=True, index=True)
    insurer_id = Column(String, foreign_key=ForeignKey(InsurerProfile.user_id))
    plan_name = Column(String)
    premium = Column(FLOAT)
    coverage = Column(FLOAT)
    duration_years = Column(FLOAT)
    Deductible_amt = Column(FLOAT)
    isMonthly = Column(Boolean, default=True)
   