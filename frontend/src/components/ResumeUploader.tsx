import React, { useState, useRef } from 'react';
import { 
  UploadCloud, FileText, Loader2, 
  Target, AlertTriangle, Zap, Sparkles, 
  ExternalLink, MessageSquare, Send, X
} from 'lucide-react';

export default function ResumeUploader() {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [parsedData, setParsedData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  
  // Feature States
  const [generatingLetterFor, setGeneratingLetterFor] = useState<string | null>(null);
  const [coverLetters, setCoverLetters] = useState<Record<string, string>>({});
  
  // Chat States
  const [activeChat, setActiveChat] = useState<string | null>(null);
  const [chatMessages, setChatMessages] = useState<Record<string, {role: 'user' | 'ai', text: string}[]>>({});
  const [chatInput, setChatInput] = useState("");
  const [isSendingChat, setIsSendingChat] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => { e.preventDefault(); setIsDragging(true); };
  const handleDragLeave = () => setIsDragging(false);
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) validateAndSetFile(e.dataTransfer.files[0]);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) validateAndSetFile(e.target.files[0]);
  };

  const validateAndSetFile = (selectedFile: File) => {
    if (selectedFile.type !== 'application/pdf') {
      setError('Please upload a valid PDF file.');
      setFile(null);
      return;
    }
    setError(null);
    setFile(selectedFile);
    setParsedData(null); 
    setCoverLetters({});
    setChatMessages({});
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('https://getjob-q483.onrender.com/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      setParsedData(data);
    } catch (err) {
      console.error("Frontend Fetch Error:", err);
      setError('Failed to process resume. Check the browser console for details.');
    } finally {
      setIsUploading(false);
    }
  };

  const generateCoverLetter = async (job: any) => {
    setGeneratingLetterFor(job.job_id);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/generate-cover-letter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_data: parsedData.profile,
          job_title: job.job_title,
          job_description: job.raw_job_description
        }),
      });
      if (!response.ok) throw new Error("Failed to generate cover letter");
      const data = await response.json();
      setCoverLetters(prev => ({ ...prev, [job.job_id]: data.cover_letter }));
    } catch (err) {
      alert("Failed to generate cover letter.");
    } finally {
      setGeneratingLetterFor(null);
    }
  };

  const handleSendMessage = async (job: any) => {
    if (!chatInput.trim()) return;
    
    const userMsg = chatInput;
    setChatInput("");
    setIsSendingChat(true);

    // Immediately show user message in UI
    setChatMessages(prev => ({
      ...prev,
      [job.job_id]: [...(prev[job.job_id] || []), { role: 'user', text: userMsg }]
    }));

    try {
      const response = await fetch('http://127.0.0.1:8000/api/interview-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_data: parsedData.profile,
          job_title: job.job_title,
          job_description: job.raw_job_description,
          message: userMsg
        }),
      });
      
      if (!response.ok) throw new Error("Chat failed");
      const data = await response.json();
      
      // Add AI response to UI
      setChatMessages(prev => ({
        ...prev,
        [job.job_id]: [...(prev[job.job_id] || []), { role: 'ai', text: data.reply }]
      }));
    } catch (err) {
      console.error(err);
    } finally {
      setIsSendingChat(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 50) return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  return (
    <div className="w-full max-w-5xl mx-auto p-6">
      <div
        className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200 ease-in-out
          ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400 bg-white'}
          ${file ? 'bg-green-50 border-green-400' : ''} ${parsedData ? 'hidden' : 'block'}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input type="file" ref={fileInputRef} onChange={handleFileSelect} accept="application/pdf" className="hidden" />
        
        {!file ? (
          <div className="flex flex-col items-center cursor-pointer" onClick={() => fileInputRef.current?.click()}>
            <div className="p-4 bg-blue-100 rounded-full mb-4"><UploadCloud className="w-8 h-8 text-blue-600" /></div>
            <h3 className="text-lg font-semibold text-gray-800">Click or drag your resume here</h3>
            <p className="text-sm text-gray-500 mt-2">PDF format only (Max 5MB)</p>
          </div>
        ) : (
          <div className="flex flex-col items-center">
            <div className="p-4 bg-green-100 rounded-full mb-4"><FileText className="w-8 h-8 text-green-600" /></div>
            <h3 className="text-lg font-semibold text-gray-800">{file.name}</h3>
            <p className="text-sm text-gray-500 mt-2">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            <button onClick={() => setFile(null)} className="mt-4 text-sm text-red-500 hover:text-red-700 font-medium">Remove file</button>
          </div>
        )}
      </div>

      {error && <p className="mt-4 text-red-500 text-center font-medium">{error}</p>}

      {!parsedData && (
        <div className="mt-8 flex justify-center">
          <button
            onClick={handleUpload}
            disabled={!file || isUploading}
            className={`flex items-center gap-2 px-8 py-3 rounded-lg font-semibold text-white transition-all
              ${!file ? 'bg-gray-300 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 shadow-md hover:shadow-lg'}
              ${isUploading ? 'opacity-80 cursor-wait' : ''}`}
          >
            {isUploading ? <><Loader2 className="w-5 h-5 animate-spin" /> Fetching Live Jobs & Matching...</> : <><Zap className="w-5 h-5" /> Find Live Jobs</>}
          </button>
        </div>
      )}

      {parsedData && parsedData.profile && (
        <div className="mt-8 space-y-8 animate-fade-in-up">
          
          {/* PROFILE SECTION */}
          <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
            <div className="bg-slate-900 p-8 text-white flex justify-between items-center">
              <div>
                <h2 className="text-3xl font-extrabold">{parsedData.profile.name}</h2>
                <p className="text-slate-300 mt-1">{parsedData.profile.email || 'Email not provided'}</p>
              </div>
              <div className="text-right">
                <span className="text-4xl font-black text-blue-400">{parsedData.profile.total_experience_years}</span>
                <p className="text-slate-400 text-sm uppercase tracking-wider font-semibold">Years Exp.</p>
              </div>
            </div>
            <div className="p-8">
               <div className="flex flex-wrap gap-2 mb-4">
                  {parsedData.profile.skills.map((skill: string, i: number) => (
                    <span key={i} className="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm font-semibold rounded-lg border border-blue-100">
                      {skill}
                    </span>
                  ))}
               </div>
               <p className="text-gray-600">{parsedData.profile.summary}</p>
            </div>
          </div>

          {/* JOB MATCHES SECTION */}
          <div>
            <h2 className="text-2xl font-extrabold text-gray-900 mb-6 flex items-center gap-2">
              <Target className="w-7 h-7 text-blue-600" /> Real Live Job Matches
            </h2>
            <div className="grid grid-cols-1 gap-6">
              {parsedData.recommended_jobs.map((job: any, index: number) => (
                <div key={index} className="bg-white rounded-2xl shadow-md border border-gray-200 p-6 overflow-hidden relative">
                  
                  {/* Job Header */}
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-2xl font-bold text-gray-900">{job.job_title}</h3>
                      <p className="text-lg text-blue-600 font-semibold">{job.company}</p>
                    </div>
                    <div className={`px-4 py-2 rounded-xl border flex flex-col items-center justify-center min-w-[100px] ${getScoreColor(job.match_analysis.match_score)}`}>
                      <span className="text-2xl font-black">{job.match_analysis.match_score}%</span>
                      <span className="text-xs font-bold uppercase tracking-wider">Match</span>
                    </div>
                  </div>

                  <p className="text-sm text-gray-700 mb-6"><span className="font-bold text-gray-900">AI Notes:</span> {job.match_analysis.recommendation}</p>

                  {/* Missing Skills Warning */}
                  {job.match_analysis.missing_skills.length > 0 && (
                     <div className="mb-6 space-y-2">
                        <h4 className="text-sm font-bold text-gray-700 flex items-center gap-1.5">
                          <AlertTriangle className="w-4 h-4 text-amber-500" /> Missing Requirements (Learn these!)
                        </h4>
                        <div className="flex flex-wrap gap-1.5">
                           {job.match_analysis.missing_skills.map((skill: string, i: number) => (
                             <span key={i} className="px-2.5 py-1 bg-amber-50 text-amber-700 text-xs font-bold rounded-md border border-amber-200">{skill}</span>
                           ))}
                        </div>
                     </div>
                  )}

                  {/* ACTION BUTTONS */}
                  <div className="flex flex-wrap gap-3 pt-6 border-t border-gray-100">
                    <a 
                      href={job.apply_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white text-sm font-bold rounded-lg hover:bg-blue-700 transition shadow-sm"
                    >
                      Apply Now <ExternalLink className="w-4 h-4" />
                    </a>
                    
                    <button
                      onClick={() => generateCoverLetter(job)}
                      disabled={generatingLetterFor === job.job_id}
                      className="flex items-center gap-2 px-5 py-2.5 bg-white border border-gray-300 text-gray-700 text-sm font-semibold rounded-lg hover:bg-gray-50 transition shadow-sm"
                    >
                      {generatingLetterFor === job.job_id ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4 text-yellow-500" />} 
                      Draft Cover Letter
                    </button>

                    <button
                      onClick={() => setActiveChat(activeChat === job.job_id ? null : job.job_id)}
                      className={`flex items-center gap-2 px-5 py-2.5 text-sm font-semibold rounded-lg transition shadow-sm ${activeChat === job.job_id ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-200'}`}
                    >
                      <MessageSquare className="w-4 h-4" /> 
                      {activeChat === job.job_id ? 'Close Chat' : 'Practice Interview'}
                    </button>
                  </div>

                  {/* AI COVER LETTER UI */}
                  {coverLetters[job.job_id] && (
                    <div className="mt-6 bg-slate-50 border border-slate-200 rounded-xl p-6">
                      <h4 className="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                        <FileText className="w-5 h-5 text-blue-600" /> Custom Cover Letter
                      </h4>
                      <div className="whitespace-pre-wrap text-sm text-slate-700 leading-relaxed font-serif bg-white p-6 rounded-lg border border-slate-200 shadow-inner">
                        {coverLetters[job.job_id]}
                      </div>
                    </div>
                  )}

                  {/* AI INTERVIEW CHATBOT UI */}
                  {activeChat === job.job_id && (
                    <div className="mt-6 border border-slate-200 rounded-xl overflow-hidden bg-slate-50 flex flex-col h-96 shadow-inner animate-fade-in-up">
                      <div className="bg-slate-800 p-3 flex justify-between items-center text-white">
                        <span className="font-semibold text-sm flex items-center gap-2"><Target className="w-4 h-4 text-green-400"/> AI Hiring Manager: {job.company}</span>
                        <button onClick={() => setActiveChat(null)} className="hover:text-red-400"><X className="w-4 h-4" /></button>
                      </div>
                      
                      <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        <div className="bg-white border border-slate-200 text-slate-800 p-3 rounded-xl rounded-tl-none w-5/6 text-sm shadow-sm">
                          Hi {parsedData.profile.name.split(' ')[0]}! I'm the hiring manager for the {job.job_title} role at {job.company}. I reviewed your resume and would love to ask you a few questions. Are you ready?
                        </div>
                        
                        {(chatMessages[job.job_id] || []).map((msg, idx) => (
                          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`p-3 rounded-xl max-w-[85%] text-sm shadow-sm ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-white border border-slate-200 text-slate-800 rounded-tl-none'}`}>
                              {msg.text}
                            </div>
                          </div>
                        ))}
                        {isSendingChat && (
                           <div className="flex justify-start"><div className="p-3 bg-white border border-slate-200 rounded-xl rounded-tl-none text-slate-400 text-sm"><Loader2 className="w-4 h-4 animate-spin" /></div></div>
                        )}
                      </div>

                      <div className="p-3 bg-white border-t border-slate-200 flex gap-2">
                        <input 
                          type="text" 
                          value={chatInput} 
                          onChange={(e) => setChatInput(e.target.value)}
                          onKeyDown={(e) => e.key === 'Enter' && handleSendMessage(job)}
                          placeholder="Type your answer..." 
                          className="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                        />
                        <button 
                          onClick={() => handleSendMessage(job)}
                          disabled={!chatInput.trim() || isSendingChat}
                          className="bg-blue-600 text-white p-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                        >
                          <Send className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  )}
                  
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}