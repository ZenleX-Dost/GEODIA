/**
 * API functions for assets (ouvrages).
 */
import { apiFetch } from './client';
import type { Ouvrage, OuvrageGeoJSON, KPISummary, Alert } from '../types/ouvrage';

export async function getAssets(params?: {
  classe?: string;
  famille?: string;
  search?: string;
}): Promise<Ouvrage[]> {
  const searchParams = new URLSearchParams();
  if (params?.classe) searchParams.set('classe', params.classe);
  if (params?.famille) searchParams.set('famille', params.famille);
  if (params?.search) searchParams.set('search', params.search);
  const qs = searchParams.toString();
  return apiFetch<Ouvrage[]>(`/assets${qs ? `?${qs}` : ''}`);
}

export async function getAssetById(id: number): Promise<Ouvrage> {
  return apiFetch<Ouvrage>(`/assets/${id}`);
}

export async function getAssetsGeoJSON(classe?: string): Promise<OuvrageGeoJSON> {
  const qs = classe ? `?classe=${classe}` : '';
  return apiFetch<OuvrageGeoJSON>(`/assets/geojson${qs}`);
}

export async function getKPIs(): Promise<KPISummary> {
  return apiFetch<KPISummary>('/kpis');
}

export async function getAlerts(): Promise<Alert[]> {
  return apiFetch<Alert[]>('/alerts');
}
