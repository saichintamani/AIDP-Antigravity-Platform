import { useState, useEffect } from 'react';
import { Terminal, Download, Code, ArrowRight } from 'lucide-react';

export default function AlignEvalPage() {
  const [terminalText, setTerminalText] = useState('');
  const fullText = '> pip install align-eval\n\nInstalling collected packages: align-eval\nSuccessfully installed align-eval-1.0.0\n\n> align-eval sample_case.json --output_dir ./surveys\n\n[AlignEval] Cryptographically seeding randomizer with case ID: DEMO_CASE_01\n[AlignEval] Shuffling candidate options to prevent ordering bias...\n[AlignEval] Success! Generated blinded survey: ./surveys/survey_demo_case_01.md';

  useEffect(() => {
    let currentText = '';
    let i = 0;
    
    // Simulate typing effect
    const interval = setInterval(() => {
      if (i < fullText.length) {
        currentText += fullText[i];
        setTerminalText(currentText);
        i++;
      } else {
        clearInterval(interval);
      }
    }, 20); // ms per character

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 md:p-10 max-w-5xl mx-auto hero-anim hero-fade">
      {/* Hero Section */}
      <div className="flex flex-col items-center text-center mb-16 mt-8">
        <div className="w-24 h-24 mb-6 rounded-2xl bg-black/50 border border-white/10 flex items-center justify-center shadow-[0_0_50px_rgba(232,112,42,0.15)] overflow-hidden">
          <img src="/align_eval_logo.png" alt="AlignEval Logo" className="w-full h-full object-cover" onError={(e) => { e.currentTarget.style.display='none' }} />
          <div className="absolute inset-0 flex items-center justify-center -z-10">
             <Code className="text-[#e8702a] opacity-50" size={40} />
          </div>
        </div>
        <h1 className="text-5xl font-bold text-white mb-4 tracking-tight">Align<span className="text-[#e8702a]">Eval</span></h1>
        <p className="text-xl text-white/60 max-w-2xl font-light">
          The zero-dependency, mathematically blinded evaluation platform. Eradicate hindsight bias and candidate ordering bias from your expert alignment surveys.
        </p>
        
        <div className="mt-8 flex gap-4">
          <button className="px-6 py-3 bg-[#e8702a] hover:bg-[#e8702a]/90 text-white rounded-full font-medium transition-colors shadow-lg shadow-[#e8702a]/20 flex items-center gap-2">
            <Download size={18} /> Download CLI
          </button>
          <button className="px-6 py-3 bg-white/5 hover:bg-white/10 border border-white/10 text-white rounded-full font-medium transition-colors flex items-center gap-2">
            Read Docs <ArrowRight size={18} />
          </button>
        </div>
      </div>

      {/* Terminal Demo */}
      <div className="mb-16">
        <div className="flex items-center justify-between mb-4 px-2">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <Terminal className="text-[#3b82f6]" size={20} /> Watch it run
          </h2>
          <span className="text-xs text-white/40 font-mono">align_eval.py v1.0.0</span>
        </div>
        
        <div className="w-full bg-[#0a0a0f] rounded-xl border border-white/10 shadow-2xl overflow-hidden relative">
          <div className="h-8 bg-white/5 border-b border-white/5 flex items-center px-4 gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
            <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
          </div>
          <div className="p-6 font-mono text-sm text-green-400 whitespace-pre-wrap min-h-[200px]">
            {terminalText}
            <span className="animate-pulse">_</span>
          </div>
        </div>
      </div>

      {/* Value Props */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl bg-black/40 border border-white/5">
          <h3 className="text-white font-medium mb-2">1. Define Case</h3>
          <p className="text-sm text-white/60">Drop historical evidence, constraints, and candidate hypotheses into a standard JSON schema.</p>
        </div>
        <div className="p-6 rounded-2xl bg-black/40 border border-white/5">
          <h3 className="text-white font-medium mb-2">2. Seed & Shuffle</h3>
          <p className="text-sm text-white/60">AlignEval cryptographically seeds the randomizer using the Case ID to eliminate ordering bias (e.g. Option C is always correct).</p>
        </div>
        <div className="p-6 rounded-2xl bg-black/40 border border-white/5">
          <h3 className="text-white font-medium mb-2">3. Extract Rationale</h3>
          <p className="text-sm text-white/60">Outputs a beautifully formatted, blinded Markdown survey ready to capture human domain expert consensus.</p>
        </div>
      </div>
    </div>
  );
}
