import React, { useState } from 'react';
import { InSARTimeSeries } from '../components/charts/InSARTimeSeries';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';

export default function InSAR() {
  const [ouvrageId, setOuvrageId] = useState<number>(1);

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">InSAR (Interférométrie Radar)</h1>
        <p className="page-subtitle">Détection des anomalies de déformation spatiale</p>
      </div>

      <ScientificDisclaimer />

      <div style={{ display: 'flex', gap: '2rem', marginTop: '2rem' }}>
        <div className="card" style={{ flex: 1 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
            <h2 className="card-title">Analyse des Déformations</h2>
            <button className="btn btn-secondary btn-sm">Importer CSV InSAR</button>
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

          <InSARTimeSeries />
        </div>

        <div className="card" style={{ flex: 1 }}>
          <h2 className="card-title">Consensus des Anomalies</h2>
          <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Le système utilise 3 méthodes pour valider une anomalie : Seuils experts, DBSCAN (spatial), et Isolation Forest (multivarié).
          </p>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ padding: '1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)', borderLeft: '3px solid var(--status-critical)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <strong>Consensus Fort (3/3)</strong>
                <span className="badge badge-critical">12 Points</span>
              </div>
              <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)', marginTop: '0.5rem' }}>
                Anomalies confirmées par les 3 modèles. Action requise immédiate (ex: Nivellement).
              </p>
            </div>
            
            <div style={{ padding: '1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)', borderLeft: '3px solid var(--status-warning)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <strong>Consensus Moyen (2/3)</strong>
                <span className="badge badge-warning">45 Points</span>
              </div>
              <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)', marginTop: '0.5rem' }}>
                Détection partielle. À surveiller lors de la prochaine acquisition.
              </p>
            </div>
            
            <div style={{ padding: '1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)', borderLeft: '3px solid var(--status-info)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <strong>Consensus Faible (1/3)</strong>
                <span className="badge badge-info">120 Points</span>
              </div>
              <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)', marginTop: '0.5rem' }}>
                Bruit potentiel ou artefact atmosphérique. Ignoré dans le calcul IAD.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
