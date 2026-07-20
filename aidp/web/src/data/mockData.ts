// Mock data derived from actual AIDP project files

export interface BenchmarkCase {
  id: string;
  domain: string;
  status: 'PASS' | 'FAIL' | 'PENDING';
  percentile: number;
  aidpRank: string;
  baselineRank: string;
  outperformsBaseline: boolean;
  historicalWinner: string;
  yearRange: string;
}

export const benchmarkCases: BenchmarkCase[] = [
  { id: 'HRC_CRISPR', domain: 'Molecular Biology', status: 'PASS', percentile: 100, aidpRank: '1 / 4', baselineRank: '3 / 4', outperformsBaseline: true, historicalWinner: 'Challenge a bacterial strain containing a specific phage-matching spacer with that exact phage to observe resistance.', yearRange: '1987–2005' },
  { id: 'HRC_PLATE_TECTONICS', domain: 'Earth Science', status: 'PASS', percentile: 100, aidpRank: '1 / 4', baselineRank: '3 / 4', outperformsBaseline: true, historicalWinner: 'Propose that magnetic stripes record Earth\'s field reversals on newly formed crust moving away from ridge crests.', yearRange: '1950–1963' },
  { id: 'HRC_H_PYLORI', domain: 'Medicine', status: 'PASS', percentile: 100, aidpRank: '1 / 4', baselineRank: '3 / 4', outperformsBaseline: true, historicalWinner: 'Culture spiral bacteria from gastric biopsies and administer targeted antibiotic therapy to ulcer patients.', yearRange: '1970–1982' },
  { id: 'HRC_PRIONS', domain: 'Biology', status: 'PASS', percentile: 100, aidpRank: '1 / 4', baselineRank: '3 / 4', outperformsBaseline: true, historicalWinner: 'Propose that the infectious agent is purely proteinaceous and replicates through conformational templating.', yearRange: '1970–1982' },
  { id: 'HRC_QUASICRYSTALS', domain: 'Materials Science', status: 'PASS', percentile: 100, aidpRank: '1 / 4', baselineRank: '2 / 4', outperformsBaseline: true, historicalWinner: 'Propose a new state of matter—a quasicrystal—with orientational order but no translational periodicity.', yearRange: '1980–1982' },
  { id: 'HRC_HT_SUPERCONDUCTORS', domain: 'Condensed Matter Physics', status: 'PASS', percentile: 100, aidpRank: '1 / 4', baselineRank: '3 / 4', outperformsBaseline: true, historicalWinner: 'Synthesize mixed-valence copper-oxide perovskite ceramics and test for high-Tc superconductivity.', yearRange: '1980–1986' },
  { id: 'HRC_RNAI', domain: 'Molecular Biology', status: 'PASS', percentile: 100, aidpRank: '1 / 4', baselineRank: '3 / 4', outperformsBaseline: true, historicalWinner: 'Test purified dsRNA against ssRNA, hypothesizing dsRNA is the true trigger for gene silencing.', yearRange: '1990–1998' },
  { id: 'HRC_MRNA_LNP', domain: 'Drug Delivery', status: 'PASS', percentile: 100, aidpRank: '1 / 4', baselineRank: '3 / 4', outperformsBaseline: true, historicalWinner: 'Synthesize IVT mRNA with modified nucleosides (pseudouridine) and test immunogenicity in dendritic cells.', yearRange: '1990–2005' },
  { id: 'HRC_HELICASE', domain: 'Biochemistry', status: 'PASS', percentile: 100, aidpRank: '1 / 4', baselineRank: '3 / 4', outperformsBaseline: true, historicalWinner: 'Purify an E. coli protein that requires ATP to catalytically unwind dsDNA into ssDNA in vitro.', yearRange: '1970–1976' },
  { id: 'HRC_GRAVITATIONAL_WAVES', domain: 'Astrophysics', status: 'PASS', percentile: 100, aidpRank: '1 / 4', baselineRank: '3 / 4', outperformsBaseline: true, historicalWinner: 'Upgrade interferometers with active seismic isolation and higher-power lasers to detect binary mergers.', yearRange: '1990–2015' },
];

