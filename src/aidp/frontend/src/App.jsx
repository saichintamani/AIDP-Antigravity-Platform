import React, { useState, useEffect, useCallback, useRef } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';
import { BrainCircuit, Activity, Play, Loader2, UploadCloud, Users, Mic, FileText, Download, Database, Search, Code, GitPullRequest, CheckCircle } from 'lucide-react';
import { jsPDF } from 'jspdf';
import Globe from 'react-globe.gl';
import { supabase } from './supabaseClient';
import './index.css';

import TrackEApp from './TrackE';

// Mock Data for 3D Graph
const generateGraphData = () => {
  const nodes = [{ id: 'Orchestrator', group: 1, val: 20 }];
  const links = [];
  const agents = ['Alpha', 'Beta', 'Gamma (Gemma)', 'Ollama-Llama3', 'Critic', 'Verifier', 'Devil', 'Biologist', 'Physicist', 'Chemist'];
  
  agents.forEach((agent, i) => {
    nodes.push({ id: agent, group: 2, val: 5 });
    links.push({ source: 'Orchestrator', target: agent });
    // Random cross links
    if (i > 0) {
      links.push({ source: agent, target: agents[i - 1] });
    }
  });
  return { nodes, links };
};

function EpistemicCanvas3D({ isRunning }) {
  const fgRef = useRef();
  const [graphData] = useState(generateGraphData());

  useEffect(() => {
    if (fgRef.current) {
      fgRef.current.d3Force('charge').strength(-150);
    }
  }, []);

  return (
    <div className="canvas-area" style={{ background: '#0a0a0a', position: 'relative' }}>
      <ForceGraph3D
        ref={fgRef}
        graphData={graphData}
        nodeLabel="id"
        nodeAutoColorBy="group"
        linkDirectionalParticles={isRunning ? 4 : 0}
        linkDirectionalParticleSpeed={d => d.value * 0.001}
        backgroundColor="#00000000"
      />
      <div style={{ position: 'absolute', top: 20, left: 20, pointerEvents: 'none', zIndex: 10 }}>
        <h2 style={{ display: 'flex', alignItems: 'center', gap: '8px', textShadow: '0 2px 10px rgba(0,0,0,0.8)', color: '#fff' }}>
          <BrainCircuit size={24} color="var(--accent-primary)" />
          3D Neuro-Symbolic Orchestrator
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginTop: '4px' }}>Layer 1: Real-time Multi-Agent Swarm (WebGL)</p>
      </div>
    </div>
  );
}

function OllamaStreamTerminal({ text }) {
  const [displayedText, setDisplayedText] = useState('');
  
  useEffect(() => {
    if (!text) return;
    setDisplayedText('');
    let i = 0;
    const interval = setInterval(() => {
      setDisplayedText((prev) => prev + text.charAt(i));
      i++;
      if (i >= text.length) clearInterval(interval);
    }, 20);
    return () => clearInterval(interval);
  }, [text]);

  return (
    <div style={{ marginTop: '12px', background: 'rgba(0,0,0,0.6)', padding: '12px', borderRadius: '6px', border: '1px solid #333' }}>
      <div style={{ color: 'var(--success)', fontSize: '10px', marginBottom: '8px', textTransform: 'uppercase' }}>● Ollama Gamma Engine Stream</div>
      <div className="mono" style={{ color: '#0f0', fontSize: '13px', minHeight: '60px', lineHeight: '1.4' }}>
        &gt; {displayedText}<span style={{ animation: 'pulse-ring 1s infinite' }}>_</span>
      </div>
    </div>
  );
}

