import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import InputForm from './pages/InputForm';
import Recommendations from './pages/Recommendations';
import './App.css';

function App() {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Check if backend is running
    fetch('http://localhost:5000/api/health')
      .then(res => res.json())
      .then(() => setIsConnected(true))
      .catch(() => setIsConnected(false));
  }, []);

  return (
    <Router>
      <div className="app">
        <header className="header">
          <div className="header-content">
            <h1>🧱 Smart Construction Recommendation System</h1>
            <p className="status">
              Backend Status: <span className={isConnected ? 'status-ok' : 'status-error'}>
                {isConnected ? '✓ Connected' : '✗ Disconnected'}
              </span>
            </p>
          </div>
        </header>

        <nav className="navigation">
          <ul>
            <li><Link to="/">📊 Dashboard</Link></li>
            <li><Link to="/input">📝 Input Data</Link></li>
            <li><Link to="/recommendations">👷‍♀️ History</Link></li>
          </ul>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/input" element={<InputForm />} />
            <Route path="/recommendations" element={<Recommendations />} />
          </Routes>
        </main>

        <footer className="footer">
          <p>&copy; 2024 Smart Construction System. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
