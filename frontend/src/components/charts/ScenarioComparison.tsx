import React from 'react';

interface ScenarioComparisonProps {
  scenarios: {
    name: string;
    description: string;
    cost: number;
    riskReduction: number;
    isOptimal?: boolean;
  }[];
}

export const ScenarioComparison: React.FC<ScenarioComparisonProps> = ({ scenarios }) => {
  return (
    <div style={{ display: 'flex', gap: '1rem' }}>
      {scenarios.map((s, idx) => (
        <div key={idx} style={{ flex: 1, padding: '1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)', border: s.isOptimal ? '2px solid var(--accent-teal)' : '1px solid var(--border-secondary)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <h4 style={{ fontSize: 'var(--text-base)', color: 'var(--text-primary)', margin: 0 }}>{s.name}</h4>
            {s.isOptimal && <span className="badge badge-success">Recommandé</span>}
          </div>
          <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)', marginBottom: '1rem' }}>{s.description}</p>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>Coût Total</span>
            <span style={{ fontSize: 'var(--text-sm)', fontWeight: 'bold', color: 'var(--text-primary)' }}>{(s.cost / 1000).toFixed(0)}k DH</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>Réduction Risque</span>
            <span style={{ fontSize: 'var(--text-sm)', fontWeight: 'bold', color: 'var(--status-success)' }}>+{s.riskReduction}%</span>
          </div>
        </div>
      ))}
    </div>
  );
};