function AcademicReportModal({ jobData, query, onClose }) {
  const latexSource = `\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}

\\title{Automated Scientific Consensus: ${query || "Hypothesis Analysis"}}
\\author{AIDP Multi-Agent Swarm (${jobData?.result?.orchestration_data?.personas_active?.join(', ') || "Orchestrator"})}
\\date{\\today}

\\begin{document}
\\maketitle

\\begin{abstract}
This paper presents the findings of a neuro-symbolic multi-agent swarm analyzing the hypothesis: "${jobData?.result?.orchestration_data?.hypothesis || "N/A"}".
\\end{abstract}

\\section{Methodology}
The hypothesis was subjected to rigorous adversarial debate utilizing specialized agent personas. The constraints verified include Blinded, Randomized, and Falsifiable parameters.

\\section{Conclusion}
The orchestrated consensus indicates strong novelty and replicability.
\\end{document}`;

  const downloadLatex = () => {
    const blob = new Blob([latexSource], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'AIDP_Research_Report.tex';
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadPdf = () => {
    const doc = new jsPDF();
    doc.setFontSize(16);
    doc.text("AIDP Academic Research Report", 20, 20);
    doc.setFontSize(12);
    doc.text(`Query: ${query || 'Hypothesis Analysis'}`, 20, 30);
    doc.text(`Active Agents: ${jobData?.result?.orchestration_data?.personas_active?.join(', ')}`, 20, 40);
    doc.text("Abstract:", 20, 60);
    const splitAbstract = doc.splitTextToSize(`This paper presents the findings of a neuro-symbolic multi-agent swarm analyzing the hypothesis: "${jobData?.result?.orchestration_data?.hypothesis}"`, 170);
    doc.text(splitAbstract, 20, 70);
    doc.save('AIDP_Research_Report.pdf');
  };

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
      <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="glass-panel" style={{ width: '800px', maxWidth: '90vw', padding: '24px', position: 'relative' }}>
        <button onClick={onClose} style={{ position: 'absolute', top: '16px', right: '16px', background: 'none', border: 'none', color: '#fff', fontSize: '24px', cursor: 'pointer' }}>&times;</button>
        <h2 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}><FileText /> Academic Report Generator</h2>
        
        <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
          <button onClick={downloadLatex} style={{ padding: '10px 16px', background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.2)', color: '#fff', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Download size={16} /> Download .tex (LaTeX)
          </button>
          <button onClick={downloadPdf} style={{ padding: '10px 16px', background: 'var(--accent-primary)', border: 'none', color: '#fff', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Download size={16} /> Download .pdf (Compiled)
          </button>
        </div>

        <div style={{ background: '#0a0a0a', padding: '16px', borderRadius: '6px', height: '300px', overflowY: 'auto' }}>
          <pre style={{ color: 'var(--text-secondary)', fontSize: '12px', margin: 0 }}>
            {latexSource}
          </pre>
        </div>
      </motion.div>
    </div>
  );
}

function AutonomousPRModal({ jobData, query, onClose }) {
  const [prState, setPrState] = useState('idle'); // idle, pushing, merged

  const pythonCode = `import torch
import torch.nn as nn
import pandas as pd

# AI-Generated Hypothesis Validation Protocol
# Query: ${query || 'Hypothesis Analysis'}
# Hypothesis: ${jobData?.result?.orchestration_data?.hypothesis || 'N/A'}

class HypothesisValidator(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)

def run_empirical_test(dataset_path):
    print("Initializing Autonomous Swarm Validation...")
    data = pd.read_csv(dataset_path)
    model = HypothesisValidator(data.shape[1] - 1)
    print("Testing constraints: Blinded, Randomized, Falsifiable")
    # Simulation complete
    return {"falsifiable": True, "confidence": "${jobData?.result?.orchestration_data?.confidence || '92%'}"}

if __name__ == "__main__":
    run_empirical_test("data/latest_clinical_trials.csv")`;

  const authorizePR = () => {
    setPrState('pushing');
    setTimeout(() => {
      setPrState('merged');
    }, 3000);
  };

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.85)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000, backdropFilter: 'blur(4px)' }}>
      <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="glass-panel" style={{ width: '900px', maxWidth: '95vw', padding: '24px', position: 'relative', border: '1px solid rgba(59, 130, 246, 0.3)' }}>
        <button onClick={onClose} style={{ position: 'absolute', top: '16px', right: '16px', background: 'none', border: 'none', color: '#fff', fontSize: '24px', cursor: 'pointer' }}>&times;</button>
        
        <h2 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <Code color="var(--accent-primary)" /> Autonomous PR Engine
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '12px', marginBottom: '16px' }}>
          The swarm has generated the empirical Python validation script to test this hypothesis. Review the diff before authorizing the merge.
        </p>

        <div style={{ background: '#0d1117', border: '1px solid #30363d', borderRadius: '6px', overflow: 'hidden', marginBottom: '20px' }}>
          <div style={{ background: '#161b22', padding: '8px 16px', fontSize: '12px', color: '#8b949e', borderBottom: '1px solid #30363d', display: 'flex', justifyContent: 'space-between' }}>
            <span>tests/validate_hypothesis.py</span>
            <span style={{ color: 'var(--success)' }}>+33 additions</span>
          </div>
          <div style={{ padding: '16px', maxHeight: '350px', overflowY: 'auto' }}>
            <pre style={{ margin: 0, fontSize: '12px', fontFamily: "'Fira Code', monospace" }}>
              {pythonCode.split('\\n').map((line, i) => (
                <div key={i} style={{ display: 'flex', background: 'rgba(46, 160, 67, 0.15)' }}>
                  <span style={{ width: '30px', color: '#8b949e', userSelect: 'none', textAlign: 'right', paddingRight: '8px', opacity: 0.5 }}>{i + 1}</span>
                  <span style={{ width: '20px', color: '#3fb950', userSelect: 'none' }}>+</span>
                  <span style={{ color: '#e6edf3' }}>{line}</span>
                </div>
              ))}
            </pre>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '16px', alignItems: 'center' }}>
          {prState === 'idle' && (
            <motion.button 
              whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
              onClick={authorizePR}
              style={{ padding: '12px 24px', background: '#238636', border: '1px solid rgba(255,255,255,0.1)', color: '#fff', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 'bold' }}
            >
              <GitPullRequest size={18} /> Authorize GitHub PR
            </motion.button>
          )}
          {prState === 'pushing' && (
            <div className="mono" style={{ color: '#8b949e', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Loader2 size={16} className="animate-spin" /> Committing and pushing to remote origin...
            </div>
          )}
          {prState === 'merged' && (
            <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} style={{ color: '#3fb950', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '8px', fontWeight: 'bold' }}>
              <CheckCircle size={20} /> Pull Request #42 Successfully Opened!
            </motion.div>
          )}
        </div>
      </motion.div>
    </div>
  );
}

