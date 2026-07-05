import React, { useState } from 'react';
import { UploadCloud, File, CheckCircle2, AlertCircle } from 'lucide-react';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';

export default function DataImport() {
  const [file, setFile] = useState<File | null>(null);
  const [importType, setImportType] = useState('insar');
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
      setStatus('idle');
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setStatus('uploading');
    setMessage('Upload en cours...');
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', importType);

    try {
      const response = await fetch('http://localhost:8000/api/imports/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) throw new Error('Erreur lors du transfert');
      
      const data = await response.json();
      setStatus('success');
      setMessage(data.message || 'Fichier intégré avec succès.');
    } catch (err: any) {
      setStatus('error');
      setMessage(err.message || "Impossible de charger le fichier.");
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Importation de Données</h1>
        <p className="page-subtitle">Injectez vos propres jeux de données (CSV/Excel) dans le modèle GEODIA.</p>
      </div>

      <ScientificDisclaimer />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: '2rem', marginTop: '2rem' }}>
        <div className="card">
          <h2 className="card-title">Centre d'Upload</h2>
          
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
              Type de Données
            </label>
            <select 
              value={importType} 
              onChange={(e) => setImportType(e.target.value)}
              style={{ width: '100%', padding: '0.75rem', background: 'var(--bg-primary)', border: '1px solid var(--border-secondary)', borderRadius: '4px', color: 'white' }}
            >
              <option value="insar">Déplacements Satellites (InSAR)</option>
              <option value="climat">Données Météo / Climat</option>
              <option value="ouvrages">Inventaire des Ouvrages</option>
              <option value="pathologies">Relevés Pathologiques</option>
            </select>
          </div>

          <div 
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
            style={{ 
              border: `2px dashed ${file ? 'var(--accent-teal)' : 'var(--border-secondary)'}`, 
              borderRadius: 'var(--radius-md)', 
              padding: '4rem 2rem', 
              textAlign: 'center',
              background: file ? 'rgba(56, 189, 248, 0.05)' : 'rgba(148, 163, 184, 0.05)',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
            onClick={() => document.getElementById('file-upload')?.click()}
          >
            <input type="file" id="file-upload" hidden onChange={(e) => {
              if (e.target.files && e.target.files.length > 0) {
                setFile(e.target.files[0]);
                setStatus('idle');
              }
            }} />
            
            {file ? (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
                <File size={48} color="var(--accent-teal)" />
                <div>
                  <p style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{file.name}</p>
                  <p style={{ color: 'var(--text-tertiary)', fontSize: 'var(--text-sm)' }}>{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                </div>
              </div>
            ) : (
              <>
                <UploadCloud size={48} color="var(--text-tertiary)" style={{ margin: '0 auto 1rem' }} />
                <p style={{ color: 'var(--text-secondary)', fontWeight: 500, marginBottom: '0.5rem', fontSize: '1.1rem' }}>
                  Glissez-déposez votre fichier ici
                </p>
                <p style={{ color: 'var(--text-tertiary)', fontSize: 'var(--text-sm)' }}>
                  CSV, XLSX (max 50MB)
                </p>
              </>
            )}
          </div>

          {status !== 'idle' && (
            <div style={{ 
              marginTop: '1.5rem', 
              padding: '1rem', 
              borderRadius: '4px',
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              background: status === 'success' ? 'rgba(34, 197, 94, 0.1)' : status === 'error' ? 'rgba(239, 68, 68, 0.1)' : 'rgba(148, 163, 184, 0.1)',
              border: `1px solid ${status === 'success' ? 'var(--status-success)' : status === 'error' ? 'var(--status-critical)' : 'var(--border-secondary)'}`
            }}>
              {status === 'success' ? <CheckCircle2 color="var(--status-success)" /> : status === 'error' ? <AlertCircle color="var(--status-critical)" /> : <div className="spinner" style={{ width: 20, height: 20 }} />}
              <span style={{ color: 'var(--text-primary)', fontSize: 'var(--text-sm)' }}>{message}</span>
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '2rem' }}>
            <button 
              className="btn btn-primary" 
              disabled={!file || status === 'uploading'}
              onClick={handleUpload}
            >
              Intégrer les données
            </button>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div className="card">
            <h3 className="card-title">Formats Supportés</h3>
            <ul style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '0.5rem', marginLeft: '1rem' }}>
              <li><strong>InSAR:</strong> CSV avec `lat`, `lon`, `velocity`, `ts_*`</li>
              <li><strong>Climat:</strong> Données journalières NASA POWER ou ERA5</li>
              <li><strong>Ouvrages:</strong> Export interne Jorf Lasfar (CSV/XLSX)</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
