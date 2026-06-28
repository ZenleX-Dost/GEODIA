/**
 * Placeholder page component for modules under construction (Sprints 2-6).
 */
import {
  ClipboardCheck,
  CloudSun,
  BarChart3,
  Radar,
  Wrench,
  FileOutput,
} from 'lucide-react';
import Header from '../components/layout/Header';

interface PlaceholderProps {
  title: string;
  headerTitle: string;
  description: string;
  sprint: string;
  icon: 'inspection' | 'environment' | 'proba' | 'insar' | 'maintenance' | 'exports';
}

const icons = {
  inspection: ClipboardCheck,
  environment: CloudSun,
  proba: BarChart3,
  insar: Radar,
  maintenance: Wrench,
  exports: FileOutput,
};

function PlaceholderPage({ title, headerTitle, description, sprint, icon }: PlaceholderProps) {
  const Icon = icons[icon];
  return (
    <>
      <Header title={headerTitle} />
      <main className="app-main">
        <div className="page-container">
          <div className="placeholder-page">
            <div className="placeholder-icon">
              <Icon size={36} />
            </div>
            <h2 className="placeholder-title">{title}</h2>
            <p className="placeholder-text">{description}</p>
            <span
              className="badge badge-simulated"
              style={{ marginTop: 'var(--space-4)' }}
            >
              {sprint}
            </span>
          </div>
        </div>
      </main>
    </>
  );
}

export function Inspection() {
  return (
    <PlaceholderPage
      title="Inspection Terrain"
      headerTitle="Inspection Terrain"
      description="Module d'entrée des inspections terrain avec photos, états E0–E3, et observations de pathologies. Disponible dans le Sprint 2."
      sprint="Sprint 2"
      icon="inspection"
    />
  );
}

export function Environment() {
  return (
    <PlaceholderPage
      title="Environnement"
      headerTitle="Environnement"
      description="Import et visualisation des données environnementales (température, humidité, pollution, NDWI) et calcul de l'indice IAE. Disponible dans le Sprint 4."
      sprint="Sprint 4"
      icon="environment"
    />
  );
}

export function ProbabilisticModel() {
  return (
    <PlaceholderPage
      title="Modèle Probabiliste P1–P12"
      headerTitle="Modèle Proba"
      description="Modèle logistique pour le calcul des probabilités P1–P12 par ouvrage, avec matrice 19×12 et moteur d'alertes. Disponible dans le Sprint 3."
      sprint="Sprint 3"
      icon="proba"
    />
  );
}

export function InSAR() {
  return (
    <PlaceholderPage
      title="Pipeline InSAR"
      headerTitle="InSAR"
      description="Import et analyse des données InSAR : descripteurs, seuils, DBSCAN, Isolation Forest, et consensus. Disponible dans le Sprint 5."
      sprint="Sprint 5"
      icon="insar"
    />
  );
}

export function Maintenance() {
  return (
    <PlaceholderPage
      title="Maintenance & Optimisation"
      headerTitle="Maintenance & Optimisation"
      description="Plan de maintenance 5 ans, optimisation budgétaire PuLP (scénarios S1/S2/S3), et arbitrage des actions. Disponible dans le Sprint 6."
      sprint="Sprint 6"
      icon="maintenance"
    />
  );
}

export function Exports() {
  return (
    <PlaceholderPage
      title="Exports & Rapports"
      headerTitle="Exports"
      description="Centre d'export : fiches ouvrages PDF/Excel, rapports d'inspection, cartes risque, plans maintenance, et dossiers de consultation. Disponible dans le Sprint 6."
      sprint="Sprint 6"
      icon="exports"
    />
  );
}
