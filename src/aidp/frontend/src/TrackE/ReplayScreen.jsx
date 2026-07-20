import React, { useState, useEffect } from 'react';

export default function ReplayScreen({ caseData, onRankingsSubmitted }) {
  const [candidates, setCandidates] = useState([]);
  const [confidence, setConfidence] = useState(3);
  const [reasoning, setReasoning] = useState('');

  useEffect(() => {
    if (caseData && caseData.candidates) {
      setCandidates([...caseData.candidates]);
      setConfidence(3);
      setReasoning('');
    }
  }, [caseData]);

  const moveUp = (index) => {
    if (index === 0) return;
    const newCands = [...candidates];
    const temp = newCands[index - 1];
    newCands[index - 1] = newCands[index];
    newCands[index] = temp;
    setCandidates(newCands);
  };

  const moveDown = (index) => {
    if (index === candidates.length - 1) return;
    const newCands = [...candidates];
    const temp = newCands[index + 1];
    newCands[index + 1] = newCands[index];
    newCands[index] = temp;
    setCandidates(newCands);
  };

  const handleSubmit = () => {
    if (!reasoning.trim()) {
      alert("Please provide reasoning for your top choice.");
      return;
    }
    onRankingsSubmitted({ rankings: candidates, confidence, reasoning });
  };

  if (!caseData) return <div>Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto p-4 flex flex-col gap-6">
      <div className="bg-white p-6 rounded shadow">
        <h2 className="text-2xl font-bold mb-2">Historical Replay: {caseData.domain} ({caseData.time_window})</h2>
        <p className="text-gray-600 italic">Review the following historical state of knowledge.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded shadow">
          <h3 className="text-xl font-bold mb-4 text-blue-800">Historical Evidence</h3>
          <ul className="list-disc pl-5 space-y-2">
            {caseData.evidence.map((ev, i) => (
              <li key={i} className="text-gray-700">{ev}</li>
            ))}
          </ul>
        </div>

        <div className="bg-white p-6 rounded shadow">
          <h3 className="text-xl font-bold mb-4 text-red-800">Physical Constraints</h3>
          {caseData.constraints.length > 0 ? (
            <ul className="list-disc pl-5 space-y-2">
              {caseData.constraints.map((c, i) => (
                <li key={i} className="text-gray-700">{c}</li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500 italic">No explicit constraints highlighted for this era.</p>
          )}
        </div>
      </div>

      <div className="bg-white p-6 rounded shadow">
        <h3 className="text-xl font-bold mb-4">Rank Candidate Experiments</h3>
        <p className="mb-4 text-sm text-gray-500">Order from 1 (Most informative / Best next step) to 4 (Least informative).</p>
        
        <div className="space-y-3 mb-8">
          {candidates.map((c, idx) => (
            <div key={idx} className="flex items-center gap-4 p-4 border rounded bg-gray-50">
              <div className="flex flex-col gap-1">
                <button 
                  onClick={() => moveUp(idx)} 
                  disabled={idx === 0}
                  className={`p-1 rounded ${idx === 0 ? 'text-gray-300' : 'text-blue-600 hover:bg-blue-100'}`}
                >
                  ▲
                </button>
                <span className="text-center font-bold">{idx + 1}</span>
                <button 
                  onClick={() => moveDown(idx)} 
                  disabled={idx === candidates.length - 1}
                  className={`p-1 rounded ${idx === candidates.length - 1 ? 'text-gray-300' : 'text-blue-600 hover:bg-blue-100'}`}
                >
                  ▼
                </button>
              </div>
              <div className="flex-1 text-gray-800">{c}</div>
            </div>
          ))}
        </div>

        <div className="border-t pt-6 space-y-6">
          <div>
            <label className="block font-bold text-gray-800 mb-2">Confidence Level</label>
            <p className="text-sm text-gray-500 mb-3">How confident are you in this ranking?</p>
            <div className="flex gap-4">
              {[1, 2, 3, 4, 5].map(val => (
                <label key={val} className="flex flex-col items-center gap-1 cursor-pointer">
                  <input 
                    type="radio" 
                    name="confidence" 
                    value={val} 
                    checked={confidence === val}
                    onChange={() => setConfidence(val)}
                    className="w-4 h-4 text-blue-600"
                  />
                  <span className="text-sm">{val}</span>
                </label>
              ))}
            </div>
          </div>

          <div>
            <label className="block font-bold text-gray-800 mb-2">Reasoning</label>
            <p className="text-sm text-gray-500 mb-2">Why did you rank your top experiment first?</p>
            <textarea 
              value={reasoning}
              onChange={e => setReasoning(e.target.value)}
              className="w-full border rounded p-2 text-gray-700 h-24"
              placeholder="Briefly explain your rationale..."
              required
            ></textarea>
          </div>

          <div className="mt-6">
            <button onClick={handleSubmit} className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700">
              Submit Rankings & Proceed to Survey
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
