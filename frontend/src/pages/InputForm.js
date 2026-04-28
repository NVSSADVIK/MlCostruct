import React, { useState } from 'react';
import './InputForm.css';

function InputForm() {
  const [formData, setFormData] = useState({
    current_price: 5000,
    historical_prices: '4800,4900,4950,5000,5050',
    stock_level: 15000,
    daily_usage: 500,
    num_workers: 15,
    worker_efficiency: '65,70,75',
  });

  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: isNaN(value) ? value : parseFloat(value)
    }));
  };

  const parseArrayInput = (input) => {
    return input.split(',').map(val => parseFloat(val.trim())).filter(v => !isNaN(v));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setError(null);

      // Validate inputs
      if (!formData.current_price || !formData.stock_level || !formData.daily_usage) {
        throw new Error('Please fill in all required fields');
      }

      const requestData = {
        current_price: formData.current_price,
        historical_prices: parseArrayInput(formData.historical_prices),
        stock_level: formData.stock_level,
        daily_usage: formData.daily_usage,
        num_workers: formData.num_workers,
        worker_efficiency: parseArrayInput(formData.worker_efficiency),
      };

      // Validate arrays
      if (requestData.historical_prices.length === 0) {
        throw new Error('Please enter at least one historical price');
      }

      const response = await fetch('http://localhost:5000/api/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to get recommendations');
      }

      setRecommendations(data.recommendation);
    } catch (err) {
      setError(err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadSampleData = () => {
    setFormData({
      current_price: 5250,
      historical_prices: '4800,4900,4950,5000,5050,5150,5250',
      stock_level: 12000,
      daily_usage: 450,
      num_workers: 18,
      worker_efficiency: '68,72,65,70',
    });
    setRecommendations(null);
  };

  return (
    <div className="input-form-container">
      <div className="form-section">
        <h2>📝 Input Construction Data</h2>
        <p className="form-description">Enter your construction project parameters to get AI-powered recommendations</p>

        <form onSubmit={handleSubmit} className="form">
          {/* Price Section */}
          <fieldset className="form-group">
            <legend>💰 Price Information</legend>
            
            <div className="form-row">
              <div className="form-field">
                <label htmlFor="current_price">Current Cement Price (₹) *</label>
                <input
                  type="number"
                  id="current_price"
                  name="current_price"
                  value={formData.current_price}
                  onChange={handleInputChange}
                  step="10"
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-field">
                <label htmlFor="historical_prices">Past 7 Week Prices (comma-separated) *</label>
                <textarea
                  id="historical_prices"
                  name="historical_prices"
                  value={formData.historical_prices}
                  onChange={handleInputChange}
                  rows="2"
                  placeholder="e.g., 4800,4900,4950,5000,5050"
                  required
                />
                <small>Enter prices in ascending order of time</small>
              </div>
            </div>
          </fieldset>

          {/* Stock Section */}
          <fieldset className="form-group">
            <legend>📦 Stock & Usage Information</legend>
            
            <div className="form-row">
              <div className="form-field">
                <label htmlFor="stock_level">Current Stock Level (units) *</label>
                <input
                  type="number"
                  id="stock_level"
                  name="stock_level"
                  value={formData.stock_level}
                  onChange={handleInputChange}
                  step="100"
                  required
                />
              </div>

              <div className="form-field">
                <label htmlFor="daily_usage">Daily Usage Rate (units/day) *</label>
                <input
                  type="number"
                  id="daily_usage"
                  name="daily_usage"
                  value={formData.daily_usage}
                  onChange={handleInputChange}
                  step="10"
                  required
                />
              </div>
            </div>
          </fieldset>

          {/* Worker Section */}
          <fieldset className="form-group">
            <legend>👷 Worker Information</legend>
            
            <div className="form-row">
              <div className="form-field">
                <label htmlFor="num_workers">Number of Workers *</label>
                <input
                  type="number"
                  id="num_workers"
                  name="num_workers"
                  value={formData.num_workers}
                  onChange={handleInputChange}
                  step="1"
                  required
                />
              </div>

              <div className="form-field">
                <label htmlFor="worker_efficiency">Worker Efficiency Scores (comma-separated, 0-100)</label>
                <textarea
                  id="worker_efficiency"
                  name="worker_efficiency"
                  value={formData.worker_efficiency}
                  onChange={handleInputChange}
                  rows="2"
                  placeholder="e.g., 65,70,75"
                />
                <small>Optional: Leave empty for default (60)</small>
              </div>
            </div>
          </fieldset>

          {/* Buttons */}
          <div className="form-buttons">
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Analyzing...' : '🚀 Get Recommendations'}
            </button>
            <button type="button" className="btn-secondary" onClick={loadSampleData}>
              📊 Load Sample Data
            </button>
          </div>

          {error && <div className="error-message">{error}</div>}
        </form>
      </div>

      {/* Recommendations Display */}
      {recommendations && (
        <div className="recommendations-section">
          <h2>💡 Recommendations</h2>
          
          <div className="recommendations-grid">
            <div className="rec-card rec-decision">
              <div className="rec-icon">🛒</div>
              <div className="rec-content">
                <h3>Buy Decision</h3>
                <p className="rec-value">{recommendations.buy_decision}</p>
              </div>
            </div>

            <div className={`rec-card rec-risk rec-risk-${recommendations.risk.toLowerCase()}`}>
              <div className="rec-icon">⚠️</div>
              <div className="rec-content">
                <h3>Risk Level</h3>
                <p className="rec-value">{recommendations.risk}</p>
              </div>
            </div>

            <div className="rec-card rec-efficiency">
              <div className="rec-icon">📊</div>
              <div className="rec-content">
                <h3>Efficiency</h3>
                <p className="rec-value">{recommendations.avg_efficiency}%</p>
              </div>
            </div>

            <div className="rec-card rec-stock">
              <div className="rec-icon">📦</div>
              <div className="rec-content">
                <h3>Stock Days</h3>
                <p className="rec-value">{recommendations.days_of_stock} days</p>
              </div>
            </div>
          </div>

          <div className="rec-details">
            <div className="detail-box">
              <h4>📋 Reorder Suggestion</h4>
              <p>{recommendations.reorder_suggestion}</p>
            </div>

            <div className="detail-box">
              <h4>👷 Worker Allocation Plan</h4>
              <p>{recommendations.worker_plan}</p>
            </div>

            <div className="detail-box">
              <h4>📈 Price Trend</h4>
              <p>{recommendations.price_trend === 'uptrend' ? '📈 Prices Increasing' : '📉 Prices Decreasing'}</p>
            </div>

            {recommendations.predicted_prices && (
              <div className="detail-box">
                <h4>🔮 Predicted Prices (Next 7 Weeks)</h4>
                <div className="price-list">
                  {recommendations.predicted_prices.map((price, idx) => (
                    <span key={idx} className="price-badge">
                      Week {idx + 1}: ₹{price.toLocaleString()}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default InputForm;
