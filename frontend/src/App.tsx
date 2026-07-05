import { Briefcase } from 'lucide-react';
import ResumeUploader from './components/ResumeUploader';

function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          
          {/* --- NEW STARTUP LOGO --- */}
          <div className="flex items-center gap-3 select-none">
            <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 shadow-lg shadow-blue-500/30">
              <Briefcase className="w-6 h-6 text-white absolute z-10" strokeWidth={2.5} />
              <div className="absolute inset-0 rounded-xl bg-white opacity-20 blur-sm"></div>
            </div>
            <h1 className="text-2xl font-black tracking-tight text-slate-900 flex items-baseline">
              Get<span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Job</span>
              <span className="w-2 h-2 rounded-full bg-blue-500 ml-1 mb-1"></span>
            </h1>
          </div>

        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-center py-12 px-4 sm:px-6">
        <div className="text-center mb-10">
          <h2 className="text-4xl font-extrabold text-gray-900 sm:text-5xl">
            Upload your resume.
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Land your dream job.</span>
          </h2>
          <p className="mt-4 text-xl text-gray-500 max-w-2xl mx-auto">
            Our AI instantly parses your experience and matches you with roles that fit your exact skill set.
          </p>
        </div>

        <ResumeUploader />
      </main>
    </div>
  );
}

export default App;