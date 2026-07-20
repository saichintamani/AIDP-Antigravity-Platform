import React, { useState } from 'react';

export default function Onboarding({ onComplete }) {
  const [evaluatorId, setEvaluatorId] = useState('');
  const [fieldOfExpertise, setFieldOfExpertise] = useState('');
  const [yearsExperience, setYearsExperience] = useState('');
  const [affiliation, setAffiliation] = useState('');
  const [specialization, setSpecialization] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (evaluatorId && fieldOfExpertise && yearsExperience && affiliation && specialization) {
      onComplete({ 
        evaluatorId, 
        fieldOfExpertise, 
        yearsExperience, 
        affiliation, 
        specialization 
      });
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white shadow rounded-lg mt-10">
      <h1 className="text-3xl font-bold mb-4">Track E: Independent Evaluation</h1>
      <p className="mb-6 text-gray-700">
        Welcome to the AIDP independent human evaluation track. You will be presented with historical scientific data from moments before major paradigm shifts. Your task is to rank the candidate experiments based on their epistemic value—which experiment would yield the most information to resolve the current uncertainty?
      </p>
      
      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
        <p className="font-bold">Strict Rule:</p>
        <p>Do not use search engines. Base your decisions strictly on the provided evidence and constraints. The outcome of the historical case has been masked.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Evaluator ID (or Alias)</label>
          <input 
            type="text" 
            required 
            value={evaluatorId}
            onChange={e => setEvaluatorId(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border" 
            placeholder="e.g. expert_bio_01"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700">Field of Expertise</label>
          <input 
            type="text" 
            required 
            value={fieldOfExpertise}
            onChange={e => setFieldOfExpertise(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border" 
            placeholder="e.g. Molecular Biology, Physics, Medicine"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Years of Experience</label>
          <select 
            required
            value={yearsExperience}
            onChange={e => setYearsExperience(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          >
            <option value="">Select Level...</option>
            <option value="0-5">0-5 Years</option>
            <option value="5-10">5-10 Years</option>
            <option value="10+">10+ Years</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Affiliation</label>
          <select 
            required
            value={affiliation}
            onChange={e => setAffiliation(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
          >
            <option value="">Select Affiliation...</option>
            <option value="Academic">Academic</option>
            <option value="Industry">Industry</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Specialization (e.g. Immunology, RNA, Condensed Matter)</label>
          <input 
            type="text" 
            required 
            value={specialization}
            onChange={e => setSpecialization(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border" 
            placeholder="Brief description"
          />
        </div>

        <button type="submit" className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition">
          Begin Evaluation
        </button>
      </form>
    </div>
  );
}
