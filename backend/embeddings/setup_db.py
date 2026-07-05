import json
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Load environment variables (API Key)
load_dotenv()

# Define paths relative to the backend folder
DB_DIR = "../vector_db"
JOBS_FILE = "../documents/jobs.json"

def populate_database():
    """Reads jobs from JSON, embeds them, and stores them in ChromaDB."""
    
    # 1. Load the job descriptions
    if not os.path.exists(JOBS_FILE):
        print(f"Error: Could not find {JOBS_FILE}")
        return

    with open(JOBS_FILE, "r") as f:
        jobs = json.load(f)

    # 2. Convert JSON into LangChain Document objects
    documents = []
    for job in jobs:
        # We combine the title, description, and requirements into one searchable string
        content = f"Title: {job['title']}\nDescription: {job['description']}\nRequirements: {', '.join(job['requirements'])}"
        
        # Metadata allows us to easily retrieve the job details later
        doc = Document(
            page_content=content, 
            metadata={"job_id": job["id"], "title": job["title"]}
        )
        documents.append(doc)

    # 3. Initialize Gemini's free-tier Embedding Model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    # 4. Create and persist the Vector Database
    print(f"Embedding {len(documents)} jobs and saving to ChromaDB...")
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    
    print("Success! Vector DB successfully populated and stored in the vector_db/ folder.")

if __name__ == "__main__":
    populate_database()