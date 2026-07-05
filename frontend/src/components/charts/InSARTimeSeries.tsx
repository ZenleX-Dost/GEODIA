import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine,
  ResponsiveContainer,
} from 'recharts';

interface InSARTimeSeriesProps {
  data: { date: string; displacement: number }[];
}

export const InSARTimeSeries: React.FC<InSARTimeSeriesProps> = ({ data = [] }) => {
  return (
    <div style={{ padding: '1.5rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-secondary)' }}>
      <h3 style={{ fontSize: 'var(--text-lg)', fontWeight: '600', color: 'var(--text-primary)', marginBottom: '1.5rem' }}>
        Série Temporelle InSAR (LOS Displacement)
      </h3>
      <div style={{ height: '350px', width: '100%' }}>
        <ResponsiveContainer>
          <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(148, 163, 184, 0.1)" vertical={false} />
            <XAxis dataKey="date" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
            <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
            <Tooltip 
              contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', color: '#f8fafc' }}
              itemStyle={{ color: '#e2e8f0' }}
            />
            <Legend wrapperStyle={{ paddingTop: '20px', fontSize: '12px' }} />
            <ReferenceLine y={-10} label={{ position: 'top', value: 'Seuil Critique (-10mm)', fill: 'var(--status-critical)', fontSize: 12 }} stroke="var(--status-critical)" strokeDasharray="3 3" />
            <Line type="monotone" name="Déplacement (mm)" dataKey="displacement" stroke="var(--accent-teal)" strokeWidth={3} dot={{ r: 4, fill: 'var(--accent-teal)' }} activeDot={{ r: 6 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
