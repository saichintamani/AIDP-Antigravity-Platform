import StatCard from '../components/StatCard';
import GlassCard from '../components/GlassCard';
import { dashboardStats, milestones } from '../data/mockData';
import { ShieldCheck, Activity, BrainCircuit } from 'lucide-react';

export default function DashboardPage() {
  return (
    <div className="p-6 md:p-10 max-w-7xl mx-auto hero-anim hero-fade">
      <header className="mb-10">
        <h1 className="text-3xl font-bold text-white font-playfair italic mb-2">Platform Overview</h1>
        <p className="text-white/60">System status and autonomous discovery metrics</p>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
        {dashboardStats.map((stat, i) => (
          <StatCard key={i} {...stat} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Milestones */}
        <div className="lg:col-span-2 space-y-6">
          <GlassCard>
            <div className="flex items-center gap-3 mb-6">
              <ShieldCheck className="text-[#22c55e]" size={24} />
              <h2 className="text-xl font-semibold text-white">Project Maturity Gates</h2>
            </div>
            <div className="space-y-6">
              {milestones.map((milestone, idx) => (
                <div key={idx} className="flex gap-4">
                  <div className="flex flex-col items-center mt-1">
                    <div className={`w-3 h-3 rounded-full ${
                      milestone.status === 'completed' ? 'bg-[#22c55e] shadow-[0_0_10px_#22c55e]' : 
                      milestone.status === 'pending' ? 'bg-[#eab308] shadow-[0_0_10px_#eab308]' : 'bg-white/20'
                    }`} />
                    {idx !== milestones.length - 1 && <div className="w-0.5 h-full bg-white/10 my-2" />}
                  </div>
                  <div>
                    <h3 className="text-white font-medium mb-1">{milestone.name}</h3>
                    <p className="text-sm text-white/50">{milestone.notes}</p>
                  </div>
                </div>
              ))}
            </div>
          </GlassCard>

          <GlassCard>
            <div className="flex items-center gap-3 mb-6">
              <BrainCircuit className="text-[#e8702a]" size={24} />
              <h2 className="text-xl font-semibold text-white">Epistemic Engine Status</h2>
            </div>
            <p className="text-sm text-white/60 leading-relaxed mb-4">
              The core epistemic engine is fully operational. Information Theory and Subjective Logic frameworks are running on AWS EKS. The system is actively pruning logically fallacious reasoning paths in real-time.
            </p>
            <div className="flex gap-3">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#3b82f6]/20 text-[#3b82f6] text-xs font-medium border border-[#3b82f6]/30">
                <Activity size={12} /> Graph Traversal: Optimal
              </span>
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#22c55e]/20 text-[#22c55e] text-xs font-medium border border-[#22c55e]/30">
                <Activity size={12} /> Ledger: Immutable
              </span>
            </div>
          </GlassCard>
        </div>

        {/* System Health */}
        <div className="space-y-6">
          <GlassCard>
            <h2 className="text-xl font-semibold text-white mb-6">System Health</h2>
            <div className="space-y-4">
              {[
                { label: 'API Gateway', status: 'Healthy', color: '#22c55e' },
                { label: 'Reasoning Cluster (EKS)', status: 'Healthy', color: '#22c55e' },
                { label: 'Vector Database', status: 'Healthy', color: '#22c55e' },
                { label: 'Knowledge Graph', status: 'Healthy', color: '#22c55e' },
                { label: 'Epistemic Ledger', status: 'Synced', color: '#3b82f6' },
              ].map((sys, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-black/40 border border-white/5">
                  <span className="text-sm text-white/70">{sys.label}</span>
                  <span className="text-xs font-medium px-2 py-1 rounded bg-white/5" style={{ color: sys.color }}>
                    {sys.status}
                  </span>
                </div>
              ))}
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
}
