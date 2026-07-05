import os
import json
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def generate_cover_letter(resume_json: dict, job_title: str, job_description: str) -> str:
    """Generates a tailored cover letter using the parsed resume and job description."""
    
    # Initialize Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.7 # Slightly higher temperature for more natural, creative writing
    )

    prompt = PromptTemplate.from_template(
        """
        You are an expert career coach writing a highly effective, professional cover letter.
        
        Candidate Information:
        {resume_data}
        
        Target Job Title: {job_title}
        Target Job Description:
        {job_description}
        
        Write a concise, compelling cover letter (max 3 paragraphs) from the candidate to the hiring manager. 
        Focus strictly on how the candidate's existing skills and experience make them a great fit for the role. 
        Do not invent or hallucinate any experience that is not in the candidate's profile.
        Keep the tone professional, confident, and modern.
        """
    )

    chain = prompt | llm
    
    print(f"Drafting cover letter for {job_title}...")
    result = chain.invoke({
        "resume_data": json.dumps(resume_json),
        "job_title": job_title,
        "job_description": job_description
    })
    
    return result.content