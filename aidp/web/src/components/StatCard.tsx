import * as Icons from 'lucide-react';
import AnimatedCounter from './AnimatedCounter';

interface StatCardProps {
  label: string;
  value: number;
  suffix?: string;
  icon: string;
  color: string;
}

export default function StatCard({ label, value, suffix = '', icon, color }: StatCardProps) {
  const IconComponent = (Icons as any)[icon] || Icons.Activity;

  return (
    <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 transition-all duration-300 hover:bg-white/10 hover:border-white/20 hover:scale-[1.02] group">
      <div className="flex items-start justify-between mb-4">
        <div className="p-3 rounded-xl" style={{ backgroundColor: `${color}15` }}>
          <IconComponent size={24} className="transition-colors" style={{ color }} />
        </div>
        <div className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: color }} />
      </div>
      <div className="text-3xl font-bold text-white mb-1">
        <AnimatedCounter target={value} suffix={suffix} />
      </div>
      <div className="text-sm text-white/50">{label}</div>
    </div>
  );
}
