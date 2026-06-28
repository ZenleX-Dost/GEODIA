import React from 'react';

export const MaintenanceGantt: React.FC = () => {
  return (
    <div style={{ padding: '1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)' }}>
      <h3 style={{ fontSize: 'var(--text-base)', color: 'var(--text-primary)', marginBottom: '1rem' }}>
        Planification des Interventions (Gantt)
      </h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <span style={{ width: '100px', fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>Ouvrage R-102</span>
          <div style={{ flex: 1, display: 'flex', gap: '2px', height: '24px' }}>
            <div style={{ flex: 1, background: 'var(--status-critical)', borderRadius: '4px' }}></div>
            <div style={{ flex: 1, background: 'rgba(148, 163, 184, 0.1)', borderRadius: '4px' }}></div>
            <div style={{ flex: 1, background: 'rgba(148, 163, 184, 0.1)', borderRadius: '4px' }}></div>
            <div style={{ flex: 1, background: 'rgba(148, 163, 184, 0.1)', borderRadius: '4px' }}></div>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <span style={{ width: '100px', fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>Ouvrage R-108</span>
          <div style={{ flex: 1, display: 'flex', gap: '2px', height: '24px' }}>
            <div style={{ flex: 1, background: 'rgba(148, 163, 184, 0.1)', borderRadius: '4px' }}></div>
            <div style={{ flex: 1, background: 'var(--status-warning)', borderRadius: '4px' }}></div>
            <div style={{ flex: 1, background: 'rgba(148, 163, 184, 0.1)', borderRadius: '4px' }}></div>
            <div style={{ flex: 1, background: 'rgba(148, 163, 184, 0.1)', borderRadius: '4px' }}></div>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginTop: '0.5rem', fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>
          <span style={{ width: '100px' }}></span>
          <div style={{ flex: 1, display: 'flex', gap: '2px', textAlign: 'center' }}>
            <div style={{ flex: 1 }}>0-3 Mois</div>
            <div style={{ flex: 1 }}>3-6 Mois</div>
            <div style={{ flex: 1 }}>6-12 Mois</div>
            <div style={{ flex: 1 }}>&gt; 12 Mois</div>
          </div>
        </div>
      </div>
    </div>
  );
};
