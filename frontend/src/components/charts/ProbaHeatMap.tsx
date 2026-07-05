import React from 'react';

interface HeatMapProps {
  data: { ouvrage_id: number; probabilities: Record<string, number> }[];
  ouvrages: { id: number; nom: string }[];
  onOuvrageSelect?: (ouvrageId: number) => void;
}

export function ProbaHeatMap({ data, ouvrages, onOuvrageSelect }: HeatMapProps) {
  // Pathologies P1 to P12
  const pathologies = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12'];

  const getColor = (prob: number) => {
    if (prob < 25) return '#10b981'; // Emerald 500 (Faible)
    if (prob < 50) return '#f59e0b'; // Amber 500 (Modéré)
    if (prob < 75) return '#f97316'; // Orange 500 (Élevé)
    return '#ef4444'; // Red 500 (Très Élevé)
  };

  return (
    <div style={{ overflowX: 'auto', padding: '1.5rem', background: 'var(--bg-surface)', borderRadius: '12px', border: '1px solid var(--border-primary)', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}>
      <h3 style={{ fontSize: '1.1rem', marginBottom: '1.5rem', color: 'var(--text-primary)' }}>Heatmap du Portefeuille (Probabilités en %)</h3>
      <div style={{ display: 'grid', gridTemplateColumns: `250px repeat(${pathologies.length}, minmax(40px, 1fr))`, gap: '4px' }}>
        {/* Header Row */}
        <div style={{ padding: '0.5rem', fontWeight: 'bold', color: 'var(--text-secondary)' }}>Ouvrage</div>
        {pathologies.map(p => (
          <div key={p} style={{ padding: '0.5rem', textAlign: 'center', fontWeight: 'bold', color: 'var(--text-secondary)' }}>{p}</div>
        ))}

        {/* Data Rows */}
        {data.map(row => {
          const ouvrage = ouvrages.find(o => o.id === row.ouvrage_id);
          return (
            <React.Fragment key={row.ouvrage_id}>
              <div 
                onClick={() => onOuvrageSelect && onOuvrageSelect(row.ouvrage_id)}
                style={{ 
                  padding: '0.5rem', 
                  fontSize: '0.85rem', 
                  whiteSpace: 'nowrap', 
                  overflow: 'hidden', 
                  textOverflow: 'ellipsis',
                  color: 'var(--text-primary)',
                  display: 'flex',
                  alignItems: 'center',
                  cursor: 'pointer'
                }} 
                title={ouvrage?.nom || `Ouvrage ${row.ouvrage_id}`}
                onMouseEnter={(e) => { e.currentTarget.style.color = 'var(--primary)'; }}
                onMouseLeave={(e) => { e.currentTarget.style.color = 'var(--text-primary)'; }}
              >
                {ouvrage?.nom || `Ouvrage ${row.ouvrage_id}`}
              </div>
              {pathologies.map(p => {
                const val = row.probabilities[p] || 0;
                return (
                  <div
                    key={`${row.ouvrage_id}-${p}`}
                    onClick={() => onOuvrageSelect && onOuvrageSelect(row.ouvrage_id)}
                    style={{
                      background: getColor(val),
                      color: val > 50 || val < 25 ? '#ffffff' : '#1e293b',
                      padding: '0.5rem',
                      textAlign: 'center',
                      fontSize: '0.85rem',
                      fontWeight: '500',
                      borderRadius: '4px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      transition: 'transform 0.2s ease, opacity 0.2s ease',
                      cursor: 'pointer'
                    }}
                    onMouseEnter={(e) => { e.currentTarget.style.opacity = '0.8'; e.currentTarget.style.transform = 'scale(1.05)'; }}
                    onMouseLeave={(e) => { e.currentTarget.style.opacity = '1'; e.currentTarget.style.transform = 'scale(1)'; }}
                    title={`${ouvrage?.nom} - Pathologie ${p}: ${val.toFixed(1)}%`}
                  >
                    {val.toFixed(0)}
                  </div>
                );
              })}
            </React.Fragment>
          );
        })}
      </div>
      
      <div style={{ display: 'flex', gap: '1.5rem', marginTop: '2rem', justifyContent: 'center', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><div style={{ width: 16, height: 16, background: '#10b981', borderRadius: '4px' }}></div> &lt; 25% (Faible)</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><div style={{ width: 16, height: 16, background: '#f59e0b', borderRadius: '4px' }}></div> 25-49% (Modéré)</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><div style={{ width: 16, height: 16, background: '#f97316', borderRadius: '4px' }}></div> 50-74% (Élevé)</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}><div style={{ width: 16, height: 16, background: '#ef4444', borderRadius: '4px' }}></div> &ge; 75% (Très Élevé)</div>
      </div>
    </div>
  );
}
