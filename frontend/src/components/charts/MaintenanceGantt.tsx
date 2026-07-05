import React from 'react';

interface MaintenanceGanttProps {
  actions: {
    ouvrage: string;
    action: string;
    urgency: string; // "Immédiate", "À planifier", "Préventif"
  }[];
}

export const MaintenanceGantt: React.FC<MaintenanceGanttProps> = ({ actions = [] }) => {
  return (
    <div style={{ padding: '1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)' }}>
      <h3 style={{ fontSize: 'var(--text-base)', color: 'var(--text-primary)', marginBottom: '1rem' }}>
        Planification des Interventions
      </h3>
      
      {actions.length === 0 ? (
        <p style={{ color: 'var(--text-tertiary)', fontSize: 'var(--text-sm)' }}>Aucune action retenue avec ce budget.</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {actions.map((act, idx) => (
            <div key={idx} style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <span style={{ width: '120px', fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }} title={act.action}>
                {act.ouvrage}
              </span>
              <div style={{ flex: 1, display: 'flex', gap: '2px', height: '24px' }}>
                <div style={{ 
                  flex: 1, 
                  background: act.urgency === '0-3m' ? 'var(--status-critical)' : 'rgba(148, 163, 184, 0.1)', 
                  borderRadius: '4px' 
                }}></div>
                <div style={{ 
                  flex: 1, 
                  background: act.urgency === '3-6m' ? 'var(--status-warning)' : 'rgba(148, 163, 184, 0.1)', 
                  borderRadius: '4px' 
                }}></div>
                <div style={{ 
                  flex: 1, 
                  background: act.urgency === '6-12m' ? 'var(--status-info)' : 'rgba(148, 163, 184, 0.1)', 
                  borderRadius: '4px' 
                }}></div>
                <div style={{ 
                  flex: 1, 
                  background: act.urgency === '>12m' || (!['0-3m', '3-6m', '6-12m'].includes(act.urgency)) ? 'var(--accent-teal)' : 'rgba(148, 163, 184, 0.1)', 
                  borderRadius: '4px' 
                }}></div>
              </div>
            </div>
          ))}
          
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginTop: '0.5rem', fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>
            <span style={{ width: '120px' }}></span>
            <div style={{ flex: 1, display: 'flex', gap: '2px', textAlign: 'center' }}>
              <div style={{ flex: 1 }}>0-3 Mois</div>
              <div style={{ flex: 1 }}>3-6 Mois</div>
              <div style={{ flex: 1 }}>6-12 Mois</div>
              <div style={{ flex: 1 }}>&gt; 12 Mois</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
