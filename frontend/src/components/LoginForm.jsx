import React, { useState } from 'react';
import { Mail, Lock, LogIn, AlertCircle } from 'lucide-react';

export default function LoginForm({ onLoginSuccess, onSwitchToRegister }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Error de credenciales. Por favor intenta de nuevo.');
      }

      onLoginSuccess(data.access_token);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="card-header">
        <h2 className="card-title">Iniciar Sesión</h2>
        <p className="card-subtitle">Ingresa tus datos para acceder a tu cuenta</p>
      </div>

      {error && (
        <div className="alert alert-error">
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <div className="input-container">
            <input
              type="email"
              className="form-input"
              placeholder="Correo electrónico"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <Mail className="input-icon" size={20} />
          </div>
        </div>

        <div className="form-group">
          <div className="input-container">
            <input
              type="password"
              className="form-input"
              placeholder="Contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <Lock className="input-icon" size={20} />
          </div>
        </div>

        <button type="submit" className="btn btn-primary" disabled={isLoading}>
          {isLoading ? (
            <div className="spinner" />
          ) : (
            <>
              <LogIn size={20} />
              <span>Entrar</span>
            </>
          )}
        </button>
      </form>

      <div className="card-footer">
        <span>¿No tienes una cuenta?</span>
        <button type="button" className="footer-link" onClick={onSwitchToRegister}>
          Regístrate aquí
        </button>
      </div>
    </div>
  );
}
