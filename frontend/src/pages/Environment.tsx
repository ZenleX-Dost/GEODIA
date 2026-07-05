import React, { useState, useEffect } from 'react';
import { RefreshCw } from 'lucide-react';
import { IAELineChart } from '../components/charts/IAELineChart';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';
import { apiFetch } from '../api/client';
import type { Ouvrage } from '../types/ouvrage';

export default function Environment() {
  const [ouvrageId, setOuvrageId] = useState<number>(1);
  const [ouvrages, setOuvrages] = useState<Ouvrage[]>([]);
  const [envData, setEnvData] = useState<any[]>([]);
  const [syncingNasa, setSyncingNasa] = useState(false);
  const [syncingCopernicus, setSyncingCopernicus] = useState(false);

  const fetchTimeseries = (id: number) => {
    apiFetch(`/env/${id}/timeseries`)
      .then(data => setEnvData(data))
      .catch(err => console.error("Failed to load timeseries", err));
  };

  useEffect(() => {
    apiFetch('/assets').then(data => {
      setOuvrages(data);
      if (data.length > 0) {
        setOuvrageId(data[0].id);
        fetchTimeseries(data[0].id);
      }
    }).catch(err => console.error("Failed to load ouvrages", err));
  }, []);

  useEffect(() => {
    if (ouvrageId) fetchTimeseries(ouvrageId);
  }, [ouvrageId]);

  const handleNasaSync = async () => {
    try {
      setSyncingNasa(true);
      const res = await apiFetch('/env/sync', { method: 'POST' });
      alert(res.message);
      fetchTimeseries(ouvrageId);
    } catch (err) {
      alert("Erreur de synchronisation NASA : " + (err as Error).message);
    } finally {
      setSyncingNasa(false);
    }
  };

  const handleCopernicusSync = async () => {
    try {
      setSyncingCopernicus(true);
      const res = await apiFetch('/env/sync-copernicus', { method: 'POST' });
      alert(res.message);
      fetchTimeseries(ouvrageId);
    } catch (err) {
      alert("Erreur de synchronisation Copernicus : " + (err as Error).message);
    } finally {
      setSyncingCopernicus(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 className="page-title">Environnement</h1>
          <p className="page-subtitle">Suivi des variables climatiques et de l'agressivité de l'environnement (IAE)</p>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button 
            className="btn btn-primary" 
            onClick={handleNasaSync} 
            disabled={syncingNasa}
          >
            <RefreshCw className={syncingNasa ? "animate-spin" : ""} />
            {syncingNasa ? 'Synchronisation...' : 'Synchroniser NASA'}
          </button>
          <button 
            className="btn btn-secondary" 
            onClick={handleCopernicusSync} 
            disabled={syncingCopernicus}
            style={{ background: '#1e40af', color: 'white', borderColor: '#1e40af' }}
          >
            <RefreshCw className={syncingCopernicus ? "animate-spin" : ""} />
            {syncingCopernicus ? 'Synchronisation...' : 'Synchroniser Copernicus'}
          </button>
        </div>
      </div>

      <ScientificDisclaimer />

      <div className="grid-2" style={{ marginTop: '1.5rem', alignItems: 'start' }}>
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2 className="card-title" style={{ marginBottom: 0 }}>Séries Temporelles</h2>
            <div style={{ display: 'flex', gap: '0.25rem' }}>
              <span className="badge" style={{ background: 'rgba(34, 197, 94, 0.1)', color: '#22c55e', border: '1px solid rgba(34, 197, 94, 0.2)' }}>NASA CMR</span>
              <span className="badge" style={{ background: 'rgba(59, 130, 246, 0.1)', color: '#3b82f6', border: '1px solid rgba(59, 130, 246, 0.2)' }}>CDSE</span>
            </div>
          </div>

          <div style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <label style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', fontWeight: 500, textTransform: 'uppercase' }}>Ouvrage:</label>
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

          <IAELineChart data={envData} />
        </div>

        <div className="card">
          <h2 className="card-title" style={{ marginBottom: '1rem' }}>Agressivité de l'Environnement (IAE)</h2>
          
          {(() => {
            const latest = envData.length > 0 ? envData[envData.length - 1] : null;
            if (!latest) return <div style={{ padding: '2rem' }}>Aucune donnée disponible.</div>;

            const t = latest.temperature?.toFixed(1) || '--';
            const h = latest.humidite?.toFixed(1) || '--';
            const p = latest.pluie?.toFixed(1) || '--';
            const so2 = latest.pollution_so2?.toFixed(2) || '--';
            const iaeScore = latest.iae?.toFixed(2) || '--';

            return (
              <>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Paramètre</th>
                      <th>Valeur Actuelle</th>
                      <th>Source</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Température (T)</td>
                      <td className="numeric">{t} °C</td>
                      <td><span className="badge badge-info">{latest.source || 'NASA'}</span></td>
                    </tr>
                    <tr>
                      <td>Humidité (H)</td>
                      <td className="numeric">{h} %</td>
                      <td><span className="badge badge-info">{latest.source || 'NASA'}</span></td>
                    </tr>
                    <tr>
                      <td>Pluviométrie (R)</td>
                      <td className="numeric">{p} mm/jour</td>
                      <td><span className="badge badge-info">{latest.source || 'NASA'}</span></td>
                    </tr>
                    <tr>
                      <td>Pollution (SO2)</td>
                      <td className="numeric">{so2} DU</td>
                      <td><span className="badge badge-info">{latest.source || 'NASA'}</span></td>
                    </tr>
                  </tbody>
                </table>

                <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'var(--bg-primary)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-secondary)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', textTransform: 'uppercase', fontWeight: 600 }}>IAE Global - Ouvrage {ouvrageId}</div>
                    <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)', marginTop: '0.25rem' }}>{latest.date ? new Date(latest.date).toLocaleDateString() : 'En direct'}</div>
                  </div>
                  <div style={{ fontSize: 'var(--text-3xl)', fontWeight: 700, color: 'var(--status-critical)', fontFamily: 'var(--font-mono)' }}>
                    {iaeScore}
                  </div>
                </div>
              </>
            );
          })()}
        </div>
      </div>
    </div>
  );
}
