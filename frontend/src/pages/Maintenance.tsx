import React, { useState, useEffect } from 'react';
import { MaintenanceGantt } from '../components/charts/MaintenanceGantt';
import { ScenarioComparison } from '../components/charts/ScenarioComparison';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';
import { apiFetch } from '../api/client';

export default function Maintenance() {
  const [budget, setBudget] = useState(150000);
  const [loading, setLoading] = useState(false);
  const [actions, setActions] = useState<any[]>([]);
  const [allActions, setAllActions] = useState<any[]>([]);
  const [scenarios, setScenarios] = useState([
    { name: 'S1: Économique', description: 'Optimisation pure sous contrainte budgétaire stricte.', cost: 850000, riskReduction: 45 },
    { name: 'S2: Équilibré', description: 'Force la réalisation des actions de Classe A.', cost: 980000, riskReduction: 65, isOptimal: true },
    { name: 'S3: Sécurité Max', description: 'Ignore le budget pour les actions à fort impact (>80%).', cost: 1250000, riskReduction: 85 }
  ]);

  useEffect(() => {
    apiFetch('/maintenance/actions')
      .then(data => setAllActions(data))
      .catch(err => console.error("Failed to load actions", err));
  }, []);

  const handleOptimize = async () => {
    setLoading(true);
    try {
      const [s1, s2, s3] = await Promise.all([
        apiFetch<any>('/compute/optimize', { method: 'POST', body: JSON.stringify({ scenario_id: 'S1', budget }) }),
        apiFetch<any>('/compute/optimize', { method: 'POST', body: JSON.stringify({ scenario_id: 'S2', budget }) }),
        apiFetch<any>('/compute/optimize', { method: 'POST', body: JSON.stringify({ scenario_id: 'S3', budget }) })
      ]);
      
      setScenarios([
        { name: 'S1: Économique', description: 'Optimisation pure sous contrainte budgétaire stricte.', cost: s1.total_cost || 0, riskReduction: s1.total_gain ? (s1.total_gain * 100).toFixed(1) as any : 0, isOptimal: s1.status === 'Optimal' },
        { name: 'S2: Équilibré', description: 'Force la réalisation des urgences immédiates (0-3m).', cost: s2.total_cost || 0, riskReduction: s2.total_gain ? (s2.total_gain * 100).toFixed(1) as any : 0, isOptimal: s2.status === 'Optimal' },
        { name: 'S3: Sécurité Max', description: 'Force les urgences à court terme (0-6m).', cost: s3.total_cost || 0, riskReduction: s3.total_gain ? (s3.total_gain * 100).toFixed(1) as any : 0, isOptimal: s3.status === 'Optimal' }
      ]);

      const activeScenario = s2.status === 'Optimal' ? s2 : (s1.status === 'Optimal' ? s1 : { selected_actions_ids: [] });

      const realGanttActions = activeScenario.selected_actions_ids.map((id: number) => {
        const realAction = allActions.find(a => a.id === id);
        if (realAction) {
          return {
            ouvrage: `Ouvrage #${realAction.ouvrage_id}`,
            action: realAction.type_action || 'Intervention planifiée',
            urgency: realAction.urgence || 'À planifier'
          };
        }
        return {
          ouvrage: `Ouvrage ID:${id}`,
          action: 'Intervention planifiée',
          urgency: 'À planifier'
        };
      });
      setActions(realGanttActions);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

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
                min="50000" 
                max="400000" 
                step="25000" 
                value={budget} 
                onChange={(e) => setBudget(Number(e.target.value))} 
                style={{ width: '100%', marginBottom: '0.5rem' }}
              />
              <div style={{ textAlign: 'right', fontSize: 'var(--text-lg)', fontWeight: 'bold', color: 'var(--text-primary)' }}>
                {(budget / 1000).toFixed(0)} k DH
              </div>
            </div>
            <button className="btn btn-primary" style={{ width: '100%' }} onClick={handleOptimize} disabled={loading}>
              {loading ? 'Optimisation en cours...' : 'Relancer l\'Optimisation'}
            </button>
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
          <MaintenanceGantt actions={actions} />
          
          <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'flex-end' }}>
            <button className="btn btn-secondary">Exporter Excel</button>
          </div>
        </div>
      </div>
    </div>
  );
}
