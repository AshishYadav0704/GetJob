import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# Define the path to your newly populated database
DB_DIR = "../vector_db"

def get_matching_jobs(query_text: str, k: int = 2) -> list:
    """
    Searches the Vector DB for the top 'k' jobs that match the query text.
    """
    
    # 1. Initialize the EXACT SAME embedding model used to create the DB
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    # 2. Connect to the existing Chroma database
    if not os.path.exists(DB_DIR):
        print("Database not found! Please run setup_db.py first.")
        return []

    vectorstore = Chroma(
        persist_directory=DB_DIR, 
        embedding_function=embeddings
    )
    
    # 3. Perform a similarity search
    print(f"Searching for the top {k} matching jobs...")
    results = vectorstore.similarity_search(query_text, k=k)
    
    # 4. Format the output
    matched_jobs = []
    for doc in results:
        matched_jobs.append({
            "job_id": doc.metadata.get("job_id"),
            "title": doc.metadata.get("title"),
            "content": doc.page_content
        })
        
    return matched_jobs

# --- Quick Test Block ---
if __name__ == "__main__":
    # We will simulate a search using a candidate's top skills
    # Since you build modern UIs with component-based layouts, let's search for that!
    sample_candidate_skills = "React, Tailwind CSS, TypeScript, building responsive and dynamic web interfaces."
    
    print(f"\n--- Querying DB for: '{sample_candidate_skills}' ---")
    
    top_jobs = get_matching_jobs(sample_candidate_skills, k=1)
    
    for i, job in enumerate(top_jobs):
        print(f"\nMatch #{i+1}: {job['title']} ({job['job_id']})")
        print("-" * 30)
        print(job['content'])