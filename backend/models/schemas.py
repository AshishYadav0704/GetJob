from pydantic import BaseModel, Field
from typing import List, Optional

class WorkExperience(BaseModel):
    role: str = Field(description="The job title or position held.")
    company: str = Field(description="The name of the company.")
    duration: str = Field(description="The time period worked (e.g., 'Jan 2020 - Present').")
    bullet_points: List[str] = Field(description="Key achievements and responsibilities.")

class Education(BaseModel):
    degree: str = Field(description="The degree or certification obtained.")
    institution: str = Field(description="The name of the school or university.")
    year: str = Field(description="The graduation year or duration.")

class ResumeProfile(BaseModel):
    name: str = Field(description="The candidate's full name.")
    email: Optional[str] = Field(description="The candidate's email address if found.")
    skills: List[str] = Field(description="A comprehensive list of technical and soft skills extracted.")
    total_experience_years: int = Field(description="Calculated total years of professional experience.")
    work_history: List[WorkExperience] = Field(description="Chronological work history.")
    education: List[Education] = Field(description="Educational background.")
    summary: str = Field(description="A 2-3 sentence summary of the candidate's professional profile.")

#u
class JobMatchResult(BaseModel):
    match_score: int = Field(description="A score from 0 to 100 representing how well the candidate fits the job description.")
    matching_skills: List[str] = Field(description="Skills required by the job that the candidate already possesses.")
    missing_skills: List[str] = Field(description="Crucial skills required by the job that are missing from the candidate's resume.")
    recommendation: str = Field(description="A brief, 2-3 sentence explanation of why the candidate is or isn't a good fit, and what they should focus on learning next.")




    
    
