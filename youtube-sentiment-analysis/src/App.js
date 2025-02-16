// src/App.js
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [videoUrl, setVideoUrl] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('http://localhost:5000/analyze', { video_url: videoUrl });
      setResults(response.data);
    } catch (err) {
      setError('An error occurred while analyzing the video.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>YouTube Sentiment Analyzer</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter YouTube Video URL"
          value={videoUrl}
          onChange={(e) => setVideoUrl(e.target.value)}
          style={{ padding: '10px', width: '300px', marginRight: '10px' }}
        />
        <button type="submit" disabled={loading} style={{ padding: '10px 20px' }}>
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>

      {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}

      {results && (
        <div style={{ marginTop: '20px' }}>
          <h2>Analysis Results</h2>
          <p>Total Comments: {results.total_comments}</p>
          <p>Positive: {results.positive_percentage}%</p>
          <p>Negative: {results.negative_percentage}%</p>
          <p>Neutral: {results.neutral_percentage}%</p>
          <h3>Recommendation: <span style={{ color: results.recommendation === 'Recommended' ? 'green' : 'red' }}>
            {results.recommendation}
          </span></h3>
        </div>
      )}
    </div>
  );
}

export default App;