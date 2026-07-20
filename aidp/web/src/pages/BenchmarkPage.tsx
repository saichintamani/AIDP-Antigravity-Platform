import GlassCard from '../components/GlassCard';
import { benchmarkCases, summaryMetrics } from '../data/mockData';
import { CheckCircle2, TrendingUp, HelpCircle } from 'lucide-react';

export default function BenchmarkPage() {
  return (
    <div className="p-6 md:p-10 max-w-7xl mx-auto hero-anim hero-fade">
      <header className="mb-10">
        <h1 className="text-3xl font-bold text-white font-playfair italic mb-2">Historical Replay Benchmarks</h1>
        <p className="text-white/60">Evaluating whether AIDP can prioritize historically correct paradigm shifts over plausible decoys.</p>
      </header>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
        <GlassCard className="flex items-center gap-4">
          <div className="p-4 rounded-full bg-[#22c55e]/10">
            <CheckCircle2 className="text-[#22c55e]" size={28} />
          </div>
          <div>
            <div className="text-sm text-white/60">Pass Rate</div>
            <div className="text-2xl font-bold text-white">{summaryMetrics.passRate}</div>
          </div>
        </GlassCard>
        <GlassCard className="flex items-center gap-4">
          <div className="p-4 rounded-full bg-[#3b82f6]/10">
            <TrendingUp className="text-[#3b82f6]" size={28} />
          </div>
          <div>
            <div className="text-sm text-white/60">Median Percentile Rank</div>
            <div className="text-2xl font-bold text-white">{summaryMetrics.medianPercentile.toFixed(1)}</div>
          </div>
        </GlassCard>
        <GlassCard className="flex items-center gap-4">
          <div className="p-4 rounded-full bg-[#a855f7]/10">
            <HelpCircle className="text-[#a855f7]" size={28} />
          </div>
          <div>
            <div className="text-sm text-white/60">Confidence Level</div>
            <div className="text-xl font-bold text-white">{summaryMetrics.confidenceLevel}</div>
          </div>
        </GlassCard>
      </div>

      {/* Table */}
      <GlassCard className="overflow-x-auto p-0 border-0">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-white/5 border-b border-white/10">
              <th className="py-4 px-6 text-xs font-semibold text-white/50 uppercase tracking-wider">Case ID / Domain</th>
              <th className="py-4 px-6 text-xs font-semibold text-white/50 uppercase tracking-wider">Timeframe</th>
              <th className="py-4 px-6 text-xs font-semibold text-white/50 uppercase tracking-wider">AIDP Status</th>
              <th className="py-4 px-6 text-xs font-semibold text-white/50 uppercase tracking-wider">Ranks (AIDP vs Baseline)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5">
            {benchmarkCases.map((c) => (
              <tr key={c.id} className="hover:bg-white/[0.02] transition-colors">
                <td className="py-4 px-6">
                  <div className="font-medium text-white mb-1">{c.id}</div>
                  <div className="text-xs text-[#e8702a]">{c.domain}</div>
                </td>
                <td className="py-4 px-6">
                  <span className="text-sm text-white/70 font-mono">{c.yearRange}</span>
                </td>
                <td className="py-4 px-6">
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#22c55e]/10 text-[#22c55e] text-xs font-semibold border border-[#22c55e]/20">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#22c55e]"></div>
                    {c.status}
                  </span>
                  <div className="text-xs text-white/40 mt-2 ml-1">Top {(100 - c.percentile) || 10}%</div>
                </td>
                <td className="py-4 px-6">
                  <div className="flex flex-col gap-1 text-sm">
                    <div className="flex items-center justify-between gap-4">
                      <span className="text-white/60">AIDP:</span>
                      <span className="text-white font-mono">{c.aidpRank}</span>
                    </div>
                    <div className="flex items-center justify-between gap-4">
                      <span className="text-white/60">Baseline:</span>
                      <span className="text-white/40 font-mono">{c.baselineRank}</span>
                    </div>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </GlassCard>
    </div>
  );
}
