/**
 * Sidebar navigation component — French labels, Lucide icons.
 */
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Building2,
  Map,
  ClipboardCheck,
  CloudSun,
  BarChart3,
  Radar,
  Wrench,
  FileOutput,
} from 'lucide-react';

const navItems = [
  { path: '/', label: 'Cockpit', icon: LayoutDashboard },
  { path: '/portfolio', label: 'Portefeuille GC', icon: Building2 },
  { path: '/carte', label: 'Carte SIG', icon: Map },
  { path: '/inspection', label: 'Inspection Terrain', icon: ClipboardCheck },
  { path: '/environnement', label: 'Environnement', icon: CloudSun },
  { path: '/modele-proba', label: 'Modèle Proba', icon: BarChart3 },
  { path: '/insar', label: 'InSAR', icon: Radar },
  { path: '/maintenance', label: 'Maintenance & Optimisation', icon: Wrench },
  { path: '/exports', label: 'Exports', icon: FileOutput },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">G</div>
        <div className="sidebar-title">
          <h1>GÉODIA</h1>
          <span>SentinelCare GC</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive =
            item.path === '/'
              ? location.pathname === '/'
              : location.pathname.startsWith(item.path);

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={`nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-version">v1.0.0 — Prototype V1</div>
      </div>
    </aside>
  );
}
