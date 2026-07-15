import React, { useState, useEffect } from 'react';
import './App.css';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import Dashboard from './components/Dashboard';

function App() {
  const [token, setToken] = useState(null);
  const [currentForm, setCurrentForm] = useState('login'); // 'login' or 'register'

  // Load token from localStorage on startup
  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    if (savedToken) {
      setToken(savedToken);
    }
  }, []);

  const handleLoginSuccess = (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setCurrentForm('login');
  };

  return (
    <div className="app-container">
      {/* Premium background mesh circles */}
      <div className="mesh-background">
        <div className="mesh-circle circle-1"></div>
        <div className="mesh-circle circle-2"></div>
        <div className="mesh-circle circle-3"></div>
      </div>

      {/* Main glass card container */}
      <div className="glass-card">
        {token ? (
          <Dashboard token={token} onLogout={handleLogout} />
        ) : currentForm === 'login' ? (
          <LoginForm
            onLoginSuccess={handleLoginSuccess}
            onSwitchToRegister={() => setCurrentForm('register')}
          />
        ) : (
          <RegisterForm
            onSwitchToLogin={() => setCurrentForm('login')}
          />
        )}
      </div>
    </div>
  );
}

export default App;
