from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT
from databases.base_class import Base
from databases.db_models.profiles import InsurerProfile

class HealthcarePlan(Base):
    plan_id = Column(String, primary_key=True, index=True)
    insurer_id = Column(String, foreign_key=ForeignKey(InsurerProfile.user_id))
    plan_name = Column(String)
    plan_display_name = Column(String)
    plan_description = Column(String)
    plan_exceptions = Column(ARRAY(String))
    premium = Column(FLOAT)
    coverage = Column(FLOAT)
    duration_years = Column(FLOAT)
    deductible_amt = Column(FLOAT)
    is_monthly = Column(Boolean, default=True)