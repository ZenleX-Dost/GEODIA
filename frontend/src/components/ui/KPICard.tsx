/**
 * KPI Card component — glassmorphism card with icon, value, label, and trend.
 */
import type { ReactNode } from 'react';

interface KPICardProps {
  icon: ReactNode;
  iconColor: 'teal' | 'blue' | 'red' | 'orange' | 'yellow' | 'green';
  value: string | number;
  label: string;
  trend?: {
    direction: 'up' | 'down';
    value: string;
  };
}

export default function KPICard({ icon, iconColor, value, label, trend }: KPICardProps) {
  return (
    <div className="kpi-card">
      <div className="kpi-header">
        <div className={`kpi-icon ${iconColor}`}>{icon}</div>
        {trend && (
          <span className={`kpi-trend ${trend.direction}`}>
            {trend.direction === 'up' ? '↑' : '↓'} {trend.value}
          </span>
        )}
      </div>
      <div className="kpi-value">{value}</div>
      <div className="kpi-label">{label}</div>
    </div>
  );
}
