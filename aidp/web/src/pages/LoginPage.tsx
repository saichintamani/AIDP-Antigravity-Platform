import { Link } from 'react-router-dom';
import GlassCard from '../components/GlassCard';

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-[#3b82f6]/20 blur-[120px] pointer-events-none mix-blend-screen" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-[#e8702a]/20 blur-[120px] pointer-events-none mix-blend-screen" />
      
      <div className="w-full max-w-md z-10 hero-anim hero-fade">
        <GlassCard className="p-8 sm:p-10">
          <div className="text-center mb-8">
            <svg width="40" height="40" viewBox="0 0 256 256" fill="#e8702a" xmlns="http://www.w3.org/2000/svg" className="mx-auto mb-4">
              <path d="M 256 256 L 128 256 L 0 128 L 128 128 Z M 256 128 L 128 128 L 0 0 L 128 0 Z" />
            </svg>
            <h1 className="text-2xl font-semibold text-white mb-2 font-playfair italic">Welcome back</h1>
            <p className="text-sm text-white/50">Enter your credentials to access the workspace</p>
          </div>

          <form className="space-y-5" onSubmit={(e) => e.preventDefault()}>
            <div>
              <label className="block text-sm font-medium text-white/70 mb-1.5">Email Address</label>
              <input 
                type="email" 
                className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:border-[#e8702a]/50 focus:ring-1 focus:ring-[#e8702a]/50 transition-all"
                placeholder="scientist@institute.edu"
              />
            </div>
            <div>
              <div className="flex justify-between mb-1.5">
                <label className="block text-sm font-medium text-white/70">Password</label>
                <a href="#" className="text-sm text-[#e8702a] hover:text-[#d2611f] transition-colors">Forgot?</a>
              </div>
              <input 
                type="password" 
                className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:border-[#e8702a]/50 focus:ring-1 focus:ring-[#e8702a]/50 transition-all"
                placeholder="••••••••"
              />
            </div>
            <button className="w-full bg-[#e8702a] hover:bg-[#d2611f] text-white font-medium py-3 rounded-xl transition-all hover:scale-[1.02] active:scale-95 hover:shadow-lg hover:shadow-[#e8702a]/20 mt-2">
              Sign In
            </button>
          </form>

          <div className="mt-8 text-center text-sm text-white/50">
            Don't have an account? <Link to="/signup" className="text-white hover:text-[#e8702a] font-medium transition-colors">Request Access</Link>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
