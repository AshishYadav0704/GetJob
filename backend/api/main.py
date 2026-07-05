import os
import shutil
import traceback
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends
from database import engine, Base, get_db
from db_models import Candidate

# Import our four powerhouse agents
from agents.resume_agent import parse_resume
#from rag.retriever import get_matching_jobs
from rag.live_jobs import fetch_live_jobs
from agents.matcher_agent import match_resume_to_job
from agents.cover_letter_agent import generate_cover_letter
from agents.interview_agent import generate_interview_response

app = FastAPI(title="GetJob API")
# Create the database tables automatically
Base.metadata.create_all(bind=engine)

# Allow the React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "../documents"

# --- Data Models ---
class InterviewChatRequest(BaseModel):
    resume_data: dict
    job_title: str
    job_description: str
    message: str





class CoverLetterRequest(BaseModel):
    resume_data: dict
    job_title: str
    job_description: str


@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # --- NEW: Safely create the directory if it is missing ---
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # Save the uploaded file temporarily
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # --- STEP 1: Parse the Resume ---
        print("\n[1/4] Parsing Resume...")
        profile = parse_resume(file_path)
        os.remove(file_path) # Clean up the PDF immediately
        
        # --- STEP 2: Generate Vector Query ---
        print("[2/4] Generating vector query from skills...")
        skills_str = ", ".join(profile.get("skills", []))
        
       # --- STEP 3: Fetch LIVE Jobs from the Web ---
        print("[3/4] Searching the web for real job postings...")
        # Pass the skills list directly to our new live fetcher
        retrieved_jobs = fetch_live_jobs(profile.get("skills", []), k=2)
        
        if not retrieved_jobs:
            raise Exception("Could not find any live jobs matching those skills right now.")
            
        # --- STEP 4: Match and Grade ---
        print("[4/4] AI is grading the job matches...")
        recommendations = []
        for job in retrieved_jobs:
            match_result = match_resume_to_job(profile, job["content"])
            
            recommendations.append({
                "job_title": job["title"],
                "job_id": job["job_id"],
                "company": job["company"],       # NEW: Passing company name
                "apply_url": job["apply_url"],   # NEW: Passing the real application link
                "match_analysis": match_result,
                "raw_job_description": job["content"] 
            })
            
            time.sleep(3)
        print("Pipeline Complete! Sending payload to frontend.")
        
        return {
            "profile": profile,
            "recommended_jobs": recommendations
        }
    
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
            
        # --- NEW: Print exact crash logs to terminal ---
        print(f"\n❌ BACKEND CRASHED: {str(e)}")
        traceback.print_exc()
        
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-cover-letter")
async def create_cover_letter(request: CoverLetterRequest):
    """Takes a parsed resume and a job description and generates a tailored cover letter."""
    try:
        letter = generate_cover_letter(
            resume_json=request.resume_data,
            job_title=request.job_title,
            job_description=request.job_description
        )
        return {"cover_letter": letter}
    except Exception as e:
        print(f"\n❌ COVER LETTER AGENT CRASHED: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/api/interview-chat")
async def chat_with_hiring_manager(request: InterviewChatRequest):
    """Handles real-time interview practice with the AI hiring manager."""
    try:
        reply = generate_interview_response(
            resume_data=request.resume_data,
            job_title=request.job_title,
            job_description=request.job_description,
            user_message=request.message
        )
        return {"reply": reply}
    except Exception as e:
        import traceback
        print(f"\n❌ INTERVIEW AGENT CRASHED: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "GetJob API is active and listening!"}