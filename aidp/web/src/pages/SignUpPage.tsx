import { Link } from 'react-router-dom';
import GlassCard from '../components/GlassCard';

export default function SignUpPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center p-4 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute top-[20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-[#a855f7]/20 blur-[120px] pointer-events-none mix-blend-screen" />
      <div className="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-[#e8702a]/20 blur-[120px] pointer-events-none mix-blend-screen" />
      
      <div className="w-full max-w-md z-10 hero-anim hero-fade">
        <GlassCard className="p-8 sm:p-10">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-semibold text-white mb-2 font-playfair italic">Request Access</h1>
            <p className="text-sm text-white/50">Join the AI Discovery Platform</p>
          </div>

          <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-white/70 mb-1.5">First Name</label>
                <input 
                  type="text" 
                  className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:border-[#e8702a]/50 focus:ring-1 focus:ring-[#e8702a]/50 transition-all"
                  placeholder="Marie"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-white/70 mb-1.5">Last Name</label>
                <input 
                  type="text" 
                  className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:border-[#e8702a]/50 focus:ring-1 focus:ring-[#e8702a]/50 transition-all"
                  placeholder="Curie"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-white/70 mb-1.5">Institution / Organization</label>
              <input 
                type="text" 
                className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:border-[#e8702a]/50 focus:ring-1 focus:ring-[#e8702a]/50 transition-all"
                placeholder="University of Science"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-white/70 mb-1.5">Work Email</label>
              <input 
                type="email" 
                className="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/30 focus:outline-none focus:border-[#e8702a]/50 focus:ring-1 focus:ring-[#e8702a]/50 transition-all"
                placeholder="m.curie@science.edu"
              />
            </div>
            <button className="w-full bg-[#e8702a] hover:bg-[#d2611f] text-white font-medium py-3 rounded-xl transition-all hover:scale-[1.02] active:scale-95 hover:shadow-lg hover:shadow-[#e8702a]/20 mt-4">
              Submit Request
            </button>
          </form>

          <div className="mt-8 text-center text-sm text-white/50">
            Already have access? <Link to="/login" className="text-white hover:text-[#e8702a] font-medium transition-colors">Sign In</Link>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}