export const summaryMetrics = {
  populatedCases: '10 / 10',
  passRate: '10 / 10',
  meanPercentile: 100.0,
  medianPercentile: 100.0,
  baselineWinRate: '10 / 10',
  failureCount: 0,
  confidenceLevel: 'Moderate Evidence (N=10)',
};

export interface AgentInfo {
  name: string;
  module: string;
  description: string;
  icon: string; // lucide icon name
  status: 'active' | 'idle' | 'training';
}

export const agents: AgentInfo[] = [
  { name: 'Adversarial Scientist', module: 'reasoning_engine/adversarial_scientist.py', description: 'Challenges hypotheses with counter-evidence and adversarial critiques.', icon: 'Shield', status: 'active' },
  { name: 'Clinical Planner', module: 'discovery/clinical_planning.py', description: 'Designs clinical trial protocols with sample size justification and comparator arms.', icon: 'HeartPulse', status: 'active' },
  { name: 'Debate Orchestrator', module: 'discovery/debate.py', description: 'Multi-agent scientific debate with structured argumentation and consensus building.', icon: 'MessageSquare', status: 'active' },
  { name: 'Hypothesis Generator', module: 'discovery/hypothesis.py', description: 'Formulates mathematically grounded scientific claims from retrieved evidence.', icon: 'Lightbulb', status: 'active' },
  { name: 'Domain Router', module: 'discovery/domain_routing.py', description: 'Routes tasks across WET_LAB, CLINICAL_TRIAL, MATERIALS, COMPUTATIONAL domains.', icon: 'GitBranch', status: 'active' },
  { name: 'Risk Analyst', module: 'reasoning_engine/risk_engine.py', description: 'Evaluates experimental feasibility, ethical risks, and safety constraints.', icon: 'AlertTriangle', status: 'idle' },
  { name: 'Consensus Builder', module: 'discovery/consensus.py', description: 'Synthesizes multi-agent debate outputs into calibrated confidence scores.', icon: 'Users', status: 'active' },
  { name: 'Digital Twin', module: 'reasoning_engine/digital_twin.py', description: 'Simulates experimental outcomes before committing to physical execution.', icon: 'Copy', status: 'idle' },
];

export const pipelineStages = [
  { id: 1, name: 'Knowledge Retrieval', description: 'Searches PubMed, PMC, ArXiv for relevant literature.', icon: 'Search', modules: ['retrieval/', 'knowledge/'] },
  { id: 2, name: 'Protocol Synthesis', description: 'Extracts domain-specific constraints and protocols.', icon: 'FileText', modules: ['planning/', 'config/'] },
  { id: 3, name: 'Hypothesis Generation', description: 'Formulates mathematically sound scientific claims.', icon: 'Lightbulb', modules: ['discovery/hypothesis.py', 'reasoning/'] },
  { id: 4, name: 'Experiment Planning', description: 'Specialized domain agents design methodologies.', icon: 'FlaskConical', modules: ['discovery/clinical_planning.py', 'discovery/scientific_planning.py'] },
  { id: 5, name: 'Formal Verification', description: 'Deterministic validation checks on proposed designs.', icon: 'ShieldCheck', modules: ['verification/', 'validation/'] },
  { id: 6, name: 'Scientific Review', description: 'Multi-agent debate determines consensus and calibrates confidence.', icon: 'Scale', modules: ['discovery/debate.py', 'discovery/consensus.py'] },
  { id: 7, name: 'Execution Compilation', description: 'Translates approved plan into machine-readable protocol.', icon: 'Play', modules: ['discovery/workflow.py'] },
];

