import React, { useState } from 'react';
import { IAELineChart } from '../components/charts/IAELineChart';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';

export default function Environment() {
  const [ouvrageId, setOuvrageId] = useState<number>(1);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Environnement</h1>
        <p className="page-subtitle">Suivi des variables climatiques et de l'agressivité de l'environnement (IAE)</p>
      </div>

      <ScientificDisclaimer />

      <div style={{ display: 'flex', gap: '2rem', marginTop: '2rem' }}>
        <div className="card" style={{ flex: 1 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h2 className="card-title">Séries Temporelles</h2>
            <span className="badge badge-simulated">DONNÉES SIMULÉES (NASA POWER)</span>
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>Sélectionner un ouvrage:</label>
            <select 
              value={ouvrageId} 
              onChange={(e) => setOuvrageId(Number(e.target.value))}
              style={{ display: 'block', width: '200px', padding: '0.5rem', background: 'var(--bg-surface)', color: 'white', border: '1px solid var(--border-secondary)', borderRadius: '4px', marginTop: '0.5rem' }}
            >
              {[1, 2, 3, 4, 5].map(id => (
                <option key={id} value={id}>Ouvrage {id}</option>
              ))}
            </select>
          </div>

          <IAELineChart />
        </div>

        <div className="card" style={{ flex: 1 }}>
          <h2 className="card-title">Agressivité de l'Environnement (IAE)</h2>
          <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            L'Indice d'Altération Environnementale (IAE) est calculé sur la base des sous-scores suivants :
          </p>
          
          <table className="data-table">
            <thead>
              <tr>
                <th>Paramètre</th>
                <th>Valeur Moyenne</th>
                <th>Sous-score</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Température (T)</td>
                <td>22.5 °C</td>
                <td><span className="badge badge-high">Élevé</span></td>
              </tr>
              <tr>
                <td>Humidité (H)</td>
                <td>78.0 %</td>
                <td><span className="badge badge-critical">Critique</span></td>
              </tr>
              <tr>
                <td>Exposition Marine (M)</td>
                <td>Splash Zone</td>
                <td><span className="badge badge-critical">Critique</span></td>
              </tr>
              <tr>
                <td>Pluviométrie (R)</td>
                <td>350 mm/an</td>
                <td><span className="badge badge-warning">Moyen</span></td>
              </tr>
              <tr>
                <td>Pollution (P)</td>
                <td>Faible SO2</td>
                <td><span className="badge badge-success">Faible</span></td>
              </tr>
            </tbody>
          </table>

          <div style={{ marginTop: '2rem', padding: '1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)', textAlign: 'center' }}>
            <div style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>IAE Global - Ouvrage {ouvrageId}</div>
            <div style={{ fontSize: 'var(--text-4xl)', fontWeight: 'bold', color: 'var(--status-critical)' }}>0.82</div>
            <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)', marginTop: '0.5rem' }}>Environnement très agressif</div>
          </div>
        </div>
      </div>
    </div>
  );
}
