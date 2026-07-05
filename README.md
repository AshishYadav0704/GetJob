# GetJob AI 🚀

GetJob AI is an intelligent career companion that bridges the gap between your resume and real-world opportunities. It doesn't just parse PDFs; it analyzes your professional profile, fetches live remote job postings, and connects you with an AI-driven Hiring Manager for real-time interview preparation.

## 🌟 Key Features
- **AI-Powered Resume Analysis**: Automatically extract skills, experience, and professional summaries.
- **Live Job Aggregator**: Fetches real-time job opportunities based on your unique skill set.
- **Dynamic AI Interviewer**: Practice your technical and behavioral interviews with an agent that knows the specific job requirements.
- **Smart Cover Letter Drafting**: Generate tailored, persuasive cover letters in seconds.
- **Candidate Database**: Persistent storage to track your applications and profile progression.

## 🛠 Tech Stack
- **Frontend**: React, TypeScript, Tailwind CSS, Lucide Icons
- **Backend**: FastAPI, Python 3.13
- **AI/LLM**: Google Gemini 2.5-Flash via LangChain
- **Database**: SQLite (SQLAlchemy ORM)

## 🚀 How to Run
1. **Clone the repo**: `git clone <your-repo-link>`
2. **Setup Backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn api.main:app --reload
3.**Setup Frontend**:
```bash
cd frontend
npm install
npm run dev


@ Built with passion by Ashish Kumar Yadav
