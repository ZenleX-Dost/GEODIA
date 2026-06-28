import React, { useState } from 'react';
import { MaintenanceGantt } from '../components/charts/MaintenanceGantt';
import { ScenarioComparison } from '../components/charts/ScenarioComparison';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';

export default function Maintenance() {
  const [budget, setBudget] = useState(1000000);
  const scenarios = [
    { name: 'S1: Économique', description: 'Optimisation pure sous contrainte budgétaire stricte.', cost: 850000, riskReduction: 45 },
    { name: 'S2: Équilibré', description: 'Force la réalisation des actions de Classe A.', cost: 980000, riskReduction: 65, isOptimal: true },
    { name: 'S3: Sécurité Max', description: 'Ignore le budget pour les actions à fort impact (>80%).', cost: 1250000, riskReduction: 85 }
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Maintenance & Optimisation</h1>
        <p className="page-subtitle">Planification intelligente et allocation budgétaire (Solveur PuLP)</p>
      </div>

      <ScientificDisclaimer />

      <div style={{ display: 'flex', gap: '2rem', marginTop: '2rem' }}>
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          <div className="card">
            <h2 className="card-title">Paramètres d'Optimisation</h2>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.5rem' }}>Budget Annuel (DH)</label>
              <input 
                type="range" 
                min="500000" 
                max="5000000" 
                step="100000" 
                value={budget} 
                onChange={(e) => setBudget(Number(e.target.value))} 
                style={{ width: '100%', marginBottom: '0.5rem' }}
              />
              <div style={{ textAlign: 'right', fontSize: 'var(--text-lg)', fontWeight: 'bold', color: 'var(--text-primary)' }}>
                {(budget / 1000000).toFixed(1)} M DH
              </div>
            </div>
            <button className="btn btn-primary" style={{ width: '100%' }}>Relancer l'Optimisation</button>
          </div>

          <div className="card">
            <h2 className="card-title">Comparaison des Scénarios</h2>
            <ScenarioComparison scenarios={scenarios} />
          </div>
        </div>

        <div className="card" style={{ flex: 2 }}>
          <h2 className="card-title">Plan de Maintenance Recommandé (S2)</h2>
          <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Horizon temporel généré par l'algorithme d'optimisation (basé sur IPD, IAE, IAD).
          </p>
          <MaintenanceGantt />
          
          <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'flex-end' }}>
            <button className="btn btn-secondary">Exporter Excel</button>
          </div>
        </div>
      </div>
    </div>
  );
}
