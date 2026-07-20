import { useState } from 'react';
import GlassCard from '../components/GlassCard';
import { Search, Loader2, Sparkles, ShieldCheck, Microscope } from 'lucide-react';
import { agents } from '../data/mockData';
import * as Icons from 'lucide-react';

export default function DiscoveryPage() {
  const [query, setQuery] = useState('');
  const [isDiscovering, setIsDiscovering] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    'Parsing research query...',
    'Querying Knowledge Graph...',
    'Generating hypotheses...',
    'Debating evidence (Adversarial critique)...',
    'Formally verifying experimental design...',
    'Finalizing discovery...'
  ];

  const handleDiscover = () => {
    if (!query) return;
    setIsDiscovering(true);
    setResult(null);
    setActiveStep(0);

    // Simulate multi-agent process
    let step = 0;
    const interval = setInterval(() => {
      step++;
      if (step < steps.length) {
        setActiveStep(step);
      } else {
        clearInterval(interval);
        setIsDiscovering(false);
        setResult({
          claim: "Targeting the newly discovered regulatory protein complex X can inhibit aggregation pathways in related pathologies.",
          confidence: "0.87 (High)",
          rationale: "Based on structural similarity derived from the Knowledge Graph and verified via formal debate against contemporary decoys.",
          domain: "WET_LAB",
          sampleSize: "N=200",
          controls: "Vehicle-only, Scrambled peptide, Standard-of-care"
        });
      }
    }, 1500);
  };

  return (
    <div className="p-6 md:p-10 max-w-7xl mx-auto hero-anim hero-fade">
      <header className="mb-10">
        <h1 className="text-3xl font-bold text-white font-playfair italic mb-2">Discovery Workspace</h1>
        <p className="text-white/60">Input a scientific domain or question to trigger the autonomous reasoning pipeline</p>
      </header>

      {/* Query Box */}
      <GlassCard className="mb-8 p-1">
        <div className="flex flex-col sm:flex-row gap-4 p-5">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-white/30" />
            </div>
            <input
              type="text"
              className="block w-full pl-12 pr-4 py-4 bg-black/40 border border-white/10 rounded-xl text-white placeholder-white/30 focus:outline-none focus:border-[#e8702a]/50 focus:ring-1 focus:ring-[#e8702a]/50 transition-all text-lg"
              placeholder="E.g. Can we use a synthetic peptide to inhibit aggregation..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleDiscover()}
              disabled={isDiscovering}
            />
          </div>
          <button
            onClick={handleDiscover}
            disabled={isDiscovering || !query}
            className="bg-[#e8702a] hover:bg-[#d2611f] disabled:opacity-50 disabled:hover:scale-100 disabled:cursor-not-allowed text-white font-semibold px-8 py-4 rounded-xl transition-all hover:scale-[1.02] active:scale-95 flex items-center justify-center gap-2"
          >
            {isDiscovering ? <Loader2 className="animate-spin" size={20} /> : <Sparkles size={20} />}
            {isDiscovering ? 'Reasoning...' : 'Discover'}
          </button>
        </div>
      </GlassCard>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Results Area */}
        <div className="lg:col-span-2 space-y-6">
          {isDiscovering && (
            <GlassCard className="border-[#3b82f6]/30 shadow-[0_0_30px_rgba(59,130,246,0.1)]">
              <h2 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                <Loader2 className="animate-spin text-[#3b82f6]" size={20} />
                Orchestrator Active
              </h2>
              <div className="space-y-4">
                {steps.map((s, i) => (
                  <div key={i} className={`flex items-center gap-3 transition-opacity duration-300 ${i === activeStep ? 'opacity-100' : i < activeStep ? 'opacity-50' : 'opacity-20'}`}>
                    <div className={`w-2 h-2 rounded-full ${i <= activeStep ? 'bg-[#3b82f6]' : 'bg-white'}`} />
                    <span className={`text-sm ${i === activeStep ? 'text-white font-medium' : 'text-white'}`}>{s}</span>
                  </div>
                ))}
              </div>
            </GlassCard>
          )}

          {result && !isDiscovering && (
            <div className="space-y-6 hero-anim hero-fade">
              <GlassCard className="border-[#22c55e]/30">
                <div className="flex items-center gap-2 mb-4">
                  <ShieldCheck className="text-[#22c55e]" size={24} />
                  <h2 className="text-xl font-semibold text-white">Generated Hypothesis</h2>
                </div>
                <div className="space-y-4 bg-black/40 p-5 rounded-xl border border-white/5">
                  <div>
                    <span className="text-xs text-white/50 uppercase tracking-wider">Claim</span>
                    <p className="text-white mt-1 text-lg">{result.claim}</p>
                  </div>
                  <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/10">
                    <div>
                      <span className="text-xs text-white/50 uppercase tracking-wider">Confidence (Calibrated)</span>
                      <p className="text-[#22c55e] mt-1 font-mono font-medium">{result.confidence}</p>
                    </div>
                    <div>
                      <span className="text-xs text-white/50 uppercase tracking-wider">Rationale Summary</span>
                      <p className="text-white/80 mt-1 text-sm">{result.rationale}</p>
                    </div>
                  </div>
                </div>
              </GlassCard>

              <GlassCard>
                <div className="flex items-center gap-2 mb-4">
                  <Microscope className="text-[#a855f7]" size={24} />
                  <h2 className="text-xl font-semibold text-white">Formal Experiment Design</h2>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div className="bg-black/40 p-4 rounded-xl border border-white/5">
                    <span className="text-xs text-white/50 uppercase tracking-wider block mb-1">Domain</span>
                    <span className="text-[#a855f7] font-mono text-sm">{result.domain}</span>
                  </div>
                  <div className="bg-black/40 p-4 rounded-xl border border-white/5">
                    <span className="text-xs text-white/50 uppercase tracking-wider block mb-1">Sample Size</span>
                    <span className="text-white text-sm">{result.sampleSize}</span>
                  </div>
                  <div className="bg-black/40 p-4 rounded-xl border border-white/5">
                    <span className="text-xs text-white/50 uppercase tracking-wider block mb-1">Controls</span>
                    <span className="text-white text-sm">{result.controls}</span>
                  </div>
                </div>
              </GlassCard>
            </div>
          )}

          {!isDiscovering && !result && (
            <div className="h-64 flex flex-col items-center justify-center border-2 border-dashed border-white/10 rounded-2xl text-white/30">
              <Search size={48} className="mb-4 opacity-50" />
              <p>Awaiting query input...</p>
            </div>
          )}
        </div>

        {/* Live Agents List */}
        <div>
          <GlassCard className="h-full">
            <h2 className="text-lg font-semibold text-white mb-6">Agent Roster</h2>
            <div className="space-y-4">
              {agents.map((agent, i) => {
                const IconComponent = (Icons as any)[agent.icon] || Icons.Bot;
                const isActive = agent.status === 'active' && isDiscovering;
                
                return (
                  <div key={i} className={`p-4 rounded-xl border transition-colors ${isActive ? 'bg-[#3b82f6]/10 border-[#3b82f6]/30' : 'bg-black/40 border-white/5'}`}>
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <IconComponent size={16} className={isActive ? 'text-[#3b82f6]' : 'text-white/50'} />
                        <h3 className={`text-sm font-medium ${isActive ? 'text-white' : 'text-white/70'}`}>{agent.name}</h3>
                      </div>
                      <span className="relative flex h-2 w-2">
                        {isActive && <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#3b82f6] opacity-75"></span>}
                        <span className={`relative inline-flex rounded-full h-2 w-2 ${isActive ? 'bg-[#3b82f6]' : agent.status === 'idle' ? 'bg-white/20' : 'bg-[#eab308]'}`}></span>
                      </span>
                    </div>
                    <p className="text-xs text-white/50 line-clamp-2">{agent.description}</p>
                  </div>
                );
              })}
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
