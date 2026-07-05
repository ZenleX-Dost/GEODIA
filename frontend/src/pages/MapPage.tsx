/**
 * MapPage — Interactive map with MapLibre GL JS, structure markers, and popups.
 */
import { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import Header from '../components/layout/Header';
import { getAssetsGeoJSON } from '../api/assets';
import { apiFetch } from '../api/client';
import type { OuvrageGeoJSON } from '../types/ouvrage';
import { CLASSE_COLORS } from '../types/ouvrage';

const CLASSE_FILTERS = ['Tous', 'A', 'B', 'C', 'D'] as const;

// Jorf Lasfar center coordinates
const CENTER: [number, number] = [-8.6235, 33.103]; // Updated center to Jorf Lasfar coast

export default function MapPage() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const markersRef = useRef<maplibregl.Marker[]>([]);
  const [geoData, setGeoData] = useState<OuvrageGeoJSON | null>(null);
  const [classeFilter, setClasseFilter] = useState<string>('Tous');
  const [loading, setLoading] = useState(true);
  const [mapReady, setMapReady] = useState(false);
  const [showHeatmap, setShowHeatmap] = useState(false);

  // Load data
  useEffect(() => {
    Promise.all([
      getAssetsGeoJSON(),
      apiFetch('/compute/proba/matrix')
    ])
      .then(([geo, matrix]) => {
        // Compute max risk per ouvrage
        geo.features.forEach((f: any) => {
          const m = matrix.find((x: any) => x.ouvrage_id === f.properties.id);
          let maxR = 0;
          if (m && m.probabilities) {
            maxR = Math.max(...Object.values(m.probabilities) as number[]);
          }
          f.properties.max_risk = maxR;
        });
        setGeoData(geo);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  // Initialize map
  useEffect(() => {
    if (loading || !mapContainer.current || mapRef.current || !geoData) return;

    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          'esri-satellite': {
            type: 'raster',
            tiles: [
              'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
            ],
            tileSize: 256,
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
          },
        },
        layers: [
          {
            id: 'esri-satellite',
            type: 'raster',
            source: 'esri-satellite',
            minzoom: 0,
            maxzoom: 19,
          },
        ],
      },
      center: CENTER,
      zoom: 15,
      minZoom: 10,
      maxZoom: 18,
    });

    map.addControl(new maplibregl.NavigationControl(), 'bottom-right');
    map.addControl(new maplibregl.ScaleControl(), 'bottom-left');

    map.on('load', () => {
      // Add GeoJSON source for heatmap
      map.addSource('risk-data', {
        type: 'geojson',
        data: geoData
      });

      // Add Heatmap layer
      map.addLayer({
        id: 'risk-heat',
        type: 'heatmap',
        source: 'risk-data',
        maxzoom: 18,
        paint: {
          // Weight points by max_risk (0 to 100)
          'heatmap-weight': ['interpolate', ['linear'], ['get', 'max_risk'], 0, 0, 100, 1],
          // Increase intensity as zoom increases
          'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 14, 1, 18, 3],
          // Color ramp
          'heatmap-color': [
            'interpolate',
            ['linear'],
            ['heatmap-density'],
            0, 'rgba(16, 185, 129, 0)',   // Emerald transparent
            0.2, 'rgb(16, 185, 129)',     // Emerald
            0.5, 'rgb(245, 158, 11)',     // Amber
            0.8, 'rgb(249, 115, 22)',     // Orange
            1, 'rgb(239, 68, 68)'         // Red
          ],
          // Radius scales with zoom
          'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 14, 20, 18, 80],
          'heatmap-opacity': 0.0 // Hidden by default
        }
      });

      mapRef.current = map;
      setMapReady(true);
    });

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, [loading, geoData]);

  // Handle Heatmap Toggle
  useEffect(() => {
    const map = mapRef.current;
    if (!mapReady || !map) return;
    
    if (showHeatmap) {
      map.setPaintProperty('risk-heat', 'heatmap-opacity', 0.8);
      // Hide markers
      markersRef.current.forEach((m) => {
        const el = m.getElement();
        el.style.opacity = '0';
        el.style.pointerEvents = 'none';
      });
    } else {
      map.setPaintProperty('risk-heat', 'heatmap-opacity', 0.0);
      // Show markers
      markersRef.current.forEach((m) => {
        const el = m.getElement();
        el.style.opacity = '1';
        el.style.pointerEvents = 'auto';
      });
    }
  }, [showHeatmap, mapReady]);

  // Add/update markers when data or filter changes
  useEffect(() => {
    const map = mapRef.current;
    if (!mapReady || !map || !geoData) return;

    // Clear existing markers
    markersRef.current.forEach((m) => m.remove());
    markersRef.current = [];

    const features =
      classeFilter === 'Tous'
        ? geoData.features
        : geoData.features.filter((f) => f.properties.classe === classeFilter);

    // Also update heatmap source if filter changed
    const source = map.getSource('risk-data') as maplibregl.GeoJSONSource;
    if (source) {
      source.setData({
        type: 'FeatureCollection',
        features: features
      });
    }

    features.forEach((feature) => {
      const { coordinates } = feature.geometry;
      const { code, nom, classe, ipd, exposition, max_risk } = feature.properties;
      const color = CLASSE_COLORS[classe] || '#94a3b8';

      // Create custom marker element
      const el = document.createElement('div');
      el.style.width = '24px';
      el.style.height = '24px';
      el.style.borderRadius = '50%';
      el.style.background = color;
      el.style.border = '2px solid rgba(255,255,255,0.9)';
      el.style.boxShadow = `0 2px 6px ${color}80`;
      el.style.cursor = 'pointer';
      el.style.transition = 'transform 0.2s ease, opacity 0.3s ease';
      el.style.opacity = showHeatmap ? '0' : '1';
      el.style.pointerEvents = showHeatmap ? 'none' : 'auto';
      
      el.addEventListener('mouseenter', () => {
        el.style.transform = 'scale(1.3)';
      });
      el.addEventListener('mouseleave', () => {
        el.style.transform = 'scale(1)';
      });

      const popup = new maplibregl.Popup({
        offset: 15,
        closeButton: true,
        maxWidth: '320px',
      }).setHTML(`
        <div style="font-family: Inter, sans-serif; padding: 4px;">
          <div style="font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
            ${code} · Classe ${classe}
          </div>
          <div style="font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 8px;">
            ${nom}
          </div>
          <div style="display: flex; gap: 16px; font-size: 12px; color: #475569; margin-bottom: 4px;">
            <div><strong>IPD:</strong> ${ipd?.toFixed(1) ?? '—'}%</div>
            <div><strong>Exposition:</strong> ${exposition ?? '—'}</div>
          </div>
          <div style="font-size: 12px; color: #ef4444; font-weight: bold;">
            Risque Max (Proba): ${max_risk?.toFixed(1)}%
          </div>
        </div>
      `);

      const marker = new maplibregl.Marker({ element: el })
        .setLngLat(coordinates as [number, number])
        .setPopup(popup)
        .addTo(map);

      markersRef.current.push(marker);
    });
  }, [geoData, classeFilter, mapReady]); // NOTE: Intentionally not depending on showHeatmap to avoid re-creating markers, just using their refs to hide them in the other effect

  return (
    <>
      <Header title="Carte SIG" />
      <main className="app-main">
        <div className="page-container">
          <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h1 className="page-title">Carte SIG</h1>
              <p className="page-subtitle">
                Localisation géographique et Cartographie des risques (Heatmap)
              </p>
            </div>
            <button 
              onClick={() => setShowHeatmap(!showHeatmap)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '0.5rem 1rem',
                background: showHeatmap ? 'var(--primary-light)' : 'var(--bg-surface)',
                color: showHeatmap ? 'white' : 'var(--text-primary)',
                border: `1px solid ${showHeatmap ? 'var(--primary)' : 'var(--border-secondary)'}`,
                borderRadius: '8px',
                cursor: 'pointer',
                fontWeight: '600',
                transition: 'all 0.2s ease',
                boxShadow: showHeatmap ? '0 0 15px rgba(239, 68, 68, 0.4)' : 'none'
              }}
            >
              <div style={{ width: 12, height: 12, borderRadius: '50%', background: showHeatmap ? '#ef4444' : '#94a3b8' }}></div>
              {showHeatmap ? 'Heatmap Active' : 'Activer Heatmap'}
            </button>
          </div>

          {/* Filter chips */}
          <div className="toolbar" style={{ marginBottom: 'var(--space-4)', display: 'flex', justifyContent: 'space-between' }}>
            <div className="filter-chips">
              {CLASSE_FILTERS.map((c) => (
                <button
                  key={c}
                  className={`chip ${classeFilter === c ? 'active' : ''}`}
                  onClick={() => setClasseFilter(c)}
                  disabled={showHeatmap}
                  style={{ opacity: showHeatmap ? 0.5 : 1 }}
                >
                  {c === 'Tous' ? 'Tous les ouvrages' : `Classe ${c}`}
                </button>
              ))}
            </div>
            {!showHeatmap ? (
              <div style={{ display: 'flex', gap: 'var(--space-3)', alignItems: 'center' }}>
                {Object.entries(CLASSE_COLORS).map(([cls, color]) => (
                  <div key={cls} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
                    <div style={{ width: 10, height: 10, borderRadius: '50%', background: color }} />
                    Classe {cls}
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ display: 'flex', gap: 'var(--space-3)', alignItems: 'center' }}>
                <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', fontWeight: 'bold' }}>Risque (Max Proba):</div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#10b981' }} /> Faible
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#f59e0b' }} /> Modéré
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#f97316' }} /> Élevé
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#ef4444' }} /> Très Élevé
                </div>
              </div>
            )}
          </div>

          {/* Map */}
          {loading ? (
            <div className="loading-spinner" style={{ height: 600 }}>
              <div className="spinner" />
            </div>
          ) : (
            <div className="map-container" ref={mapContainer} style={{ height: 600, borderRadius: '12px', overflow: 'hidden', border: '1px solid var(--border-primary)', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }} />
          )}
        </div>
      </main>
    </>
  );
}
