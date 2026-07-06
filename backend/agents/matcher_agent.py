import os
import json
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.models.schemas import JobMatchResult

# Load environment variables
load_dotenv()

def match_resume_to_job(resume_json: dict, job_description: str) -> dict:
    """Compares a parsed resume against a job description and returns an ATS match score."""
    
    # Initialize Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0
    )

    # Bind the LLM to our new Pydantic schema
    structured_llm = llm.with_structured_output(JobMatchResult)

    # Define the grading instructions
    prompt = PromptTemplate.from_template(
        """
        You are an expert Technical Recruiter and strict ATS (Applicant Tracking System).
        Compare the candidate's parsed resume data against the job description below.
        
        Candidate Profile (JSON):
        {resume_data}
        
        Job Description:
        {job_description}
        
        Analyze the fit carefully. Calculate a realistic match score (0-100) based on 
        overlapping skills, experience level, and role requirements. Identify exact matching 
        skills, list strictly missing skills, and provide a brief recommendation on how the 
        candidate can improve their chances.
        """
    )

    # Chain and execute
    chain = prompt | structured_llm
    
    print("AI is analyzing the match...")
    result = chain.invoke({
        "resume_data": json.dumps(resume_json),
        "job_description": job_description
    })
    
    return result.model_dump()

# --- Quick Test Block ---
if __name__ == "__main__":
    # We will simulate a parsed resume (like the one you generated earlier)
    mock_resume = {
        "name": "Ashish",
        "skills": ["React", "Tailwind CSS", "TypeScript", "Git", "GitHub", "HTML", "CSS"],
        "total_experience_years": 1,
        "work_history": [
            {
                "role": "Web Developer",
                "company": "Gram Panchayat Website Project",
                "duration": "Jan 2025 - Present",
                "bullet_points": ["Built a dynamic homepage with multiple village sections.", "Implemented modern UI using component-based layouts."]
            }
        ]
    }

    # A sample Job Description to test against
    sample_jd = """
    Position: Frontend Engineer
    
    We are looking for a highly motivated Frontend Engineer to build modern, responsive web applications.
    
    Requirements:
    - 1+ years of experience in web development.
    - Strong proficiency in React, TypeScript, and Tailwind CSS.
    - Solid understanding of version control using Git and GitHub.
    - Bonus: Experience with Node.js and AWS for backend integration.
    """

    print("\n--- Running Matcher Agent ---")
    match_results = match_resume_to_job(mock_resume, sample_jd)
    
    print(json.dumps(match_results, indent=2))