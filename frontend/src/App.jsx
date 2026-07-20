import { useState } from 'react'

function App() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [jobId, setJobId] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleDiscover = async () => {
    if (!query) return;
    
    setLoading(true)
    setError(null)
    setResult(null)
    
    try {
      const res = await fetch('http://localhost:8000/api/discovery', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      
      const data = await res.json();
      setJobId(data.job_id);
      
      // Poll for status
      pollStatus(data.job_id);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  }

  const pollStatus = async (id) => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/discovery/${id}`);
        const data = await res.json();
        
        if (data.status === 'completed') {
          setResult(data.result);
          setLoading(false);
          clearInterval(interval);
        } else if (data.status === 'failed') {
          setError(data.result?.error || 'Unknown error occurred');
          setLoading(false);
          clearInterval(interval);
        }
      } catch (err) {
        setError(err.message);
        setLoading(false);
        clearInterval(interval);
      }
    }, 2000);
  }

  return (
    <>
      <header className="header glass-panel">
        <h1>AIDP Workspace</h1>
        <div style={{ color: 'rgba(255,255,255,0.5)' }}>Autonomous Discovery</div>
      </header>
      
      <main className="main-content">
        <div className="search-box">
          <input 
            type="text" 
            className="query-input"
            placeholder="E.g. Can we use a synthetic peptide to inhibit aggregation of alpha-synuclein..." 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleDiscover()}
          />
          <button 
            className="discover-btn" 
            onClick={handleDiscover}
            disabled={loading || !query}
          >
            {loading ? 'Initializing...' : 'Discover'}
          </button>
        </div>

        {loading && (
          <div className="glass-panel card pulse">
            <h2>Orchestrator Status</h2>
            <p>Delegating tasks to reasoning agents...</p>
          </div>
        )}

        {error && (
          <div className="glass-panel card" style={{ borderColor: 'rgba(239, 68, 68, 0.5)' }}>
            <h2 style={{ color: '#ef4444' }}>Discovery Failed</h2>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className="results-area">
            <div className="glass-panel card">
              <h2>Generated Hypothesis</h2>
              <p><strong>Claim:</strong> {result.hypothesis?.claim || 'N/A'}</p>
              <p><strong>Confidence:</strong> {result.hypothesis?.confidence?.overall_confidence || 'N/A'}</p>
              <p><strong>Rationale:</strong> {result.hypothesis?.rationale || 'N/A'}</p>
            </div>
            
            <div className="glass-panel card">
              <h2>Experiment Design</h2>
              <p><strong>Domain:</strong> {result.experiment?.domain || 'N/A'}</p>
              {result.experiment?.sampleSize && (
                <p><strong>Sample Size:</strong> {JSON.stringify(result.experiment.sampleSize)}</p>
              )}
              {result.experiment?.controls && (
                <p><strong>Controls:</strong> {JSON.stringify(result.experiment.controls)}</p>
              )}
            </div>
          </div>
        )}
      </main>
    </>
  )
}

export default App
