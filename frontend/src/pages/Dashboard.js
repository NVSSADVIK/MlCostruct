import React, { useState, useEffect } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import './Dashboard.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [priceHistory, setPriceHistory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [summaryRes, historyRes] = await Promise.all([
        fetch('http://localhost:5000/api/dashboard_summary'),
        fetch('http://localhost:5000/api/get_price_history'),
      ]);

      const summaryData = await summaryRes.json();
      const historyData = await historyRes.json();

      setDashboardData(summaryData);
      setPriceHistory(historyData);
      setError(null);
    } catch (err) {
      setError('Failed to fetch dashboard data. Is the backend running?');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!dashboardData) {
    return <div className="error-message">No data available</div>;
  }

  const { 
    current_price, 
    predicted_price_7d, 
    price_trend,
    worker_efficiency,
    num_workers,
    stock_level,
    daily_usage,
    days_of_stock,
    project_status
  } = dashboardData.status === 'success' ? dashboardData : {};

  // Prepare chart data
  const priceChartData = priceHistory && priceHistory.status === 'success' ? {
    labels: priceHistory.history.map(h => h.date),
    datasets: [
      {
        label: 'Cement Price (₹)',
        data: priceHistory.history.map(h => h.price),
        borderColor: '#667eea',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        tension: 0.4,
        borderWidth: 2,
      }
    ]
  } : null;

  const workerChartData = {
    labels: ['Skilled', 'Trainees', 'Supervisors'],
    datasets: [
      {
        label: 'Worker Distribution',
        data: [
          Math.round(num_workers * 0.6),
          Math.round(num_workers * 0.3),
          Math.round(num_workers * 0.1)
        ],
        backgroundColor: [
          '#4CAF50',
          '#2196F3',
          '#FF9800'
        ],
        borderColor: [
          '#388E3C',
          '#1565C0',
          '#E65100'
        ],
        borderWidth: 2,
      }
    ]
  };

  const getRiskColor = (days) => {
    if (days < 7) return '#f44336'; // Red
    if (days < 14) return '#FF9800'; // Orange
    return '#4CAF50'; // Green
  };

  const getTrendIcon = (trend) => {
    return trend === 'up' ? '📈 Increasing' : '📉 Decreasing';
  };

  return (
    <div className="dashboard">
      <h2>Dashboard Overview</h2>

      {/* Key Metrics Cards */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-icon">💰</div>
          <div className="metric-content">
            <p className="metric-label">Current Price</p>
            <p className="metric-value">₹{current_price?.toLocaleString()}</p>
            <p className="metric-subtext">{getTrendIcon(price_trend)}</p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">📊</div>
          <div className="metric-content">
            <p className="metric-label">Predicted Price (7-Week avg)</p>
            <p className="metric-value">₹{predicted_price_7d?.toLocaleString()}</p>
            <p className="metric-subtext">
              {predicted_price_7d > current_price ? '↗ Increase' : '↘ Decrease'}
            </p>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon">👷</div>
          <div className="metric-content">
            <p className="metric-label">Worker Efficiency</p>
            <p className="metric-value">{worker_efficiency?.toFixed(1)}%</p>
            <p className="metric-subtext">{num_workers} workers active</p>
          </div>
        </div>

        <div className="metric-card" style={{ borderLeftColor: getRiskColor(days_of_stock) }}>
          <div className="metric-icon">📦</div>
          <div className="metric-content">
            <p className="metric-label">Stock Days Remaining</p>
            <p className="metric-value">{days_of_stock?.toFixed(1)} days</p>
            <p className="metric-subtext">{stock_level?.toLocaleString()} units in stock</p>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <div className="chart-container">
          <h3>Price Trend (Last 20 Days)</h3>
          {priceChartData ? (
            <Line data={priceChartData} options={{
              responsive: true,
              maintainAspectRatio: true,
              plugins: {
                legend: { position: 'top' },
              },
              scales: {
                y: {
                  beginAtZero: false,
                }
              }
            }} />
          ) : (
            <p>No chart data available</p>
          )}
        </div>

        <div className="chart-container">
          <h3>Worker Distribution</h3>
          <Bar data={workerChartData} options={{
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
              legend: { position: 'top' },
            }
          }} />
        </div>
      </div>

      {/* Detailed Info */}
      <div className="info-section">
        <div className="info-card">
          <h3>Project Status</h3>
          <div className="status-badge" style={{ 
            backgroundColor: project_status === 'Active' ? '#4CAF50' : '#FF9800' 
          }}>
            {project_status || 'Active'}
          </div>
        </div>

        <div className="info-card">
          <h3>Daily Usage</h3>
          <p className="info-value">{daily_usage?.toLocaleString()} units/day</p>
        </div>

        <div className="info-card">
          <h3>Stock Alert</h3>
          {days_of_stock < 7 ? (
            <p style={{ color: '#f44336' }}>⚠️ Critical - Consider ordering now</p>
          ) : days_of_stock < 14 ? (
            <p style={{ color: '#FF9800' }}>⚠️ Warning - Plan to order soon</p>
          ) : (
            <p style={{ color: '#4CAF50' }}>✓ Stock levels healthy</p>
          )}
        </div>
      </div>

      <button className="refresh-btn" onClick={fetchDashboardData}>
        🔄 Refresh Data
      </button>
    </div>
  );
}

export default Dashboard;
