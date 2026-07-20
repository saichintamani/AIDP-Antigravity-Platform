import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import RevealLayer from '../components/RevealLayer';

const BG_IMAGE_1 = 'https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260609_195923_b0ba8ace-1d1d-4f2c-9a28-1ab84b330680.png&w=1280&q=85';
const BG_IMAGE_2 = 'https://images.higgs.ai/?default=1&output=webp&url=https%3A%2F%2Fd8j0ntlcm91z4.cloudfront.net%2Fuser_38xzZboKViGWJOttwIXH07lWA1P%2Fhf_20260609_201152_bba90a12-bf12-459f-91f0-51f237dbaf3b.png&w=1280&q=85';

export default function LandingPage() {
  const mouse = useRef({ x: 0, y: 0 });
  const smooth = useRef({ x: 0, y: 0 });
  const rafRef = useRef<number>(0);
  const [cursorPos, setCursorPos] = useState({ x: -999, y: -999 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      mouse.current = { x: e.clientX, y: e.clientY };
    };
    window.addEventListener('mousemove', handleMouseMove);

    const loop = () => {
      smooth.current.x += (mouse.current.x - smooth.current.x) * 0.1;
      smooth.current.y += (mouse.current.y - smooth.current.y) * 0.1;
      setCursorPos({ x: smooth.current.x, y: smooth.current.y });
      rafRef.current = requestAnimationFrame(loop);
    };
    rafRef.current = requestAnimationFrame(loop);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(rafRef.current);
    };
  }, []);

  return (
    <div className="min-h-screen bg-black tracking-[-0.02em] font-sans">
      <section className="relative w-full overflow-hidden h-screen bg-black" style={{ height: '100dvh' }}>
        {/* Base image */}
        <div 
          className="absolute inset-0 bg-center bg-cover bg-no-repeat z-10 hero-anim hero-zoom" 
          style={{ backgroundImage: `url(${BG_IMAGE_1})` }} 
        />
        
        {/* Reveal layer */}
        <RevealLayer image={BG_IMAGE_2} cursorX={cursorPos.x} cursorY={cursorPos.y} />

        {/* Heading */}
        <div className="absolute top-[25%] left-0 right-0 flex flex-col items-center text-center px-5 pointer-events-none z-50">
          <h1 className="text-white leading-[1.05]">
            <span className="block font-playfair italic font-normal text-5xl sm:text-7xl md:text-8xl hero-anim hero-reveal" style={{ letterSpacing: '-0.02em', animationDelay: '0.25s' }}>
              Discover the
            </span>
            <span className="block font-normal text-5xl sm:text-7xl md:text-8xl mt-2 text-[#e8702a] hero-anim hero-reveal" style={{ letterSpacing: '-0.05em', animationDelay: '0.42s' }}>
              Unknown
            </span>
          </h1>
          <p className="mt-8 text-lg sm:text-xl text-white/70 max-w-2xl mx-auto hero-anim hero-fade" style={{ animationDelay: '0.7s' }}>
            The Artificial Intelligence Discovery Platform integrates multi-agent reasoning, formal verification, and an immutable epistemic ledger to accelerate scientific breakthroughs.
          </p>
          <div className="mt-10 flex gap-4 pointer-events-auto hero-anim hero-fade" style={{ animationDelay: '0.85s' }}>
            <Link to="/discover" className="bg-[#e8702a] hover:bg-[#d2611f] text-white text-base font-semibold px-8 py-4 rounded-full transition-all hover:scale-[1.03] active:scale-95 hover:shadow-lg hover:shadow-[#e8702a]/30">
              Start Discovering
            </Link>
            <Link to="/architecture" className="bg-white/10 hover:bg-white/20 backdrop-blur-md border border-white/20 text-white text-base font-semibold px-8 py-4 rounded-full transition-all hover:scale-[1.03] active:scale-95">
              View Architecture
            </Link>
          </div>
        </div>

        {/* Bottom-left text */}
        <div className="hidden sm:block absolute bottom-14 left-10 md:left-14 max-w-[280px] z-50 hero-anim hero-fade" style={{ animationDelay: '1s' }}>
          <p className="text-sm text-white/60 leading-relaxed font-mono uppercase tracking-wider">
            Platform Status: Flagship Ready
            <br/>N=10 Historical Replay Benchmark
            <br/>Pass Rate: 100%
          </p>
        </div>
      </section>
    </div>
  );
}
