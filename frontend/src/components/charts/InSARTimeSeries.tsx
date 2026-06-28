import React from 'react';

export const InSARTimeSeries: React.FC = () => {
  return (
    <div style={{ padding: '1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)' }}>
      <h3 style={{ fontSize: 'var(--text-base)', color: 'var(--text-primary)', marginBottom: '1rem' }}>
        Série Temporelle InSAR (LOS Displacement)
      </h3>
      <div style={{ position: 'relative', height: '300px', display: 'flex', alignItems: 'center', borderLeft: '1px solid var(--border-secondary)', borderBottom: '1px solid var(--border-secondary)' }}>
        {/* Placeholder for InSAR points line chart */}
        <svg viewBox="0 0 100 100" preserveAspectRatio="none" style={{ width: '100%', height: '100%' }}>
          <polyline 
            fill="none" 
            stroke="var(--accent-teal)" 
            strokeWidth="1.5" 
            points="0,50 10,52 20,48 30,55 40,60 50,75 60,78 70,82 80,85 90,92 100,95" 
          />
          {/* Threshold line */}
          <line x1="0" y1="80" x2="100" y2="80" stroke="var(--status-critical)" strokeWidth="1" strokeDasharray="4" />
        </svg>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', marginTop: '1rem', fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
          <div style={{ width: '10px', height: '2px', background: 'var(--accent-teal)' }} /> Déplacement (mm)
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
          <div style={{ width: '10px', height: '2px', background: 'var(--status-critical)' }} /> Seuil Critique (-10mm)
        </span>
      </div>
    </div>
  );
};
