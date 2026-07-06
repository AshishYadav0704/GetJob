import os
import pdfplumber
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.models.schemas import ResumeProfile

# Load environment variables (your Google API Key)
load_dotenv()

def extract_text_from_pdf(pdf_path: str) -> str:
    """Reads a PDF file and extracts all text."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def parse_resume(pdf_path: str) -> dict:
    """Extracts text from a resume PDF and parses it into structured JSON using Gemini."""
    
    # 1. Extract raw text
    resume_text = extract_text_from_pdf(pdf_path)
    if not resume_text:
        return {"error": "Could not extract text from the provided PDF."}

    # 2. Initialize Gemini 2.5 Flash
    # We use temperature=0 because we want factual extraction, not creative writing.
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0
    )

    # 3. Bind the LLM to our Pydantic schema
    # This forces Gemini to output the exact JSON structure we defined in schemas.py
    structured_llm = llm.with_structured_output(ResumeProfile)

    # 4. Define the instructions
    prompt = PromptTemplate.from_template(
        """
        You are an expert technical recruiter and resume parser. 
        Extract the requested information from the raw resume text provided below.
        Be precise. Calculate the total years of experience accurately based on the dates provided.
        
        Raw Resume Text:
        {resume_text}
        """
    )

    # 5. Chain them together and execute
    chain = prompt | structured_llm
    
    print("Sending text to Gemini for parsing...")
    result = chain.invoke({"resume_text": resume_text})
    
    # Return the Pydantic object as a standard Python dictionary
    return result.model_dump()

# --- Quick Test Block ---
# If you run this file directly, it will test the extraction.
if __name__ == "__main__":
    # Create a dummy pdf or place a real resume in the backend folder named 'test_resume.pdf'
    test_pdf = "test_resume.pdf" 
    
    if os.path.exists(test_pdf):
        parsed_data = parse_resume(test_pdf)
        print("\n--- Extracted JSON ---")
        import json
        print(json.dumps(parsed_data, indent=2))
    else:
        print(f"To test this script, place a PDF named '{test_pdf}' in the backend folder.")