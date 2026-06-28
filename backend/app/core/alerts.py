from typing import List, Dict

def evaluate_alerts(ouvrage_data: dict, proba_data: dict, insar_data: dict, env_data: dict) -> List[Dict]:
    """
    Evaluate alert rules from the spec.
    """
    alerts = []
    classe = ouvrage_data.get('classe', 'C')
    p2 = proba_data.get('P2', 0.0)
    p8 = proba_data.get('P8', 0.0)
    p9 = proba_data.get('P9', 0.0)
    iad = ouvrage_data.get('iad', 0.0)
    iae = ouvrage_data.get('iae', 0.0)
    
    # 1. Class A + P2 > 60% → critical corrosion inspection
    if classe == 'A' and p2 > 0.60:
        alerts.append({
            "type": "corrosion_critique",
            "level": "critical",
            "message": "Classe A + P2 > 60% : Inspection de corrosion critique requise."
        })
        
    # 2. IAD > 0.60 + consensus >= 2 -> GPR/leveling
    consensus = insar_data.get('consensus_max', 0)
    if iad > 0.60 and consensus >= 2:
        alerts.append({
            "type": "anomalie_insar",
            "level": "high",
            "message": f"IAD ({iad:.2f}) > 0.60 et consensus fort : Nivellement/Géomatique requis."
        })
        
    # 3. IAE > 0.70 + P8/P9 > 60% -> chemical sampling
    if iae > 0.70 and (p8 > 0.60 or p9 > 0.60):
        alerts.append({
            "type": "attaque_chimique",
            "level": "high",
            "message": f"IAE ({iae:.2f}) > 0.70 et P8/P9 > 60% : Carottage et analyse chimique recommandés."
        })
        
    # 4. E3 état -> emergency alert
    if ouvrage_data.get('etat_global') == 'E3':
        alerts.append({
            "type": "etat_urgence",
            "level": "emergency",
            "message": "État global E3 détecté : Mise en sécurité immédiate de la structure."
        })
        
    return alerts
