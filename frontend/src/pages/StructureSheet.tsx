import React from 'react';
import { useParams } from 'react-router-dom';

export default function StructureSheet() {
  const { id } = useParams();

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Fiche de Structure</h1>
        <p className="page-subtitle">Détails de l'ouvrage {id}</p>
      </div>
      <div className="card">
        <h2 className="card-title">Informations Générales</h2>
        <p>Données de structure à venir...</p>
      </div>
    </div>
  );
}