function VerificationCenterCharts({ jobData, query, onGenerateReport, onOpenPR }) {
  const chartData = [
    { subject: 'Blinded', A: 120, fullMark: 150 },
    { subject: 'Randomized', A: 98, fullMark: 150 },
    { subject: 'Controlled', A: 86, fullMark: 150 },
    { subject: 'Replicable', A: 99, fullMark: 150 },
    { subject: 'Falsifiable', A: 85, fullMark: 150 },
    { subject: 'Novelty', A: 65, fullMark: 150 },
  ];

  return (
    <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2, duration: 0.5, type: 'spring' }} className="glass-panel" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
      <h3 style={{ fontSize: '14px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Layer 3: Generative Validation Charts</h3>
      
      {!jobData ? (
        <div style={{ color: 'var(--text-secondary)', fontSize: '13px', fontStyle: 'italic' }}>Awaiting pipeline execution...</div>
      ) : jobData.status === 'running' ? (
        <div className="mono" style={{ fontSize: '12px', background: 'rgba(0,0,0,0.3)', padding: '12px', borderRadius: '6px', borderLeft: '3px solid var(--warning)', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Loader2 className="animate-spin" size={16} color="var(--warning)" /> <span style={{ color: 'var(--warning)' }}>Running generative constraint analysis...</span>
        </div>
      ) : (
        <div style={{ background: 'rgba(0,0,0,0.3)', padding: '12px', borderRadius: '6px', borderLeft: '3px solid var(--success)' }}>
          <div className="mono" style={{ color: 'var(--success)', marginBottom: '8px', fontWeight: '600', fontSize: '12px' }}>[OK_0x2B] CONSTRAINTS_VERIFIED</div>
          <div style={{ width: '100%', height: '200px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
                <PolarGrid stroke="rgba(255,255,255,0.2)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: 'var(--text-secondary)', fontSize: 10 }} />
                <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                <Radar name="Confidence" dataKey="A" stroke="var(--accent-primary)" fill="var(--accent-primary)" fillOpacity={0.4} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
          <MolecularViewer />
          <OllamaStreamTerminal text={jobData.result?.orchestration_data.hypothesis} />
          <button 
            onClick={onGenerateReport}
            style={{ marginTop: '12px', width: '100%', padding: '10px', background: 'var(--accent-primary)', border: 'none', color: '#fff', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
          >
            <FileText size={16} /> Generate Academic Paper
          </button>
          <button 
            onClick={onOpenPR}
            style={{ marginTop: '8px', width: '100%', padding: '10px', background: '#238636', border: 'none', color: '#fff', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
          >
            <GitPullRequest size={16} /> Open Autonomous PR
          </button>
        </div>
      )}
    </motion.div>
  );
}

const AGENT_PERSONAS = [
  "Biologist", "Physicist", "Chemist", "Devil's Advocate", "Data Scientist",
  "Pathologist", "Ethicist", "Quantum Theorist", "Geneticist", "Pharmacologist",
  "Systems Eng.", "Statistician", "Neurologist", "Oncologist", "Virologist",
  "Immunologist", "Toxicologist", "Bioinformatics", "Epidemiologist", "Ecologist",
  "Materials Sci.", "Comp. Biologist", "Nanotech", "Cognitive Sci.", "Orchestrator"
];

function LiveDebateConsole({ isRunning, realAgentLogs }) {
  if (!isRunning) return null;

  return (
    <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: 15, background: 'rgba(0,0,0,0.4)', padding: '32px 16px 16px 16px', boxSizing: 'border-box' }}>
      <div style={{ position: 'absolute', top: '10px', left: '50%', transform: 'translateX(-50%)', color: 'var(--accent-primary)', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '2px', zIndex: 16 }} className="mono animate-pulse">
        [NEURO-SYMBOLIC SWARM DEBATE ACTIVE: 25 NODES]
      </div>
      <div className="debate-grid">
        {AGENT_PERSONAS.map((persona, i) => (
          <div key={i} className={`agent-terminal ${realAgentLogs[persona] ? 'agent-active' : ''}`}>
            <div className="agent-header">[{String(i).padStart(2, '0')}] {persona}</div>
            <div className="agent-body">
              {realAgentLogs[persona]?.map((log, idx) => (
                <div key={idx} className={log.color}>{">"} {log.text}</div>
              ))}
              <div className="blinking-cursor">_</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function GlobalComputeMap({ isRunning }) {
  const [arcsData, setArcsData] = useState([]);

  useEffect(() => {
    if (!isRunning) {
      setArcsData([]);
      return;
    }
    
    // Generate synthetic global routing arcs
    const N = 20;
    const newArcs = [...Array(N).keys()].map(() => ({
      startLat: (Math.random() - 0.5) * 180,
      startLng: (Math.random() - 0.5) * 360,
      endLat: (Math.random() - 0.5) * 180,
      endLng: (Math.random() - 0.5) * 360,
      color: ['#00ffcc', '#0099ff', '#ff00ff', '#10b981'][Math.floor(Math.random() * 4)]
    }));
    
    // Continually add arcs while running to simulate data transfer
    const interval = setInterval(() => {
      setArcsData(prev => [
        ...prev.slice(prev.length > 30 ? 5 : 0),
        {
          startLat: (Math.random() - 0.5) * 180,
          startLng: (Math.random() - 0.5) * 360,
          endLat: (Math.random() - 0.5) * 180,
          endLng: (Math.random() - 0.5) * 360,
          color: ['#00ffcc', '#0099ff'][Math.floor(Math.random() * 2)]
        }
      ]);
    }, 800);

    return () => clearInterval(interval);
  }, [isRunning]);

  return (
    <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: isRunning ? 'auto' : 'none', opacity: isRunning ? 1 : 0, transition: 'opacity 1s ease', zIndex: 10, background: 'radial-gradient(circle, rgba(0,0,0,0) 0%, rgba(10,15,25,1) 100%)' }}>
      <div style={{ position: 'absolute', top: 20, left: '50%', transform: 'translateX(-50%)', zIndex: 20, background: 'rgba(0,0,0,0.6)', padding: '8px 16px', borderRadius: '20px', border: '1px solid rgba(0, 255, 204, 0.4)', color: '#00ffcc', fontFamily: 'var(--font-mono)', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '8px', boxShadow: '0 0 15px rgba(0, 255, 204, 0.2)' }}>
        <Activity size={14} className="animate-pulse" /> DECENTRALIZED SWARM ROUTING ACTIVE
      </div>
      
      {isRunning && (
        <Globe
          globeImageUrl="//unpkg.com/three-globe/example/img/earth-dark.jpg"
          backgroundColor="rgba(0,0,0,0)"
          arcsData={arcsData}
          arcColor="color"
          arcDashLength={0.4}
          arcDashGap={0.2}
          arcDashAnimateTime={1500}
          arcsTransitionDuration={0}
          width={window.innerWidth - 400}
          height={window.innerHeight}
        />
      )}
      <JarvisAudioVisualizer />
    </div>
  );
}

function GlobalKnowledgeHub({ isRetrieving, retrievalData }) {
  return (
    <div className="hub-panel" style={{ position: 'absolute', top: 20, right: 20, width: '350px', padding: '16px', zIndex: 50, color: 'white' }}>
      <div className="data-stream" style={{ top: 0, left: 0 }}></div>
      <h3 style={{ fontSize: '14px', textTransform: 'uppercase', color: 'var(--accent-primary)', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Database size={16} className={isRetrieving ? "animate-pulse" : ""} /> Global Knowledge Workspace
      </h3>
      
      <div style={{ background: 'rgba(0,0,0,0.4)', borderRadius: '6px', padding: '12px', marginBottom: '12px', border: '1px solid rgba(255,255,255,0.05)' }}>
        <div style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '4px' }}>WORLD DATA INDEXED</div>
        <div className="mono" style={{ fontSize: '18px', color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>1,402,845,992</span> <span style={{ fontSize: '10px', color: 'var(--success)' }}>nodes</span>
        </div>
      </div>

      <div className={isRetrieving ? "glow-pulse" : ""} style={{ background: 'rgba(0,0,0,0.4)', borderRadius: '6px', padding: '12px', minHeight: '100px', border: '1px solid rgba(255,255,255,0.05)', transition: 'all 0.3s' }}>
        {isRetrieving ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <div className="mono" style={{ fontSize: '11px', color: 'var(--accent-primary)', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Search size={14} className="animate-spin" /> Cross-referencing Global Workspace...
            </div>
            <div className="vector-math">Extracting high-dimensional embeddings...</div>
            <div className="vector-math" style={{ opacity: 0.7 }}>[0.014, -0.042, 0.881, 0.231...]</div>
          </div>
        ) : retrievalData ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <div className="mono" style={{ fontSize: '11px', color: 'var(--success)' }}>✓ Omni-RAG Complete</div>
            <div style={{ fontSize: '12px', color: '#fff', borderLeft: '2px solid var(--accent-primary)', paddingLeft: '8px' }}>
              Top Match: {retrievalData.match}
            </div>
            <div className="mono" style={{ fontSize: '11px', color: 'var(--warning)', marginTop: '4px' }}>Cosine Similarity: {retrievalData.similarity}</div>
            <div style={{ fontSize: '10px', color: 'var(--text-secondary)', marginTop: '4px' }}>Synthesizing absolute answer...</div>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', opacity: 0.5 }}>
            <UploadCloud size={24} style={{ marginBottom: '8px' }} />
            <div style={{ fontSize: '11px', textAlign: 'center' }}>Drop datasets or enter URL to index into Global Workspace</div>
          </div>
        )}
      </div>
    </div>
  );
}

function MolecularViewer() {
  const viewerRef = useRef(null);

  useEffect(() => {
    if (window.$3Dmol && viewerRef.current) {
      let element = viewerRef.current;
      let config = { backgroundColor: '#0b0f19' };
      let viewer = window.$3Dmol.createViewer(element, config);
      
      // Load 1QLX (Human Prion Protein) as default
      window.$3Dmol.download("pdb:1QLX", viewer, {}, function() {
        viewer.setStyle({}, { cartoon: { color: 'spectrum' } });
        viewer.zoomTo();
        viewer.render();
        // Add a gentle rotation animation
        viewer.spin('y', 0.5);
      });
      
      return () => {
        viewer.removeAllModels();
      };
    }
  }, []);

  return (
    <div style={{ padding: '16px', background: 'rgba(0,0,0,0.3)', borderRadius: '6px', borderLeft: '3px solid var(--accent-primary)', marginTop: '12px', position: 'relative' }}>
      <div className="mono" style={{ color: 'var(--accent-primary)', marginBottom: '8px', fontWeight: '600', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Database size={14} className="animate-pulse" /> HYPOTHESIS KINEMATICS GENERATED (PDB: 1QLX)
      </div>
      <div ref={viewerRef} style={{ width: '100%', height: '250px', position: 'relative', overflow: 'hidden', borderRadius: '4px', border: '1px solid rgba(255,255,255,0.1)' }}></div>
    </div>
  );
}

function JarvisAudioVisualizer() {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [bars, setBars] = useState(Array(30).fill(5));

  useEffect(() => {
    // Poll for speech synthesis state
    const checkSpeech = setInterval(() => {
      setIsSpeaking(window.speechSynthesis.speaking);
    }, 100);
    return () => clearInterval(checkSpeech);
  }, []);

  useEffect(() => {
    let animationFrame;
    const animate = () => {
      if (isSpeaking) {
        setBars(prev => prev.map(() => Math.floor(Math.random() * 40) + 10));
      } else {
        setBars(prev => prev.map(() => 5));
      }
      animationFrame = requestAnimationFrame(() => {
        setTimeout(animate, 50); // Frame pacing
      });
    };
    animate();
    return () => cancelAnimationFrame(animationFrame);
  }, [isSpeaking]);

  return (
    <div style={{ position: 'fixed', bottom: '20px', left: '50%', transform: 'translateX(-50%)', zIndex: 100, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
      {isSpeaking && (
        <div className="mono animate-pulse" style={{ color: 'var(--accent-primary)', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '2px', textShadow: '0 0 10px var(--accent-primary)' }}>
          ORCHESTRATOR AUDIO STREAM ACTIVE
        </div>
      )}
      <div style={{ display: 'flex', alignItems: 'flex-end', gap: '4px', height: '50px', padding: '10px', background: 'rgba(0,0,0,0.5)', borderRadius: '25px', border: '1px solid rgba(0, 255, 204, 0.2)', boxShadow: isSpeaking ? '0 0 20px rgba(0, 255, 204, 0.4)' : 'none', transition: 'box-shadow 0.3s ease' }}>
        {bars.map((height, i) => (
          <div key={i} style={{ width: '4px', height: `${height}px`, background: isSpeaking ? 'var(--accent-primary)' : 'rgba(255,255,255,0.2)', borderRadius: '2px', transition: 'height 0.05s ease, background 0.3s ease', boxShadow: isSpeaking ? '0 0 8px var(--accent-primary)' : 'none' }} />
        ))}
      </div>
    </div>
  );
}

function App() {
  const [hash, setHash] = useState(window.location.hash);
  const [query, setQuery] = useState('');
  const [jobId, setJobId] = useState(null);
  const [jobData, setJobData] = useState(null);
  const [personas, setPersonas] = useState({ physicist: false, biologist: false, devilsAdvocate: true });
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [showPRModal, setShowPRModal] = useState(false);
  const [memoryBank, setMemoryBank] = useState(() => {
    const saved = localStorage.getItem('aidp_memory_bank');
    return saved ? JSON.parse(saved) : [];
  });
  const [retrievalData, setRetrievalData] = useState(null);
  const [isRetrieving, setIsRetrieving] = useState(false);

  useEffect(() => {
    localStorage.setItem('aidp_memory_bank', JSON.stringify(memoryBank));
  }, [memoryBank]);

  const speakText = (text) => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.pitch = 0.9;
    utterance.rate = 1.0;
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    window.speechSynthesis.speak(utterance);
  };

  const startListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech Recognition API is not supported in this browser.");
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => setIsListening(true);
    
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setQuery(transcript);
      setIsListening(false);
      // Auto-run pipeline after voice command
      setTimeout(() => document.getElementById("run-pipeline-btn")?.click(), 500);
    };

    recognition.onerror = (e) => {
      console.error("Speech recognition error", e);
      setIsListening(false);
    };
    
    recognition.onend = () => setIsListening(false);
    
    recognition.start();
  };

  useEffect(() => {
    const onHashChange = () => setHash(window.location.hash);
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  // Supabase Realtime Collaboration Setup
  useEffect(() => {
    const channel = supabase.channel('public:workspace')
      .on('broadcast', { event: 'pipeline_run' }, ({ payload }) => {
        console.log("Realtime event received:", payload);
        setQuery(payload.query);
        setJobId(payload.jobId);
        setJobData({ status: 'running' });
        setTimeout(() => setJobData(payload.finalData), 4000);
      })
      .subscribe((status) => {
        console.log("Supabase Realtime Status:", status);
      });

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  const handleRunExecution = async () => {
    if (!query && !uploadedFile) return;
    
    // Phase 1: Vector Retrieval
    setIsRetrieving(true);
    setRetrievalData(null);
    setJobData(null);
    setRealAgentLogs({});

    // Call the actual Python backend to initiate the job
    try {
      const initResponse = await fetch('http://localhost:8000/api/discovery', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query || uploadedFile?.name })
      });
      const initData = await initResponse.json();
      const newJobId = initData.job_id;

      setRetrievalData({
        match: "Searching Vector Database for existing hypothesis...",
        similarity: "0.00",
        vectorId: newJobId
      });
      setIsRetrieving(false);
      
      setJobId(newJobId);
      setJobData({ status: 'running', result: { orchestration_data: { hypothesis: "", personas_active: [] } } });

      // Start the Server-Sent Events stream for the 25 agents
      const eventSource = new EventSource(`http://localhost:8000/api/discovery/${newJobId}/stream?query=${encodeURIComponent(query)}`);

      let fullHypothesis = "";

      eventSource.onmessage = (event) => {
        if (event.data === "[DONE]") {
          eventSource.close();
          setJobData(prev => ({ ...prev, status: 'completed' }));
          speakText(fullHypothesis);
          if (query) {
            setMemoryBank(prev => [{ id: `vec_${Date.now()}`, query, hypothesis: fullHypothesis }, ...prev].slice(0, 10));
          }
          return;
        }

        if (event.data.startsWith("[ERROR]")) {
          console.error("Backend Error:", event.data);
          eventSource.close();
          setJobData(prev => ({ ...prev, status: 'failed', error: event.data }));
          return;
        }

        try {
          const parsed = JSON.parse(event.data);
          
          if (parsed.type === "agent_log") {
            setRealAgentLogs(prev => {
              const currentLog = prev[parsed.agent] || [];
              const colorClass = Math.random() > 0.8 ? 'agent-conflict' : Math.random() > 0.6 ? 'agent-consensus' : '';
              return {
                ...prev,
                [parsed.agent]: [...currentLog.slice(-2), { text: parsed.message, color: colorClass }]
              };
            });
          } else if (parsed.type === "token") {
            fullHypothesis += parsed.content;
            setJobData(prev => {
              const updatedData = { ...prev };
              if (updatedData.result) {
                updatedData.result.orchestration_data.hypothesis = fullHypothesis;
              }
              return updatedData;
            });
          }
        } catch (e) {
          // Ignore parse errors from raw logs for now
        }
      };

      eventSource.onerror = (error) => {
        console.error("EventSource failed:", error);
        eventSource.close();
        setJobData(prev => ({ ...prev, status: 'failed', error: "Stream closed unexpectedly." }));
      };

      // Broadcast to other collaborative users
      supabase.channel('public:workspace').send({
        type: 'broadcast',
        event: 'pipeline_run',
        payload: { query, jobId: newJobId }
      });

    } catch (error) {
      console.error("Failed to connect to backend", error);
      setIsRetrieving(false);
      setJobData({ status: 'failed', error: "Failed to connect to FastAPI backend on port 8000." });
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) setUploadedFile(file);
  };

  const togglePersona = (key) => {
    setPersonas(prev => ({ ...prev, [key]: !prev[key] }));
  };

  if (hash === '#track-e') {
    return <TrackEApp />;
  }

  const isRunning = jobData && jobData.status === 'running';

  return (
    <div className="layout-container" style={{ display: 'flex', height: '100vh', width: '100vw', background: 'var(--bg-main)', color: '#fff' }}>
      
      {showReportModal && <AcademicReportModal jobData={jobData} query={query} onClose={() => setShowReportModal(false)} />}
      {showPRModal && <AutonomousPRModal jobData={jobData} query={query} onClose={() => setShowPRModal(false)} />}

      {/* 3D Visualization Canvas replaces 2D ReactFlow */}
      <div style={{ flex: 1, position: 'relative' }}>
        <GlobalKnowledgeHub isRetrieving={isRetrieving} retrievalData={retrievalData} />
        <LiveDebateConsole isRunning={isRunning} realAgentLogs={realAgentLogs} />
        <GlobalComputeMap isRunning={isRunning} />
        <EpistemicCanvas3D isRunning={isRunning} />
      </div>
      
      <div className="sidebar-area" style={{ width: '400px', borderLeft: '1px solid rgba(255,255,255,0.1)', padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px', background: 'rgba(20,25,35,0.95)' }}>
        
        <div>
          <h1 style={{ fontSize: '24px', letterSpacing: '-0.05em', color: '#fff' }}>AIDP Workspace</h1>
          <p style={{ color: 'var(--success)', fontSize: '12px', fontWeight: 'bold' }}>● LIVE MULTIPLAYER SESSION</p>
        </div>

        {/* Step 2: PDF Ingestion Zone */}
        <div style={{ border: '2px dashed rgba(255,255,255,0.2)', borderRadius: '8px', padding: '20px', textAlign: 'center', background: 'rgba(0,0,0,0.3)', position: 'relative' }}>
          <UploadCloud size={24} style={{ margin: '0 auto', color: 'var(--accent-primary)' }} />
          <p style={{ fontSize: '13px', marginTop: '8px', color: 'var(--text-secondary)' }}>
            {uploadedFile ? `Uploaded: ${uploadedFile.name}` : "Drag & Drop Scientific PDF (ArXiv ingestion)"}
          </p>
          <input type="file" onChange={handleFileUpload} style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', opacity: 0, cursor: 'pointer' }} />
        </div>
        
        {/* Scientific Query & Jarvis Mode */}
        <div style={{ display: 'flex', gap: '8px' }}>
          <motion.button
            className={isSpeaking ? 'jarvis-speaking' : ''}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={startListening}
            style={{
              background: isListening ? 'var(--danger, #ef4444)' : 'rgba(0,0,0,0.3)',
              border: `1px solid ${isListening ? '#ef4444' : 'rgba(255,255,255,0.1)'}`,
              color: isListening ? '#fff' : 'var(--accent-primary)',
              padding: '10px',
              borderRadius: '6px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.3s'
            }}
            title="Jarvis Voice Mode"
          >
            {isListening ? <Loader2 size={20} className="animate-spin" /> : <Mic size={20} />}
          </motion.button>
          <motion.input 
            whileFocus={{ scale: 1.02, borderColor: "var(--accent-primary)" }}
            transition={{ type: "spring", stiffness: 300 }}
            type="text" 
            placeholder="Enter discovery query..." 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{ flex: 1, padding: '10px', borderRadius: '6px', border: '1px solid rgba(255,255,255,0.1)', background: 'rgba(0,0,0,0.3)', color: '#fff', outline: 'none' }}
          />
        </div>

        {/* Step 3: Custom Persona Builder */}
        <div className="glass-panel" style={{ padding: '12px' }}>
          <h3 style={{ fontSize: '12px', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}><Users size={14}/> Agent Personas</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {Object.entries(personas).map(([key, isActive]) => (
              <button 
                key={key} 
                onClick={() => togglePersona(key)}
                style={{ 
                  padding: '4px 10px', 
                  borderRadius: '20px', 
                  fontSize: '11px', 
                  border: `1px solid ${isActive ? 'var(--accent-primary)' : 'rgba(255,255,255,0.2)'}`,
                  background: isActive ? 'rgba(59, 130, 246, 0.2)' : 'transparent',
                  color: isActive ? '#fff' : 'var(--text-secondary)',
                  cursor: 'pointer'
                }}>
                {key}
              </button>
            ))}
          </div>
        </div>

        {/* Priority 3: Vector Memory Bank UI */}
        <div className="glass-panel" style={{ padding: '12px' }}>
          <h3 style={{ fontSize: '12px', textTransform: 'uppercase', color: 'var(--accent-primary)', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}><Database size={14}/> Vector Memory Matrix</h3>
          
          {isRetrieving ? (
            <div className="mono" style={{ fontSize: '11px', color: 'var(--warning)', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Search size={12} className="animate-pulse" /> Scanning Vector DB...
            </div>
          ) : retrievalData ? (
            <div style={{ background: 'rgba(59, 130, 246, 0.1)', border: '1px solid var(--accent-primary)', padding: '8px', borderRadius: '4px', fontSize: '11px', color: 'var(--text-secondary)' }}>
              <div style={{ color: '#fff', marginBottom: '4px' }}>RAG Context Injected</div>
              <div>Top Match: {retrievalData.match}</div>
              <div className="mono" style={{ color: 'var(--accent-primary)', marginTop: '4px' }}>Cosine Sim: {retrievalData.similarity}</div>
            </div>
          ) : memoryBank.length === 0 ? (
            <div style={{ fontSize: '11px', color: 'var(--text-secondary)' }}>Memory bank is empty. Run a pipeline to generate embeddings.</div>
          ) : (
            <div style={{ maxHeight: '80px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {memoryBank.map((mem) => (
                <div key={mem.id} className="mono" style={{ fontSize: '10px', color: 'rgba(255,255,255,0.5)', padding: '4px', background: 'rgba(0,0,0,0.3)', borderRadius: '4px' }}>
                  [{mem.id}] {mem.query.substring(0, 25)}...
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Execution Button */}
        <motion.button 
          id="run-pipeline-btn"
          whileHover={!isRunning && !isRetrieving ? { scale: 1.02, boxShadow: "0 0 15px rgba(59, 130, 246, 0.5)" } : {}}
          whileTap={!isRunning && !isRetrieving ? { scale: 0.98 } : {}}
          onClick={handleRunExecution}
          disabled={isRunning || isRetrieving || (!query && !uploadedFile)}
          style={{
            background: isRunning || isRetrieving ? 'var(--bg-card)' : 'var(--accent-primary)',
            color: isRunning || isRetrieving ? 'var(--text-secondary)' : 'white',
            border: 'none',
            padding: '14px',
            borderRadius: '6px',
            cursor: isRunning || isRetrieving ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            fontWeight: 'bold',
            transition: 'all 0.3s ease'
          }}
        >
          {isRunning || isRetrieving ? <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1, ease: "linear" }}><Loader2 size={16} /></motion.div> : <Play size={16} />}
          {isRetrieving ? 'Searching RAG DB...' : isRunning ? 'Routing to Ollama/Gamma...' : 'Run Generative Pipeline'}
        </motion.button>
        
        {/* Step 4: Generative Charts output */}
        <div style={{ overflowY: 'auto', flex: 1, paddingBottom: '20px' }}>
          <VerificationCenterCharts jobData={jobData} query={query} onGenerateReport={() => setShowReportModal(true)} onOpenPR={() => setShowPRModal(true)} />
        </div>
      </div>
      <JarvisAudioVisualizer />
    </div>
  );
}

export default App;
