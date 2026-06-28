import React from 'react';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';

export default function Exports() {
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
            <select style={{ flex: 1, padding: '0.5rem', background: 'var(--bg-surface)', color: 'white', border: '1px solid var(--border-secondary)', borderRadius: '4px' }}>
              <option>Tous les Ouvrages (ZIP)</option>
              <option>R-102 (Déversoir Eau de Mer)</option>
              <option>R-108 (Bassin REM1)</option>
            </select>
            <button className="btn btn-primary">Générer PDF</button>
          </div>
        </div>

        <div className="card">
          <h2 className="card-title">Rapports d'Inspection (PDF)</h2>
          <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Synthèse des pathologies relevées sur le terrain avec photos et notes de l'inspecteur.
          </p>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            <select style={{ flex: 1, padding: '0.5rem', background: 'var(--bg-surface)', color: 'white', border: '1px solid var(--border-secondary)', borderRadius: '4px' }}>
              <option>Dernière Inspection (R-102)</option>
              <option>Archive Q1 2026</option>
            </select>
            <button className="btn btn-primary">Générer PDF</button>
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
            <button className="btn btn-primary">Générer Excel</button>
          </div>
        </div>
      </div>
    </div>
  );
}
