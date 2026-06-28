import React from 'react';

interface ProbaData {
  pathologie: string;
  probability: number;
}

interface ProbaBarChartProps {
  data: ProbaData[];
}

export const ProbaBarChart: React.FC<ProbaBarChartProps> = ({ data }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', width: '100%' }}>
      {data.map((item) => {
        let color = '#34d399'; // Low: Emerald 400
        if (item.probability >= 0.75) color = '#ef4444'; // Very High: Red
        else if (item.probability >= 0.50) color = '#f97316'; // High: Orange
        else if (item.probability >= 0.25) color = '#eab308'; // Moderate: Yellow

        return (
          <div key={item.pathologie} style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <span style={{ width: '40px', fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>
              {item.pathologie}
            </span>
            <div style={{ flex: 1, background: 'rgba(148, 163, 184, 0.1)', height: '12px', borderRadius: '4px', overflow: 'hidden' }}>
              <div 
                style={{ 
                  width: `${item.probability * 100}%`, 
                  background: color, 
                  height: '100%',
                  transition: 'width 1s ease-in-out'
                }} 
              />
            </div>
            <span style={{ width: '50px', fontSize: 'var(--text-xs)', textAlign: 'right', fontFamily: 'var(--font-mono)' }}>
              {(item.probability * 100).toFixed(1)}%
            </span>
          </div>
        );
      })}
    </div>
  );
};
