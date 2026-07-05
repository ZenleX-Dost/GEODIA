import React, { useState, useEffect } from 'react';
import { InSARTimeSeries } from '../components/charts/InSARTimeSeries';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';
import { apiFetch } from '../api/client';
import type { Ouvrage } from '../types/ouvrage';

export default function InSAR() {
  const [ouvrageId, setOuvrageId] = useState<number>(1);
  const [ouvrages, setOuvrages] = useState<Ouvrage[]>([]);
  const [timeseries, setTimeseries] = useState<any[]>([]);
  const [consensus, setConsensus] = useState({ strong: 0, medium: 0, weak: 0 });

  useEffect(() => {
    apiFetch('/assets').then(data => {
      setOuvrages(data);
      if (data.length > 0) {
        setOuvrageId(data[0].id);
      }
    }).catch(err => console.error("Failed to load ouvrages", err));
  }, []);

  useEffect(() => {
    if (ouvrageId) {
      apiFetch(`/insar/${ouvrageId}/summary`)
        .then(data => {
          setTimeseries(data.timeseries);
          setConsensus(data.consensus);
        })
        .catch(err => console.error("Failed to load insar summary", err));
    }
  }, [ouvrageId]);
  
  const [isRecomputing, setIsRecomputing] = useState(false);
  const [lastRecompute, setLastRecompute] = useState<string | null>(null);

  const handleRecompute = async () => {
    setIsRecomputing(true);
    try {
      const res = await fetch('http://localhost:8000/api/insar/recompute', { method: 'POST' });
      const data = await res.json();
      if (data.status === 'success') {
        setLastRecompute(new Date().toLocaleTimeString());
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsRecomputing(false);
    }
  };

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
            <div style={{ display: 'flex', gap: '1rem' }}>
              <button className="btn btn-primary btn-sm" onClick={handleRecompute} disabled={isRecomputing}>
                {isRecomputing ? 'Calcul ML en cours...' : 'Lancer le Calcul ML'}
              </button>
            </div>
          </div>
          
          {lastRecompute && (
            <div style={{ padding: '0.5rem', background: 'rgba(34, 197, 94, 0.1)', color: 'var(--status-success)', borderRadius: '4px', fontSize: 'var(--text-sm)', marginBottom: '1rem' }}>
              ✓ Modèles ML (Isolation Forest, DBSCAN) mis à jour à {lastRecompute}.
            </div>
          )}

          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>Sélectionner un ouvrage:</label>
            <select 
              value={ouvrageId}
              onChange={(e) => setOuvrageId(Number(e.target.value))}
              style={{ padding: '0.25rem 0.5rem', background: 'var(--bg-surface)', color: 'var(--text-primary)', border: '1px solid var(--border-secondary)', borderRadius: '4px', fontSize: 'var(--text-sm)', fontFamily: 'var(--font-mono)' }}
            >
              {ouvrages.map(o => (
                <option key={o.id} value={o.id}>{o.nom}</option>
              ))}
            </select>
          </div>

          <InSARTimeSeries data={timeseries} />
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
                <span className="badge badge-critical">{consensus.strong} Points</span>
              </div>
              <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)', marginTop: '0.5rem' }}>
                Anomalies confirmées par les 3 modèles. Action requise immédiate (ex: Nivellement).
              </p>
            </div>
            
            <div style={{ padding: '1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)', borderLeft: '3px solid var(--status-warning)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <strong>Consensus Moyen (2/3)</strong>
                <span className="badge badge-warning">{consensus.medium} Points</span>
              </div>
              <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)', marginTop: '0.5rem' }}>
                Détection partielle. À surveiller lors de la prochaine acquisition.
              </p>
            </div>
            
            <div style={{ padding: '1rem', background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)', borderLeft: '3px solid var(--status-info)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <strong>Consensus Faible (1/3)</strong>
                <span className="badge badge-info">{consensus.weak} Points</span>
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
