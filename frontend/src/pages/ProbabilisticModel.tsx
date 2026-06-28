import React, { useState, useEffect } from 'react';
import { ProbaBarChart } from '../components/charts/ProbaBarChart';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';

export default function ProbabilisticModel() {
  const [ouvrageId, setOuvrageId] = useState<number>(1);

  // Mock data for display
  const mockProbaData = [
    { pathologie: 'P1', probability: 0.12 },
    { pathologie: 'P2', probability: 0.65 },
    { pathologie: 'P3', probability: 0.22 },
    { pathologie: 'P4', probability: 0.05 },
    { pathologie: 'P5', probability: 0.45 },
    { pathologie: 'P6', probability: 0.80 },
    { pathologie: 'P7', probability: 0.15 },
    { pathologie: 'P8', probability: 0.35 },
    { pathologie: 'P9', probability: 0.10 },
    { pathologie: 'P10', probability: 0.25 },
    { pathologie: 'P11', probability: 0.02 },
    { pathologie: 'P12', probability: 0.90 }
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Modèle Probabiliste</h1>
        <p className="page-subtitle">Évaluation probabiliste des pathologies (P1–P12)</p>
      </div>

      <ScientificDisclaimer />

      <div style={{ display: 'flex', gap: '2rem', marginTop: '2rem' }}>
        <div className="card" style={{ flex: 1 }}>
          <h2 className="card-title">Profil de l'Ouvrage {ouvrageId}</h2>
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>Sélectionner un ouvrage:</label>
            <select 
              value={ouvrageId} 
              onChange={(e) => setOuvrageId(Number(e.target.value))}
              style={{ display: 'block', width: '100%', padding: '0.5rem', background: 'var(--bg-surface)', color: 'white', border: '1px solid var(--border-secondary)', borderRadius: '4px', marginTop: '0.5rem' }}
            >
              {[1, 2, 3, 4, 5].map(id => (
                <option key={id} value={id}>Ouvrage {id}</option>
              ))}
            </select>
          </div>
          
          <h3 style={{ fontSize: 'var(--text-sm)', color: 'var(--text-primary)', marginBottom: '1rem' }}>Probabilités par pathologie</h3>
          <ProbaBarChart data={mockProbaData} />
        </div>

        <div className="card" style={{ flex: 1 }}>
          <h2 className="card-title">Explainabilité du Modèle</h2>
          <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            Facteurs contribuant au profil de risque actuel.
          </p>
          
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: 'var(--text-sm)' }}>
            <li style={{ background: 'var(--bg-surface)', padding: '0.75rem', borderRadius: '4px', borderLeft: '3px solid #ef4444' }}>
              <strong>P12 Très Élevé (90%)</strong> : Tiré par un Indice d'Altération Environnementale (IAE) critique et un historique (H) défavorable.
            </li>
            <li style={{ background: 'var(--bg-surface)', padding: '0.75rem', borderRadius: '4px', borderLeft: '3px solid #f97316' }}>
              <strong>P6 Élevé (80%)</strong> : Corrélation avec une anomalie InSAR (IAD) &gt; 0.60 dans la zone.
            </li>
            <li style={{ background: 'var(--bg-surface)', padding: '0.75rem', borderRadius: '4px', borderLeft: '3px solid #f97316' }}>
              <strong>P2 Élevé (65%)</strong> : Classe A de l'ouvrage combinée à un Indice de Vétusté Physique (IVP) dégradé.
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
