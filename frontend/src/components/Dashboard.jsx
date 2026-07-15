import React, { useState, useEffect } from 'react';
import { LogOut, Heart, List, UserCheck, RefreshCw } from 'lucide-react';

export default function Dashboard({ token, onLogout }) {
  const [userEmail, setUserEmail] = useState('');
  const [favorites, setFavorites] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Decode JWT payload locally to extract user info
  useEffect(() => {
    if (token) {
      try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
          window.atob(base64)
            .split('')
            .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
            .join('')
        );
        const payload = JSON.parse(jsonPayload);
        setUserEmail(payload.email || 'Usuario');
      } catch (e) {
        setUserEmail('Usuario');
      }
    }
  }, [token]);

  const fetchFavorites = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/v1/favorites', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('No se pudieron cargar los favoritos.');
      }

      const data = await response.json();
      setFavorites(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchFavorites();
  }, [token]);

  return (
    <div className="dashboard-container">
      <div className="user-avatar">
        {userEmail ? userEmail[0].toUpperCase() : 'U'}
      </div>

      <div className="card-header">
        <h2 className="card-title">¡Bienvenido de nuevo!</h2>
        <p className="card-subtitle">Has iniciado sesión correctamente</p>
      </div>

      <div className="dashboard-card-list">
        <div className="info-item">
          <span className="info-label">Usuario:</span>
          <span className="info-value">{userEmail}</span>
        </div>
        <div className="info-item">
          <span className="info-label">Estado de sesión:</span>
          <span className="status-badge">
            <UserCheck size={14} />
            Activo
          </span>
        </div>
      </div>

      <div style={{ textAlign: 'left', marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '600', color: 'var(--text-primary)' }}>Mis Favoritos</h3>
          <button 
            onClick={fetchFavorites} 
            style={{ background: 'none', border: 'none', color: '#a855f7', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px' }}
            disabled={isLoading}
          >
            <RefreshCw size={14} className={isLoading ? 'spinner' : ''} />
          </button>
        </div>

        {isLoading && favorites.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '20px 0', color: 'var(--text-secondary)' }}>
            Cargando favoritos...
          </div>
        ) : error ? (
          <div style={{ color: 'var(--text-error)', fontSize: '14px', padding: '10px 0' }}>
            {error}
          </div>
        ) : favorites.length === 0 ? (
          <div style={{ background: 'rgba(255,255,255,0.01)', border: '1px dashed var(--glass-border)', borderRadius: '12px', padding: '20px', textAlign: 'center', color: 'var(--text-secondary)', fontSize: '14px' }}>
            Aún no tienes listas de favoritos. ¡Crea una en la API!
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {favorites.map((fav) => (
              <div 
                key={fav.id} 
                style={{ 
                  background: 'rgba(255,255,255,0.02)', 
                  border: '1px solid var(--glass-border)', 
                  borderRadius: '12px', 
                  padding: '12px 16px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}
              >
                <div>
                  <div style={{ fontWeight: '600', color: 'var(--text-primary)', fontSize: '14px' }}>{fav.name}</div>
                  <div style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>{fav.description || 'Sin descripción'}</div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#ec4899', fontSize: '13px', fontWeight: '500' }}>
                  <Heart size={14} fill="#ec4899" />
                  <span>{fav.products ? fav.products.length : 0}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <button onClick={onLogout} className="btn" style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.2)', color: '#f87171', marginTop: '10px' }}>
        <LogOut size={20} />
        <span>Cerrar Sesión</span>
      </button>
    </div>
  );
}
