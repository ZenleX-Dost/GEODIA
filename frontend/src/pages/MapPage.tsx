/**
 * MapPage — Interactive map with MapLibre GL JS, structure markers, and popups.
 */
import { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import Header from '../components/layout/Header';
import { getAssetsGeoJSON } from '../api/assets';
import type { OuvrageGeoJSON } from '../types/ouvrage';
import { CLASSE_COLORS } from '../types/ouvrage';

const CLASSE_FILTERS = ['Tous', 'A', 'B', 'C', 'D'] as const;

// Jorf Lasfar center coordinates
const CENTER: [number, number] = [-6.852, 33.103];

export default function MapPage() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const markersRef = useRef<maplibregl.Marker[]>([]);
  const [geoData, setGeoData] = useState<OuvrageGeoJSON | null>(null);
  const [classeFilter, setClasseFilter] = useState<string>('Tous');
  const [loading, setLoading] = useState(true);

  // Load data
  useEffect(() => {
    getAssetsGeoJSON()
      .then(setGeoData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  // Initialize map
  useEffect(() => {
    if (!mapContainer.current || mapRef.current) return;

    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          'osm-tiles': {
            type: 'raster',
            tiles: [
              'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
            ],
            tileSize: 256,
            attribution: '© OpenStreetMap contributors',
          },
        },
        layers: [
          {
            id: 'osm-tiles',
            type: 'raster',
            source: 'osm-tiles',
            minzoom: 0,
            maxzoom: 19,
          },
        ],
      },
      center: CENTER,
      zoom: 14,
      minZoom: 10,
      maxZoom: 18,
    });

    map.addControl(new maplibregl.NavigationControl(), 'bottom-right');
    map.addControl(new maplibregl.ScaleControl(), 'bottom-left');

    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  // Add/update markers when data or filter changes
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !geoData) return;

    // Clear existing markers
    markersRef.current.forEach((m) => m.remove());
    markersRef.current = [];

    const features =
      classeFilter === 'Tous'
        ? geoData.features
        : geoData.features.filter((f) => f.properties.classe === classeFilter);

    features.forEach((feature) => {
      const { coordinates } = feature.geometry;
      const { code, nom, classe, ipd, exposition } = feature.properties;
      const color = CLASSE_COLORS[classe] || '#94a3b8';

      // Create custom marker element
      const el = document.createElement('div');
      el.style.width = '28px';
      el.style.height = '28px';
      el.style.borderRadius = '50%';
      el.style.background = color;
      el.style.border = '3px solid rgba(255,255,255,0.9)';
      el.style.boxShadow = `0 2px 8px ${color}80, 0 0 16px ${color}40`;
      el.style.cursor = 'pointer';
      el.style.transition = 'transform 0.2s ease';
      el.addEventListener('mouseenter', () => {
        el.style.transform = 'scale(1.3)';
      });
      el.addEventListener('mouseleave', () => {
        el.style.transform = 'scale(1)';
      });

      const popup = new maplibregl.Popup({
        offset: 20,
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
          <div style="display: flex; gap: 16px; font-size: 12px; color: #475569;">
            <div><strong>IPD:</strong> ${ipd?.toFixed(1) ?? '—'}%</div>
            <div><strong>Exposition:</strong> ${exposition ?? '—'}</div>
          </div>
        </div>
      `);

      const marker = new maplibregl.Marker({ element: el })
        .setLngLat(coordinates as [number, number])
        .setPopup(popup)
        .addTo(map);

      markersRef.current.push(marker);
    });
  }, [geoData, classeFilter]);

  return (
    <>
      <Header title="Carte SIG" />
      <main className="app-main">
        <div className="page-container">
          <div className="page-header">
            <h1 className="page-title">Carte SIG</h1>
            <p className="page-subtitle">
              Localisation géographique des 19 ouvrages — Jorf Lasfar
            </p>
          </div>

          {/* Filter chips */}
          <div className="toolbar" style={{ marginBottom: 'var(--space-4)' }}>
            <div className="filter-chips">
              {CLASSE_FILTERS.map((c) => (
                <button
                  key={c}
                  className={`chip ${classeFilter === c ? 'active' : ''}`}
                  onClick={() => setClasseFilter(c)}
                >
                  {c === 'Tous' ? 'Tous les ouvrages' : `Classe ${c}`}
                </button>
              ))}
            </div>
            <div style={{ display: 'flex', gap: 'var(--space-3)', alignItems: 'center' }}>
              {Object.entries(CLASSE_COLORS).map(([cls, color]) => (
                <div key={cls} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
                  <div style={{ width: 10, height: 10, borderRadius: '50%', background: color }} />
                  Classe {cls}
                </div>
              ))}
            </div>
          </div>

          {/* Map */}
          {loading ? (
            <div className="loading-spinner" style={{ height: 500 }}>
              <div className="spinner" />
            </div>
          ) : (
            <div className="map-container" ref={mapContainer} />
          )}
        </div>
      </main>
    </>
  );
}
