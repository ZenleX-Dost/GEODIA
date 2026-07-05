import React, { useState, useEffect, useRef } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { ProbaBarChart } from '../components/charts/ProbaBarChart';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';
import { apiFetch } from '../api/client';

export default function ProbabilisticModel() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  
  const [geoData, setGeoData] = useState<any>(null);
  const [selectedCell, setSelectedCell] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Fetch Area Grid Data
  useEffect(() => {
    apiFetch('/area/grid?grid_size=80')
      .then((data: any) => {
        setGeoData(data);
        // Default select the middle cell if available
        if (data && data.features && data.features.length > 0) {
            const centerIdx = Math.floor(data.features.length / 2);
            setSelectedCell(data.features[centerIdx].properties);
        }
      })
      .catch(err => console.error("Failed to load area grid", err))
      .finally(() => setLoading(false));
  }, []);

  // Initialize MapLibre Map
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
      center: [-8.605, 33.120],
      zoom: 12.5,
      pitch: 45,
      bearing: -17.6,
    });

    map.addControl(new maplibregl.NavigationControl(), 'bottom-right');

    map.on('load', () => {
      map.addSource('grid-data', {
        type: 'geojson',
        data: geoData
      });

      // Add grid polygons
      map.addLayer({
        id: 'grid-fill',
        type: 'fill',
        source: 'grid-data',
        paint: {
          'fill-color': [
            'interpolate',
            ['linear'],
            ['get', 'max_risk'],
            0, '#10b981',   // Emerald
            25, '#f59e0b',  // Amber
            50, '#f97316',  // Orange
            75, '#ef4444'   // Red
          ],
          'fill-opacity': 0.6,
          'fill-outline-color': 'rgba(255,255,255,0.1)'
        }
      });

      // Hover and Click events
      map.on('click', 'grid-fill', (e) => {
        if (e.features && e.features.length > 0) {
            const props = e.features[0].properties;
            // Parse probas since MapLibre stringifies arrays/objects in properties
            if (typeof props.probas === 'string') {
                props.probas = JSON.parse(props.probas);
            }
            setSelectedCell(props);
        }
      });

      map.on('mouseenter', 'grid-fill', () => {
        map.getCanvas().style.cursor = 'pointer';
      });
      map.on('mouseleave', 'grid-fill', () => {
        map.getCanvas().style.cursor = '';
      });

      mapRef.current = map;
    });

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, [loading, geoData]);

  // Derived state for Explainability and Chart
  const probaData = selectedCell?.probas || [];
  const exp: string[] = [];
  
  if (selectedCell && probaData.length > 0) {
      const PATHOLOGY_NAMES: Record<string, string> = {
        P2: "Corrosion par chlorures",
        P6: "Affouillement",
        P12: "Tassement / Soulèvement"
      };

      const sortedData = [...probaData].sort((a: any, b: any) => b.p_current - a.p_current);
      
      sortedData.forEach((item: any) => {
          if (item.p_current > 50) {
              let reason = "";
              if (item.iad && item.iad > 0.5) {
                  reason += `fortes anomalies InSAR (IAD: ${item.iad.toFixed(2)})`;
              }
              if (item.iae && item.iae > 0.5) {
                  if (reason) reason += " et ";
                  reason += `environnement agressif (IAE: ${item.iae.toFixed(2)})`;
              }
              if (!reason) reason = "la dégradation naturelle globale";
              
              exp.push(`🔴 ${item.pathologie} (${PATHOLOGY_NAMES[item.pathologie]}) : ${item.p_current.toFixed(1)}% piloté par ${reason}.`);
          } else if (item.p_current > 25) {
              exp.push(`🟠 ${item.pathologie} (${PATHOLOGY_NAMES[item.pathologie]}) : Risque modéré à ${item.p_current.toFixed(1)}%.`);
          }
      });

      if (exp.length === 0) exp.push("🟢 Secteur globalement stable. Aucune anomalie majeure de déformation ou environnementale détectée.");
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">Modèle Probabiliste (Area Analysis)</h1>
        <p className="page-subtitle">Évaluation probabiliste continue de la plateforme Jorf Lasfar</p>
      </div>

      <ScientificDisclaimer />

      {loading ? (
        <div className="spinner" style={{ margin: '4rem auto' }} />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', marginTop: '2rem' }}>
          
          {/* MAP GRID VISUALIZATION */}
          <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
            <div style={{ padding: '1.5rem', borderBottom: '1px solid var(--border-secondary)', background: 'var(--bg-surface)' }}>
              <h2 className="card-title" style={{ margin: 0 }}>Grille de Risque Géospatiale</h2>
              <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
                Cliquez sur n'importe quel bloc 50x50m pour afficher les détails du modèle.
              </p>
            </div>
            <div ref={mapContainer} style={{ height: '500px', width: '100%' }} />
          </div>

          {/* INDIVIDUAL CELL ANALYSIS SECTION */}
          {selectedCell && (
            <div style={{ display: 'flex', gap: '2rem' }}>
              <div className="card" style={{ flex: 1 }}>
                <h2 className="card-title">Profil du Bloc Sélectionné</h2>
                <div style={{ marginBottom: '1.5rem', fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>
                  Coordonnées : {selectedCell.lat.toFixed(5)}°N, {selectedCell.lon.toFixed(5)}°W
                </div>
                
                <h3 style={{ fontSize: 'var(--text-sm)', color: 'var(--text-primary)', marginBottom: '1rem' }}>Probabilités actuelles (%)</h3>
                <ProbaBarChart data={probaData.map((p: any) => ({ pathologie: p.pathologie, probability: p.p_current }))} />
              </div>

              <div className="card" style={{ flex: 1 }}>
                <h2 className="card-title">Explainabilité du Modèle Local</h2>
                <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', marginBottom: '1rem' }}>
                  Variables de terrain satellitaires (InSAR) et environnementales (NASA).
                </p>
                
                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: 'var(--text-sm)' }}>
                  {exp.map((txt, idx) => (
                    <li key={idx} style={{ background: 'var(--bg-surface)', padding: '0.75rem', borderRadius: '4px', borderLeft: `3px solid ${idx === 0 ? '#ef4444' : '#f97316'}` }}>
                      {txt}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

        </div>
      )}
    </div>
  );
}
