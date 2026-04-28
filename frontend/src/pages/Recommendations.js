import React, { useState, useEffect } from 'react';
import './Recommendations.css';

function Recommendations() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRecommendationHistory();
  }, []);

  const fetchRecommendationHistory = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:5000/api/recommendation_history');
      const data = await response.json();

      if (data.status === 'success') {
        setHistory(data.history || []);
      } else {
        setError('Failed to fetch recommendations');
      }
    } catch (err) {
      setError('Failed to connect to backend. Make sure the server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleString();
    } catch {
      return dateString;
    }
  };

  const getRiskStyle = (risk) => {
    const colors = {
      'Low': { bg: '#e8f5e9', text: '#2e7d32', icon: '✓' },
      'Medium': { bg: '#fff3e0', text: '#e65100', icon: '⚠️' },
      'High': { bg: '#ffebee', text: '#d32f2f', icon: '⚠️' }
    };
    return colors[risk] || colors['Low'];
  };

  if (loading) {
    return <div className="loading">Loading recommendations...</div>;
  }

  return (
    <div className="recommendations-page">
      <h2>📋 Recommendation History</h2>
      <p className="page-description">View all past recommendations and decisions</p>

      {error && <div className="error-message">{error}</div>}

      {history.length === 0 ? (
        <div className="no-data">
          <p>No recommendations yet. <a href="/input">Generate a new recommendation</a></p>
        </div>
      ) : (
        <div className="history-container">
          {history.map((rec, idx) => {
            const riskStyle = getRiskStyle(rec.risk_level);
            return (
              <div key={idx} className="recommendation-item">
                <div className="rec-header">
                  <div className="rec-timestamp">
                    🕐 {formatDate(rec.created_at)}
                  </div>
                  <div className="rec-id">
                    #{idx + 1}
                  </div>
                </div>

                <div className="rec-body">
                  <div className="rec-grid">
                    {/* Price */}
                    <div className="rec-info-box">
                      <span className="info-label">💰 Current Price</span>
                      <span className="info-value">₹{rec.current_price?.toLocaleString()}</span>
                    </div>

                    {/* Stock */}
                    <div className="rec-info-box">
                      <span className="info-label">📦 Stock Level</span>
                      <span className="info-value">{rec.stock_level?.toLocaleString()} units</span>
                    </div>

                    {/* Daily Usage */}
                    <div className="rec-info-box">
                      <span className="info-label">⚙️ Daily Usage</span>
                      <span className="info-value">{rec.daily_usage?.toLocaleString()} units/day</span>
                    </div>

                    {/* Risk Level */}
                    <div className="rec-info-box">
                      <span className="info-label">Risk Assessment</span>
                      <span 
                        className="info-value risk-badge"
                        style={{
                          backgroundColor: riskStyle.bg,
                          color: riskStyle.text
                        }}
                      >
                        {riskStyle.icon} {rec.risk_level}
                      </span>
                    </div>
                  </div>

                  <div className="rec-decisions">
                    {/* Buy Decision */}
                    <div className="decision-box buy-decision">
                      <h4>🛒 Buy Decision</h4>
                      <p>{rec.buy_decision}</p>
                    </div>

                    {/* Reorder Suggestion */}
                    <div className="decision-box reorder-suggestion">
                      <h4>📋 Reorder Suggestion</h4>
                      <p>{rec.reorder_suggestion}</p>
                    </div>

                    {/* Worker Plan */}
                    <div className="decision-box worker-plan">
                      <h4>👷 Worker Plan</h4>
                      <p>{rec.worker_plan}</p>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      <button className="refresh-history-btn" onClick={fetchRecommendationHistory}>
        🔄 Refresh History
      </button>
    </div>
  );
}

export default Recommendations;
