import { UploadCloud, CheckCircle2 } from 'lucide-react';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';

export default function Inspection() {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Saisie d'Inspection Terrain</h1>
        <p className="page-subtitle">Enregistrement des observations visuelles et relevés pathologiques</p>
      </div>

      <ScientificDisclaimer />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: '2rem', marginTop: '2rem' }}>
        {/* Main Form */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <h2 className="card-title">Nouveau Rapport d'Inspection</h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
            <div>
              <label style={labelStyle}>Ouvrage Inspecté</label>
              <select style={inputStyle}>
                <option value="">Sélectionner un ouvrage...</option>
                <option value="R-102">R-102 (Déversoir Eau de Mer)</option>
                <option value="R-108">R-108 (Bassin REM1)</option>
                <option value="R-110">R-110 (Pylône d'éclairage)</option>
              </select>
            </div>
            <div>
              <label style={labelStyle}>Date d'inspection</label>
              <input type="date" style={inputStyle} />
            </div>
          </div>

          <div>
            <label style={labelStyle}>Pathologies Observées (Sélection multiple)</label>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.75rem', marginTop: '0.5rem' }}>
              {['P1 (Écaillage)', 'P2 (Fissuration)', 'P3 (Corrosion)', 'P6 (Affaissement)', 'P12 (Carbonatation)'].map(p => (
                <label key={p} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'var(--bg-primary)', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border-secondary)', cursor: 'pointer' }}>
                  <input type="checkbox" style={{ accentColor: 'var(--accent-teal)', width: '16px', height: '16px' }} />
                  <span style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>{p}</span>
                </label>
              ))}
            </div>
          </div>

          <div>
            <label style={labelStyle}>Description détaillée des observations</label>
            <textarea 
              rows={4} 
              style={{ ...inputStyle, resize: 'vertical' }} 
              placeholder="Ex: Fissure de 2mm d'ouverture sur le voile Nord..."
            />
          </div>

          <div>
            <label style={labelStyle}>Preuves Photographiques</label>
            <div style={{ 
              border: '2px dashed var(--border-secondary)', 
              borderRadius: 'var(--radius-md)', 
              padding: '3rem', 
              textAlign: 'center',
              background: 'rgba(148, 163, 184, 0.05)',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}>
              <UploadCloud size={40} color="var(--text-tertiary)" style={{ margin: '0 auto 1rem' }} />
              <p style={{ color: 'var(--text-secondary)', fontWeight: 500, marginBottom: '0.25rem' }}>Glissez-déposez vos photos ici</p>
              <p style={{ color: 'var(--text-tertiary)', fontSize: 'var(--text-sm)' }}>JPG, PNG ou PDF (max 10MB)</p>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '1rem' }}>
            <button className="btn btn-secondary">Annuler</button>
            <button className="btn btn-primary" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <CheckCircle2 size={18} /> Enregistrer l'inspection
            </button>
          </div>
        </div>

        {/* Sidebar Info */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="card">
            <h3 className="card-title">Instructions</h3>
            <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Assurez-vous de capturer au moins une photo globale et une photo détaillée pour chaque pathologie signalée.
            </p>
          </div>
          <div className="card">
            <h3 className="card-title">Dernières saisies</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
              <div style={{ borderLeft: '2px solid var(--accent-teal)', paddingLeft: '1rem' }}>
                <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-primary)', fontWeight: 500 }}>Ouvrage R-105</p>
                <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>Il y a 2 jours par Inspecteur A.</p>
              </div>
              <div style={{ borderLeft: '2px solid var(--status-warning)', paddingLeft: '1rem' }}>
                <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-primary)', fontWeight: 500 }}>Ouvrage R-099</p>
                <p style={{ fontSize: 'var(--text-xs)', color: 'var(--text-tertiary)' }}>Il y a 5 jours par Inspecteur B.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const labelStyle: React.CSSProperties = {
  display: 'block',
  fontSize: 'var(--text-sm)',
  fontWeight: 500,
  color: 'var(--text-secondary)',
  marginBottom: '0.5rem'
};

const inputStyle: React.CSSProperties = {
  width: '100%',
  padding: '0.75rem 1rem',
  background: 'var(--bg-primary)',
  border: '1px solid var(--border-secondary)',
  borderRadius: 'var(--radius-md)',
  color: 'var(--text-primary)',
  fontSize: 'var(--text-sm)',
  outline: 'none',
  transition: 'border-color 0.2s'
};
