import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X } from 'lucide-react';

interface NavbarProps {
  showAuth?: boolean;
}

export default function Navbar({ showAuth = true }: NavbarProps) {
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const location = useLocation();
  const isLanding = location.pathname === '/';

  return (
    <nav className={`fixed top-0 left-0 right-0 z-[100] flex items-center justify-between p-4 sm:p-5 ${isLanding ? '' : 'bg-[#0a0a0f]/80 backdrop-blur-xl border-b border-white/5'}`}>
      <Link to="/" className="flex items-center gap-2">
        <svg width="26" height="26" viewBox="0 0 256 256" fill="#e8702a" xmlns="http://www.w3.org/2000/svg">
          <path d="M 256 256 L 128 256 L 0 128 L 128 128 Z M 256 128 L 128 128 L 0 0 L 128 0 Z" />
        </svg>
        <span className="text-white text-2xl font-playfair italic">AIDP</span>
      </Link>

      {/* Center pill — desktop */}
      <div className="hidden md:flex absolute left-1/2 -translate-x-1/2 bg-white/10 backdrop-blur-md border border-white/20 rounded-full px-2 py-2 items-center gap-1">
        {[
          { to: '/dashboard', label: 'Dashboard' },
          { to: '/discover', label: 'Discovery' },
          { to: '/benchmarks', label: 'Benchmarks' },
          { to: '/architecture', label: 'Architecture' },
        ].map((item) => (
          <Link
            key={item.to}
            to={item.to}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${location.pathname === item.to ? 'text-white bg-white/15' : 'text-white/70 hover:bg-white/10 hover:text-white'}`}
          >
            {item.label}
          </Link>
        ))}
      </div>

      {/* Right — desktop */}
      {showAuth && (
        <div className="hidden md:flex items-center gap-3">
          <Link to="/login" className="text-white/70 text-sm font-medium hover:text-white transition-colors px-4 py-2">
            Sign In
          </Link>
          <Link to="/signup" className="bg-[#e8702a] hover:bg-[#d2611f] text-white text-sm font-semibold px-6 py-2.5 rounded-full transition-all hover:scale-[1.03]">
            Get Started
          </Link>
        </div>
      )}

      {/* Mobile hamburger */}
      <button onClick={() => setMobileOpen(!mobileOpen)} className="md:hidden text-white p-2">
        {mobileOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden absolute top-full left-0 right-0 bg-[#0a0a0f]/95 backdrop-blur-xl border-b border-white/10 p-4 space-y-2">
          {[
            { to: '/dashboard', label: 'Dashboard' },
            { to: '/discover', label: 'Discovery' },
            { to: '/benchmarks', label: 'Benchmarks' },
            { to: '/architecture', label: 'Architecture' },
            { to: '/login', label: 'Sign In' },
            { to: '/signup', label: 'Get Started' },
          ].map((item) => (
            <Link
              key={item.to}
              to={item.to}
              onClick={() => setMobileOpen(false)}
              className="block text-white/70 hover:text-white text-sm font-medium py-2 px-3 rounded-xl hover:bg-white/5 transition-colors"
            >
              {item.label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
}
