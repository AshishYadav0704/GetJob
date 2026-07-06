from sqlalchemy import Column, Integer, String, JSON
from backend.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    
    # We can store the entire list of skills directly as JSON!
    skills = Column(JSON) 
    
    summary = Column(String)
    total_experience_years = Column(Integer)