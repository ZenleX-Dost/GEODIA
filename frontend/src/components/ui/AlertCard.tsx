import React from 'react';

interface AlertCardProps {
  id: number;
  ouvrage_code: string;
  ouvrage_nom: string;
  severity: 'emergency' | 'critical' | 'high' | 'warning' | 'info';
  action: string;
  source: string;
  date: string;
}

export const AlertCard: React.FC<AlertCardProps> = ({ ouvrage_code, ouvrage_nom, severity, action, source, date }) => {
  let severityClass = '';
  switch (severity) {
    case 'emergency': severityClass = 'badge-emergency'; break;
    case 'critical': severityClass = 'badge-critical'; break;
    case 'high': severityClass = 'badge-high'; break;
    case 'warning': severityClass = 'badge-warning'; break;
    default: severityClass = 'badge'; break;
  }

  return (
    <div className="alert-card">
      <div className={`alert-dot ${severity}`}></div>
      <div style={{ flex: 1 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
          <strong style={{ color: 'var(--text-primary)' }}>{ouvrage_code} - {ouvrage_nom}</strong>
          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>{date}</span>
        </div>
        <p style={{ fontSize: 'var(--text-sm)', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>
          {action}
        </p>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <span className={`badge ${severityClass}`}>{severity.toUpperCase()}</span>
          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>Source: {source}</span>
        </div>
      </div>
    </div>
  );
};
