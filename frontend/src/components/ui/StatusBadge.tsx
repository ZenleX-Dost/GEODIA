import React from 'react';

type BadgeType = 'class' | 'emergency' | 'critical' | 'high' | 'warning' | 'simulated' | 'success' | 'info';

interface StatusBadgeProps {
  type: BadgeType;
  value?: string;
  label?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ type, value, label }) => {
  let className = 'badge ';
  let text = label || value;

  switch (type) {
    case 'class':
      if (value) {
        className += `badge-classe-${value.toLowerCase()}`;
        text = text || `Classe ${value.toUpperCase()}`;
      }
      break;
    case 'emergency':
      className += 'badge-emergency';
      text = text || 'Urgence';
      break;
    case 'critical':
      className += 'badge-critical';
      text = text || 'Critique';
      break;
    case 'high':
      className += 'badge-high';
      text = text || 'Élevé';
      break;
    case 'warning':
      className += 'badge-warning';
      text = text || 'Avertissement';
      break;
    case 'simulated':
      className += 'badge-simulated';
      text = text || 'Simulé';
      break;
    case 'success':
      className += 'badge-classe-d'; // reusing green styling
      text = text || 'OK';
      break;
    case 'info':
      className += 'badge'; // default styling or custom info styling if needed
      text = text || 'Info';
      break;
    default:
      break;
  }

  return <span className={className}>{text}</span>;
};
