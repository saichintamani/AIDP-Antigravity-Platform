import React, { useState, useEffect } from 'react';
import Onboarding from './Onboarding';
import ReplayScreen from './ReplayScreen';
import RubricSurvey from './RubricSurvey';
import { supabase } from '../supabaseClient';

const MOCK_CASES = [
  {
    case_id: "CASE_001_PRIONS",
    title: "The Prion Hypothesis",
    year: 1982,
    context: "A novel infectious agent causing scrapie appears to lack nucleic acids. It is highly resistant to UV radiation and nucleases, but sensitive to proteases.",
    candidates: [
      { id: "A", description: "Search for a highly concealed, ultra-small virus using advanced electron microscopy." },
      { id: "B", description: "Purify the infectious protein and sequence it to prove it replicates without DNA/RNA." },
      { id: "C", description: "Isolate the host genome to find a gene that encodes the infectious protein." }
    ]
  },
  {
    case_id: "CASE_002_CRISPR",
    title: "CRISPR Repeats",
    year: 2005,
    context: "Strange clustered repeats are found in bacterial genomes, interspaced with viral DNA sequences. Bacteria with these sequences seem immune to those specific viruses.",
    candidates: [
      { id: "A", description: "Hypothesize this is a structural DNA artifact and ignore it." },
      { id: "B", description: "Perform a gene knockout of the cas genes to see if viral immunity is lost." },
      { id: "C", description: "Attempt to express the repeats in human cells to confer viral immunity." }
    ]
  }
];

export default function TrackEApp() {
  const [evaluatorMeta, setEvaluatorMeta] = useState(null);
  const [cases, setCases] = useState([]);
  const [currentCaseIndex, setCurrentCaseIndex] = useState(0);
  const [currentRankings, setCurrentRankings] = useState(null);
  const [step, setStep] = useState('onboarding');

  useEffect(() => {
    // Attempt to fetch from API, fallback to Mock if offline
    fetch('http://localhost:8000/api/cases')
      .then(res => {
        if (!res.ok) throw new Error("Offline");
        return res.json();
      })
      .then(data => setCases(data.cases))
      .catch(err => {
        console.warn("[TrackE] Backend offline. Using offline dataset.");
        setCases(MOCK_CASES);
      });
  }, []);

  const handleOnboardingComplete = async (meta) => {
    setEvaluatorMeta(meta);
    
    // Verify/Register the user in Supabase
    try {
      const { data, error } = await supabase
        .from('evaluators')
        .upsert([{ 
          evaluator_id: meta.evaluatorId,
          field_of_expertise: meta.fieldOfExpertise,
          years_experience: meta.yearsExperience,
          affiliation: meta.affiliation,
          specialization: meta.specialization
        }]);
      if (error) console.error("Supabase verification error:", error);
      else console.log("Evaluator verified in Supabase!");
    } catch (e) {
      console.warn("Supabase auth bypassed (mock mode).");
    }

    setStep('replay');
  };

  const handleRankingsSubmitted = ({ rankings, confidence, reasoning }) => {
    setCurrentRankings({ rankings, confidence, reasoning });
    setStep('rubric');
  };

  const handleSurveySubmitted = async ({ scores, feedback }) => {
    const currentCase = cases[currentCaseIndex];
    const payload = {
      evaluator_id: evaluatorMeta.evaluatorId,
      case_id: currentCase.case_id,
      ranked_candidates: currentRankings.rankings,
      confidence: currentRankings.confidence,
      reasoning: currentRankings.reasoning,
      rubric_scores: scores,
      feedback: feedback
    };

    try {
      // Secure local storage via FastAPI
      const res = await fetch('http://localhost:8000/api/submit_ranking', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        console.log("Ranking securely saved locally via FastAPI!");
      } else {
        console.error("FastAPI insert error:", await res.text());
      }
    } catch (e) {
      console.error("Failed to submit ranking:", e);
    }

    if (currentCaseIndex < cases.length - 1) {
      setCurrentCaseIndex(prev => prev + 1);
      setStep('replay');
    } else {
      setStep('finished');
    }
  };

  if (step === 'onboarding') return <Onboarding onComplete={handleOnboardingComplete} />;
  
  if (step === 'finished') {
    return (
      <div className="max-w-2xl mx-auto p-6 bg-white shadow rounded-lg mt-10 text-center">
        <h1 className="text-3xl font-bold mb-4 text-green-600">Evaluation Complete</h1>
        <p className="text-gray-700">Thank you for participating in the AIDP independent evaluation. Your rankings have been securely stored.</p>
      </div>
    );
  }

  const currentCase = cases[currentCaseIndex];

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-4xl mx-auto mb-4 px-4 flex justify-between items-center text-gray-500 text-sm">
        <span>Evaluator: {evaluatorMeta?.evaluatorId}</span>
        <span>Case {currentCaseIndex + 1} of {cases.length}</span>
      </div>
      {step === 'replay' && (
        <ReplayScreen 
          caseData={currentCase} 
          onRankingsSubmitted={handleRankingsSubmitted} 
        />
      )}
      {step === 'rubric' && (
        <RubricSurvey 
          onSubmitSurvey={handleSurveySubmitted} 
        />
      )}
    </div>
  );
}
