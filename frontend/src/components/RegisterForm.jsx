import React, { useState } from 'react';
import { User, Mail, Lock, UserPlus, AlertCircle, CheckCircle2 } from 'lucide-react';

export default function RegisterForm({ onRegisterSuccess, onSwitchToLogin }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);

    if (password !== confirmPassword) {
      setError('Las contraseñas no coinciden.');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Error al registrar el usuario. Por favor intenta de nuevo.');
      }

      setSuccess(true);
      setTimeout(() => {
        onSwitchToLogin();
      }, 2000);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <div className="card-header">
        <h2 className="card-title">Crear Cuenta</h2>
        <p className="card-subtitle">Regístrate para comenzar a guardar tus favoritos</p>
      </div>

      {error && (
        <div className="alert alert-error">
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          <CheckCircle2 size={18} />
          <span>¡Cuenta creada con éxito! Redirigiendo...</span>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <div className="input-container">
            <input
              type="text"
              className="form-input"
              placeholder="Nombre de usuario"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <User className="input-icon" size={20} />
          </div>
        </div>

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

        <div className="form-group">
          <div className="input-container">
            <input
              type="password"
              className="form-input"
              placeholder="Confirmar contraseña"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
            <Lock className="input-icon" size={20} />
          </div>
        </div>

        <button type="submit" className="btn btn-primary" disabled={isLoading || success}>
          {isLoading ? (
            <div className="spinner" />
          ) : (
            <>
              <UserPlus size={20} />
              <span>Registrarse</span>
            </>
          )}
        </button>
      </form>

      <div className="card-footer">
        <span>¿Ya tienes una cuenta?</span>
        <button type="button" className="footer-link" onClick={onSwitchToLogin} disabled={success}>
          Inicia sesión
        </button>
      </div>
    </div>
  );
}
