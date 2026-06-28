/**
 * Cockpit page — main dashboard with KPI cards, alerts feed, and quick actions.
 */
import { useEffect, useState } from 'react';
import {
  Building2,
  AlertTriangle,
  Radar,
  ClipboardList,
  Shield,
  TrendingDown,
  FileText,
  PlusCircle,
  CalendarClock,
  BellPlus,
  Send,
} from 'lucide-react';
import KPICard from '../components/ui/KPICard';
import ScientificDisclaimer from '../components/ui/ScientificDisclaimer';
import Header from '../components/layout/Header';
import { getKPIs, getAlerts } from '../api/assets';
import type { KPISummary, Alert } from '../types/ouvrage';

export default function Cockpit() {
  const [kpis, setKpis] = useState<KPISummary | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getKPIs(), getAlerts()])
      .then(([kpiData, alertData]) => {
        setKpis(kpiData);
        setAlerts(alertData);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <>
        <Header title="Cockpit" />
        <main className="app-main">
          <div className="loading-spinner">
            <div className="spinner" />
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <Header title="Cockpit" />
      <main className="app-main">
        <div className="page-container">
          <div className="page-header">
            <h1 className="page-title">Tableau de Bord</h1>
            <p className="page-subtitle">
              Vue d'ensemble du portefeuille de 19 ouvrages — OCP Jorf Lasfar
            </p>
          </div>

          <ScientificDisclaimer />

          {/* KPI Cards */}
          <div className="kpi-grid">
            <KPICard
              icon={<Building2 size={22} />}
              iconColor="teal"
              value={kpis?.total_ouvrages ?? '—'}
              label="Nombre d'ouvrages"
            />
            <KPICard
              icon={<AlertTriangle size={22} />}
              iconColor="red"
              value={kpis?.classe_a_count ?? '—'}
              label="Criticité élevée (Classe A)"
              trend={{ direction: 'up', value: '6 structures' }}
            />
            <KPICard
              icon={<Radar size={22} />}
              iconColor="orange"
              value={kpis?.alertes_insar ?? 0}
              label="Alertes InSAR"
            />
            <KPICard
              icon={<ClipboardList size={22} />}
              iconColor="yellow"
              value={kpis?.inspections_pending ?? '—'}
              label="Inspections en attente"
            />
            <KPICard
              icon={<Shield size={22} />}
              iconColor="blue"
              value={`${kpis?.indice_prevention?.toFixed(0) ?? '—'}`}
              label="Indice de prévention (/100)"
              trend={{ direction: 'up', value: '+5.2%' }}
            />
            <KPICard
              icon={<TrendingDown size={22} />}
              iconColor="green"
              value={
                kpis?.economie_potentielle
                  ? `${(kpis.economie_potentielle / 1_000_000).toFixed(1)}M`
                  : '—'
              }
              label="Économie potentielle (DH)"
              trend={{ direction: 'up', value: '30%' }}
            />
          </div>

          {/* Quick Actions */}
          <section className="section">
            <h3 className="section-title">
              <Send size={20} /> Actions Rapides
            </h3>
            <div className="quick-actions">
              <button className="btn btn-primary">
                <FileText size={16} /> Export PDF unique
              </button>
              <button className="btn btn-secondary">
                <PlusCircle size={16} /> Nouveau rapport
              </button>
              <button className="btn btn-secondary">
                <CalendarClock size={16} /> Plan d'inspection
              </button>
              <button className="btn btn-secondary">
                <BellPlus size={16} /> Ajouter alerte
              </button>
              <button className="btn btn-secondary">
                <Send size={16} /> Demande d'intervention
              </button>
            </div>
          </section>

          {/* Alerts Feed */}
          <section className="section">
            <h3 className="section-title">
              <AlertTriangle size={20} /> Alertes Récentes
            </h3>
            <div className="alerts-feed">
              {alerts.map((alert) => (
                <div className="alert-card" key={alert.id}>
                  <div className={`alert-dot ${alert.severity}`} />
                  <div className="alert-content">
                    <div className="alert-title">
                      {alert.ouvrage_code} — {alert.ouvrage_nom}
                    </div>
                    <div className="alert-description">{alert.action}</div>
                    <div className="alert-meta">
                      {alert.source} · {alert.date}
                    </div>
                  </div>
                  <span className={`badge badge-${alert.severity}`}>
                    {alert.severity}
                  </span>
                </div>
              ))}
            </div>
          </section>
        </div>
      </main>
    </>
  );
}
