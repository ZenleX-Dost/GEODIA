import React, { useState } from 'react';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';

export default function Exports() {
  const [ouvrageId, setOuvrageId] = useState(1);
  const [inspectionId, setInspectionId] = useState(1);

  const handleDownloadOuvrage = () => {
    window.open(`http://localhost:8000/api/reports/pdf/ouvrage/${ouvrageId}`, '_blank');
  };

  const handleDownloadInspection = () => {
    window.open(`http://localhost:8000/api/reports/pdf/inspection/${inspectionId}`, '_blank');
  };

  const handleDownloadExcel = () => {
    window.open(`http://localhost:8000/api/reports/excel/maintenance`, '_blank');
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Génération de Rapports (Exports)</h1>
        <p className="page-subtitle">Rapports PDF, Tableaux Excel et lots ZIP</p>
      </div>

      <ScientificDisclaimer />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginTop: '2rem' }}>
        <div className="card">
          <h2 className="card-title">Fiches d'Ouvrage (PDF)</h2>
          <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Export détaillé incluant les données structurelles, les indices de santé (IPD, IAE, IAD), et le modèle probabiliste.
          </p>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <select 
              value={ouvrageId} 
              onChange={e => setOuvrageId(Number(e.target.value))}
              style={{ flex: 1, padding: '0.5rem', background: 'var(--bg-surface)', color: 'white', border: '1px solid var(--border-secondary)', borderRadius: '4px' }}
            >
              <option value="1">Ouvrage #1 (R-102)</option>
              <option value="2">Ouvrage #2 (R-105)</option>
              <option value="3">Ouvrage #3 (R-108)</option>
            </select>
            <button className="btn btn-primary" onClick={handleDownloadOuvrage}>Générer PDF</button>
          </div>
        </div>

        <div className="card">
          <h2 className="card-title">Rapports d'Inspection (PDF)</h2>
          <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Synthèse des pathologies relevées sur le terrain avec photos et notes de l'inspecteur.
          </p>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <select 
              value={inspectionId}
              onChange={e => setInspectionId(Number(e.target.value))}
              style={{ flex: 1, padding: '0.5rem', background: 'var(--bg-surface)', color: 'white', border: '1px solid var(--border-secondary)', borderRadius: '4px' }}
            >
              <option value="1">Dernière Inspection (ID: 1)</option>
            </select>
            <button className="btn btn-primary" onClick={handleDownloadInspection}>Générer PDF</button>
          </div>
        </div>

        <div className="card">
          <h2 className="card-title">Plan de Maintenance (Excel)</h2>
          <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Export du tableau de bord complet avec le plan d'intervention, les coûts estimés et les horizons recommandés.
          </p>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <select style={{ flex: 1, padding: '0.5rem', background: 'var(--bg-surface)', color: 'white', border: '1px solid var(--border-secondary)', borderRadius: '4px' }}>
              <option>Scénario S2 (Équilibré)</option>
              <option>Scénario S1 (Économique)</option>
            </select>
            <button className="btn btn-primary" onClick={handleDownloadExcel}>Générer Excel</button>
          </div>
        </div>
      </div>
    </div>
  );
}
