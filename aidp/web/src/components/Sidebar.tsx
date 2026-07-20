import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Search, BarChart3, Network, LogOut, ChevronLeft, ChevronRight, ShieldCheck, Database, Layers, Code } from 'lucide-react';
import { motion } from 'framer-motion';
import { cn } from '../lib/utils';

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/discover', label: 'Discovery', icon: Search },
  { id: 'benchmarks', label: 'Benchmarks', icon: Database, path: '/benchmarks' },
  { id: 'architecture', label: 'Architecture', icon: Layers, path: '/architecture' },
  { id: 'validation', label: 'Validation', icon: ShieldCheck, path: '/validation' },
  { id: 'align-eval', label: 'AlignEval', icon: Code, path: '/align-eval' },
];

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

export default function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const location = useLocation();

  return (
    <aside className={`fixed left-0 top-0 h-screen z-40 flex flex-col bg-[#0d0d14]/95 backdrop-blur-xl border-r border-white/5 transition-all duration-300 ${collapsed ? 'w-[72px]' : 'w-[240px]'}`}>
      {/* Logo */}
      <Link to="/" className="flex items-center gap-3 px-5 py-5 border-b border-white/5">
        <svg width="28" height="28" viewBox="0 0 256 256" fill="#e8702a" xmlns="http://www.w3.org/2000/svg">
          <path d="M 256 256 L 128 256 L 0 128 L 128 128 Z M 256 128 L 128 128 L 0 0 L 128 0 Z" />
        </svg>
        {!collapsed && <span className="text-white text-lg font-semibold tracking-tight">AIDP</span>}
      </Link>

      {/* Nav items */}
      <nav className="flex-1 py-4 px-3 space-y-1">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          const Icon = item.icon;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                "relative flex items-center gap-4 px-3 py-3 rounded-xl transition-colors group",
                isActive ? "text-white" : "text-white/50 hover:text-white"
              )}
            >
              {isActive && (
                <motion.div
                  layoutId="sidebar-active"
                  className="absolute inset-0 bg-white/10 rounded-xl"
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
              <Icon size={22} className="relative z-10 min-w-[22px]" />
              {!collapsed && <span className="relative z-10 text-sm font-medium">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Bottom */}
      <div className="px-3 py-4 border-t border-white/5 space-y-1">
        <Link to="/" className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-white/50 hover:text-white hover:bg-white/5 transition-all">
          <LogOut size={20} />
          {!collapsed && <span>Sign Out</span>}
        </Link>
        <button onClick={onToggle} className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-white/30 hover:text-white/60 transition-all w-full">
          {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
          {!collapsed && <span>Collapse</span>}
        </button>
      </div>
    </aside>
  );
}
