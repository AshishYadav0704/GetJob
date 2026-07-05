import requests
import re

def clean_html(raw_html: str) -> str:
    """Removes HTML tags from the live job descriptions so the AI can read them cleanly."""
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html)

def fetch_live_jobs(skills: list, k: int = 2) -> list:
    """Fetches real, live remote jobs based on the candidate's top skill."""
    
    # Grab their top skill to search the live web (fallback to 'software' if empty)
    search_term = skills[0] if skills else "software"
    
    print(f"🌐 Fetching live remote jobs for: {search_term}...")
    url = f"https://remotive.com/api/remote-jobs?search={search_term}&limit={k}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        jobs = data.get("jobs", [])
        
        formatted_jobs = []
        for job in jobs[:k]:
            formatted_jobs.append({
                "job_id": str(job["id"]),
                "title": job["title"],
                "company": job["company_name"],
                "content": clean_html(job["description"])[:3000], # Trimmed to keep Gemini rate limits happy
                "apply_url": job["url"] # The actual link to apply!
            })
            
        return formatted_jobs
        
    except Exception as e:
        print(f"❌ Failed to fetch live jobs: {e}")
        return []