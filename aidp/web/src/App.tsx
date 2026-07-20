import { useState } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import DashboardPage from './pages/DashboardPage';
import DiscoveryPage from './pages/DiscoveryPage';
import BenchmarkPage from './pages/BenchmarkPage';
import ArchitecturePage from './pages/ArchitecturePage';
import ValidationPage from './pages/ValidationPage';
import AlignEvalPage from './pages/AlignEvalPage';

export default function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const location = useLocation();

  // Pages that don't have the sidebar layout
  const isAuthOrLanding = ['/', '/login', '/signup'].includes(location.pathname);

  return (
    <div className="min-h-screen bg-[#050508] text-white selection:bg-[#e8702a]/30">
      <div className="bg-noise" />
      {isAuthOrLanding ? (
        <>
          <Navbar showAuth={true} />
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignUpPage />} />
          </Routes>
        </>
      ) : (
        <div className="flex h-screen overflow-hidden">
          <Sidebar collapsed={sidebarCollapsed} onToggle={() => setSidebarCollapsed(!sidebarCollapsed)} />
          <div className={`flex-1 flex flex-col transition-all duration-300 ${sidebarCollapsed ? 'ml-[72px]' : 'ml-[240px]'}`}>
            <Navbar showAuth={false} />
            <main className="flex-1 overflow-y-auto mt-[72px] pb-12">
              <Routes>
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/discover" element={<DiscoveryPage />} />
                <Route path="/benchmarks" element={<BenchmarkPage />} />
                <Route path="/architecture" element={<ArchitecturePage />} />
                <Route path="/validation" element={<ValidationPage />} />
                <Route path="/align-eval" element={<AlignEvalPage />} />
              </Routes>
            </main>
          </div>
        </div>
      )}
    </div>
  );
}
