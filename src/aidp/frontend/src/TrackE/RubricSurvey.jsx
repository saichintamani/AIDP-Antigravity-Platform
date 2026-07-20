import React, { useState } from 'react';

export default function RubricSurvey({ onSubmitSurvey }) {
  const [scores, setScores] = useState({
    epistemic_clarity: 3,
    contradiction_resolution: 3,
    physical_constraints: 3,
    confidence_alignment: 3
  });
  const [feedback, setFeedback] = useState("");

  const handleChange = (field, value) => {
    setScores(prev => ({ ...prev, [field]: parseInt(value) }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmitSurvey({ scores, feedback });
  };

  const renderRadio = (field, label, description) => (
    <div className="mb-6">
      <label className="block font-bold text-gray-800 mb-1">{label}</label>
      <p className="text-sm text-gray-500 mb-2 italic">"{description}"</p>
      <div className="flex gap-4">
        {[1, 2, 3, 4, 5].map(val => (
          <label key={val} className="flex flex-col items-center gap-1 cursor-pointer">
            <input 
              type="radio" 
              name={field} 
              value={val} 
              checked={scores[field] === val}
              onChange={(e) => handleChange(field, e.target.value)}
              className="w-4 h-4 text-blue-600"
            />
            <span className="text-sm">{val}</span>
          </label>
        ))}
      </div>
    </div>
  );

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white shadow rounded-lg mt-10">
      <h2 className="text-2xl font-bold mb-4">Post-Evaluation Rubric</h2>
      <p className="mb-6 text-gray-600">Please rate the system based on the case you just evaluated (1 = Strongly Disagree, 5 = Strongly Agree).</p>
      
      <form onSubmit={handleSubmit}>
        {renderRadio("epistemic_clarity", "Epistemic Clarity", "The tool made it easy to trace the exact source and lineage of the evidence supporting the claims.")}
        {renderRadio("contradiction_resolution", "Contradiction Resolution", "When the literature contained conflicting claims, the tool explicitly highlighted the contradiction.")}
        {renderRadio("physical_constraints", "Physical Constraint Enforcement", "The tool successfully grounded its reasoning in undeniable physical or biological constraints.")}
        {renderRadio("confidence_alignment", "Confidence Alignment", "My personal confidence in the final conclusion aligns with the confidence reported or implied by the tool.")}

        <div className="mb-6">
          <label className="block font-bold text-gray-800 mb-2">Open Feedback / Limitations</label>
          <textarea 
            value={feedback}
            onChange={e => setFeedback(e.target.value)}
            className="w-full border rounded p-2 text-gray-700 h-24"
            placeholder="What was the primary limitation of this environment? Did it state anything false without context?"
          ></textarea>
        </div>

        <button type="submit" className="w-full bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700 transition">
          Finalize Submission
        </button>
      </form>
    </div>
  );
}
