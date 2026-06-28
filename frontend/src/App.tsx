/**
 * GÉODIA SentinelCare GC — Main Application
 * React Router v6 with persistent sidebar layout.
 */
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/layout/Sidebar';
import Cockpit from './pages/Cockpit';
import Portfolio from './pages/Portfolio';
import MapPage from './pages/MapPage';
import Inspection from './pages/Inspection';
import StructureSheet from './pages/StructureSheet';
import Environment from './pages/Environment';
import ProbabilisticModel from './pages/ProbabilisticModel';
import InSAR from './pages/InSAR';
import Maintenance from './pages/Maintenance';
import Exports from './pages/Exports';

import './index.css';

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar />
        <div className="app-content">
          <Routes>
            <Route path="/" element={<Cockpit />} />
            <Route path="/portfolio" element={<Portfolio />} />
            <Route path="/carte" element={<MapPage />} />
            <Route path="/inspection" element={<Inspection />} />
            <Route path="/ouvrage/:id" element={<StructureSheet />} />
            <Route path="/environnement" element={<Environment />} />
            <Route path="/modele-proba" element={<ProbabilisticModel />} />
            <Route path="/insar" element={<InSAR />} />
            <Route path="/maintenance" element={<Maintenance />} />
            <Route path="/exports" element={<Exports />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