export const validationData = {
  humanAgreement: [
    { case: 'Helicase', aiConfidence: 85, humanConsensus: 82 },
    { case: 'RNAi', aiConfidence: 92, humanConsensus: 95 },
    { case: 'Grav Waves', aiConfidence: 78, humanConsensus: 70 },
    { case: 'CRISPR', aiConfidence: 96, humanConsensus: 98 },
    { case: 'String Theory', aiConfidence: 65, humanConsensus: 40 },
    { case: 'Supercond.', aiConfidence: 45, humanConsensus: 35 },
    { case: 'Plate Tect.', aiConfidence: 91, humanConsensus: 88 },
    { case: 'H. Pylori', aiConfidence: 88, humanConsensus: 85 },
    { case: 'Prions', aiConfidence: 94, humanConsensus: 89 },
    { case: 'Quasicrystals', aiConfidence: 81, humanConsensus: 75 },
  ],
  engineEntropy: [
    { epoch: 'T-100', systemEntropy: 8.5, informationGain: 0.2 },
    { epoch: 'T-80', systemEntropy: 7.2, informationGain: 1.5 },
    { epoch: 'T-60', systemEntropy: 5.8, informationGain: 3.2 },
    { epoch: 'T-40', systemEntropy: 4.1, informationGain: 5.1 },
    { epoch: 'T-20', systemEntropy: 2.5, informationGain: 6.8 },
    { epoch: 'T-0', systemEntropy: 1.2, informationGain: 8.4 },
  ]
};

export const milestones = [
  { name: 'Phase R1 — Core Epistemic Engine', status: 'completed' as const, notes: 'EIG formulas, Subjective Logic, and Information Theory engine fully operational.' },
  { name: 'Phase R1.5 — CoT Engine Validation', status: 'completed' as const, notes: 'Chain-of-Thought engine and constraint sensitivity validation successful.' },
  { name: 'Phase R2 — Human Pilot (N=10)', status: 'completed' as const, notes: 'Deploy 10 historical cases to independent scientists for baseline epistemic evaluation.' },
  { name: 'Phase R3 — Scaled Simulation', status: 'completed' as const, notes: 'Engine Characterization bounds formalized (Stability: 0.92, Sensitivity: 0.88).' },
];

export const dashboardStats = [
  { label: 'Benchmark Pass Rate', value: 100, suffix: '%', icon: 'CheckCircle', color: '#22c55e' },
  { label: 'Active Agents', value: 6, suffix: '', icon: 'Bot', color: '#3b82f6' },
  { label: 'Discovery Modules', value: 16, suffix: '', icon: 'Boxes', color: '#e8702a' },
  { label: 'Research Cases', value: 10, suffix: '', icon: 'Microscope', color: '#a855f7' },
];

export const coreModules = [
  { name: 'Discovery Engine', path: 'src/aidp/discovery/', files: 16, description: 'Hypothesis generation, debate, consensus, domain routing, clinical planning' },
  { name: 'Reasoning Engine', path: 'src/aidp/reasoning_engine/', files: 10, description: 'Adversarial scientist, causal sandbox, debate graph, risk engine, simulation' },
  { name: 'Cognitive Core', path: 'src/aidp/cognitive_core/', files: 8, description: 'Tree-of-Thoughts orchestrator, evaluator, traceability logger' },
  { name: 'Knowledge Substrate', path: 'src/aidp/knowledge/', files: 6, description: 'Graph database, vector search, fusion layer' },
  { name: 'Meta-Learning Academy', path: 'src/aidp/meta_learning/', files: 5, description: 'Failure analysis, prompt optimization, reward/penalty system' },
  { name: 'Epistemic Ledger', path: 'src/aidp/platform/', files: 4, description: 'Immutable cryptographic claim tracking and confidence lineage' },
  { name: 'Explainability', path: 'src/aidp/explainability/', files: 4, description: 'Counterfactual engine, reasoning trace visualization' },
  { name: 'Federation', path: 'src/aidp/federation/', files: 6, description: 'WebSocket protocol, distributed agent communication' },
];
