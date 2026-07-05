import json
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def generate_interview_response(resume_data: dict, job_title: str, job_description: str, user_message: str) -> str:
    """Simulates a hiring manager responding to a candidate during an interview."""
    
    # Initialize Gemini with a slightly higher temperature for conversational variety
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.7 
    )

    prompt = PromptTemplate.from_template(
        """
        You are a technical hiring manager interviewing a candidate for the "{job_title}" position.
        
        Candidate's Parsed Resume Data:
        {resume_data}
        
        Job Requirements:
        {job_description}
        
        The candidate just said: "{user_message}"
        
        Your Goal: 
        Respond directly to the candidate in the first person ("I", "we"). 
        Evaluate what they just said, and ask them a follow-up interview question based on their resume or the job requirements.
        Keep it conversational, highly realistic, professional, and strictly under 4 sentences. 
        Do not break character.
        """
    )

    chain = prompt | llm
    
    print(f"💬 Generating Hiring Manager response for {job_title}...")
    result = chain.invoke({
        "resume_data": json.dumps(resume_data),
        "job_title": job_title,
        "job_description": job_description,
        "user_message": user_message
    })
    
    return result.content