import { useState } from 'react';
import GlassCard from '../components/GlassCard';
import { BrainCircuit, Users, CheckCircle2 } from 'lucide-react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { validationData } from '../data/mockData';

export default function ValidationPage() {
  const [activeTab, setActiveTab] = useState<'human' | 'engine'>('human');

  return (
    <div className="p-6 md:p-10 max-w-7xl mx-auto hero-anim hero-fade">
      <header className="mb-10">
        <h1 className="text-3xl font-bold text-white font-playfair italic mb-2">Research Methodology Gates</h1>
        <p className="text-white/60">Formal verification of engine characterization and human evidence baselines.</p>
        <div className="mt-4 flex gap-3 text-sm">
           <span className="text-[#3b82f6] hover:underline cursor-pointer">View Historical Replay Report v1</span>
           <span className="text-[#22c55e] hover:underline cursor-pointer">View Engine Validation Report v1</span>
           <span className="text-[#ef4444] hover:underline cursor-pointer">View Failure Registry</span>
        </div>
      </header>

      {/* Tabs */}
      <div className="flex gap-4 mb-8">
        <button
          onClick={() => setActiveTab('human')}
          className={`px-6 py-3 rounded-full text-sm font-medium transition-all ${
            activeTab === 'human' ? 'bg-[#e8702a] text-white shadow-lg shadow-[#e8702a]/20' : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white'
          }`}
        >
          Gate 2: Human Pilot (R2)
        </button>
        <button
          onClick={() => setActiveTab('engine')}
          className={`px-6 py-3 rounded-full text-sm font-medium transition-all ${
            activeTab === 'engine' ? 'bg-[#3b82f6] text-white shadow-lg shadow-[#3b82f6]/20' : 'bg-white/5 text-white/60 hover:bg-white/10 hover:text-white'
          }`}
        >
          Gate 3: Scaled Simulation (R3)
        </button>
      </div>

      {activeTab === 'human' && (
        <div className="space-y-6 hero-anim">
          <GlassCard className="border-[#22c55e]/30">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <Users className="text-[#22c55e]" size={24} />
                <h2 className="text-xl font-semibold text-white">Human vs. Epistemic Engine Agreement</h2>
                <span className="px-2 py-0.5 bg-yellow-500/20 text-yellow-400 text-[10px] uppercase font-bold tracking-wider rounded border border-yellow-500/30">Simulated Data</span>
              </div>
              <span className="px-3 py-1 bg-[#22c55e]/10 text-[#22c55e] text-xs font-semibold rounded-full border border-[#22c55e]/20">N = 10 Scientists</span>
            </div>
            <p className="text-sm text-white/70 mb-8">
              Blinded evaluation across 10 historical paradigm shifts. The Epistemic Engine's generative confidence scores strongly correlate with expert human consensus.
            </p>
            
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={validationData.humanAgreement}>
                  <defs>
                    <linearGradient id="colorAI" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#e8702a" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#e8702a" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorHuman" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="case" stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px', backdropFilter: 'blur(10px)' }}
                    itemStyle={{ color: '#fff' }}
                  />
                  <Area type="monotone" dataKey="aiConfidence" name="AI Confidence %" stroke="#e8702a" strokeWidth={2} fillOpacity={1} fill="url(#colorAI)" />
                  <Area type="monotone" dataKey="humanConsensus" name="Human Consensus %" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#colorHuman)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </GlassCard>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
             <GlassCard className="border-[#ef4444]/20 bg-[#ef4444]/5">
                <h3 className="text-lg font-semibold text-white mb-4 text-[#ef4444]">Preserved Failures (Transparency)</h3>
                <p className="text-sm text-white/60 mb-4">
                  In accordance with our core cultural rule against narrative drift, we preserve all cases where the AI diverged from reality or human experts.
                </p>
                <div className="space-y-3">
                  <div className="p-3 bg-black/40 rounded-xl border border-white/5">
                    <span className="text-[#ef4444] text-xs font-mono mb-1 block">CASE-03: String Theory Prioritization</span>
                    <p className="text-sm text-white/80">Engine exhibited historical bias, falsely inflating probability mass for string theory over loop quantum gravity despite explicit structural penalties.</p>
                  </div>
                  <div className="p-3 bg-black/40 rounded-xl border border-white/5">
                    <span className="text-[#ef4444] text-xs font-mono mb-1 block">CASE-05: Room-Temp Superconductor</span>
                    <p className="text-sm text-white/80">False positive triggered by anomalous data in early literature. Failed to apply adequate epistemic discounting to non-replicated primary sources.</p>
                  </div>
                </div>
             </GlassCard>

             <GlassCard>
                <div className="flex items-center gap-2 mb-4">
                  <CheckCircle2 className="text-[#22c55e]" size={20} />
                  <h3 className="text-lg font-semibold text-white">Methodology Status</h3>
                </div>
                <div className="space-y-4 text-sm">
                  <div className="flex justify-between items-center py-2 border-b border-white/5">
                    <span className="text-white/60">Blinded Protocol</span>
                    <span className="text-[#22c55e] font-medium">Executed</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-white/5">
                    <span className="text-white/60">Agreement Statistics</span>
                    <span className="text-white font-medium">r = 0.89</span>
                  </div>
                  <div className="flex justify-between items-center py-2">
                    <span className="text-white/60">Prompt Configuration</span>
                    <span className="text-white font-mono bg-white/10 px-2 rounded">v1.2.0-FROZEN</span>
                  </div>
                </div>
             </GlassCard>
          </div>
        </div>
      )}

      {activeTab === 'engine' && (
        <div className="space-y-6 hero-anim">
           <GlassCard className="border-[#3b82f6]/30">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <BrainCircuit className="text-[#3b82f6]" size={24} />
                <h2 className="text-xl font-semibold text-white">Engine Characterization (Scaled)</h2>
                <span className="px-2 py-0.5 bg-yellow-500/20 text-yellow-400 text-[10px] uppercase font-bold tracking-wider rounded border border-yellow-500/30">Mock Architecture</span>
              </div>
            </div>
            <p className="text-sm text-white/70 mb-8">
              Generative evaluation across all 10 historical cases. Tracking uncertainty bounds and engine stability (Stability Index: 0.92, Constraint Sensitivity: 0.88).
            </p>
            
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={validationData.engineEntropy}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                  <XAxis dataKey="epoch" stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="rgba(255,255,255,0.3)" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px', backdropFilter: 'blur(10px)' }}
                    itemStyle={{ color: '#fff' }}
                  />
                  <Line type="monotone" dataKey="systemEntropy" name="System Entropy (Bits)" stroke="#3b82f6" strokeWidth={3} dot={false} activeDot={{ r: 6, fill: '#3b82f6' }} />
                  <Line type="monotone" dataKey="informationGain" name="Info Gain (EIG)" stroke="#a855f7" strokeWidth={3} dot={false} strokeDasharray="5 5" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </GlassCard>
        </div>
      )}
    </div>
  );
}
