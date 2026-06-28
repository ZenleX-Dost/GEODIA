import React from 'react';

export const IAELineChart: React.FC = () => {
  return (
    <div style={{ padding: '1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)' }}>
      <h3 style={{ fontSize: 'var(--text-base)', color: 'var(--text-primary)', marginBottom: '1rem' }}>
        Indice d'Altération Environnementale (IAE) vs Variables Climatiques
      </h3>
      <div style={{ height: '300px', display: 'flex', alignItems: 'flex-end', gap: '8px', paddingBottom: '20px', borderBottom: '1px solid var(--border-secondary)' }}>
        {/* Simple placeholder for line chart */}
        {[30, 40, 35, 50, 45, 60, 55, 70, 65, 80, 75, 90].map((val, idx) => (
          <div key={idx} style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
            <div style={{ 
              width: '10px', 
              height: `${val}%`, 
              background: 'var(--accent-blue-light)', 
              borderRadius: '2px',
              transition: 'height 0.5s ease'
            }} />
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', marginTop: '1rem', fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
          <div style={{ width: '10px', height: '10px', background: 'var(--accent-blue-light)', borderRadius: '50%' }} /> IAE Global
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
          <div style={{ width: '10px', height: '10px', background: 'var(--status-critical)', borderRadius: '50%' }} /> Température (°C)
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
          <div style={{ width: '10px', height: '10px', background: 'var(--status-info)', borderRadius: '50%' }} /> Humidité (%)
        </span>
      </div>
    </div>
  );
};
