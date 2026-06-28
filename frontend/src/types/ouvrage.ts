/**
 * TypeScript types for Ouvrage (structure/asset).
 */

export interface Ouvrage {
  id: number;
  code: string;
  nom: string;
  famille: string;
  lat: number;
  lon: number;
  classe: 'A' | 'B' | 'C' | 'D';
  icf: number | null;
  ivp: number | null;
  ipd: number | null;
  ied: number | null;
  exposition: string | null;
  created_at: string;
}

export interface OuvrageGeoJSON {
  type: 'FeatureCollection';
  features: OuvrageFeature[];
}

export interface OuvrageFeature {
  type: 'Feature';
  geometry: {
    type: 'Point';
    coordinates: [number, number]; // [lon, lat]
  };
  properties: {
    id: number;
    code: string;
    nom: string;
    famille: string;
    classe: 'A' | 'B' | 'C' | 'D';
    ipd: number | null;
    ied: number | null;
    exposition: string | null;
  };
}

export interface KPISummary {
  total_ouvrages: number;
  classe_a_count: number;
  alertes_insar: number;
  inspections_pending: number;
  indice_prevention: number;
  economie_potentielle: number;
}

export interface Alert {
  id: number;
  ouvrage_code: string;
  ouvrage_nom: string;
  severity: 'emergency' | 'critical' | 'high' | 'warning' | 'info';
  action: string;
  source: string;
  date: string;
}

export const CLASSE_COLORS: Record<string, string> = {
  A: '#ef4444',
  B: '#f97316',
  C: '#eab308',
  D: '#22c55e',
};

export const FAMILLE_OPTIONS = [
  'hydraulique',
  'réservoir',
  'bâtiment',
  'fosse',
  'canal',
  'station',
] as const;
