/**
 * Scientific Disclaimer banner — displays the 4 limitations from spec §21.
 */
import { AlertTriangle } from 'lucide-react';

export default function ScientificDisclaimer() {
  return (
    <div className="disclaimer-banner">
      <AlertTriangle size={18} />
      <div className="disclaimer-text">
        <strong>Limitations scientifiques :</strong>{' '}
        Les probabilités ne sont pas des diagnostics. Les données satellites ne donnent pas la cause d'une pathologie béton. 
        L'InSAR signale des déformations dans la ligne de visée, pas la cause. 
        Toute action de maintenance doit être validée par un ingénieur et par des preuves terrain.
      </div>
    </div>
  );
}
