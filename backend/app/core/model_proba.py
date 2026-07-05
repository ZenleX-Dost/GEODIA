import math
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.proba import Proba
from app.models.env_timeseries import EnvTimeseries
from app.models.insar_point import InsarPoint

def sigmoid(x: float) -> float:
    if x < -100: return 0.0
    if x > 100: return 1.0
    return 1 / (1 + math.exp(-x))

def logit(p: float) -> float:
    p = max(0.0001, min(0.9999, p))
    return math.log(p / (1 - p))

def compute_proba(E: int, F: float, H: float, V: float, D: float, IAE: float, IAD: float, beta_coeffs: dict) -> float:
    """
    Compute logistic probability from spec.
    """
    b0 = beta_coeffs.get('b0', 0)
    b1 = beta_coeffs.get('b1', 0)
    b2 = beta_coeffs.get('b2', 0)
    b3 = beta_coeffs.get('b3', 0)
    b4 = beta_coeffs.get('b4', 0)
    b5 = beta_coeffs.get('b5', 0)
    b6 = beta_coeffs.get('b6', 0)
    b7 = beta_coeffs.get('b7', 0)
    
    logit_val = b0 + (b1 * E) + (b2 * F) + (b3 * H) + (b4 * V) + (b5 * D) + (b6 * IAE) + (b7 * IAD)
    return sigmoid(logit_val)

def classify_probability(p: float) -> str:
    if p < 0.25:
        return "Low"
    elif p < 0.50:
        return "Moderate"
    elif p < 0.75:
        return "High"
    else:
        return "Very High"

def recalculate_probabilities(db: Session, ouvrage_id: int):
    """
    Recalculates the dynamic probability (p_current) for all pathologies of an ouvrage 
    using the CDC logistic equation, based on the latest IAE and IAD.
    """
    # Get latest IAE
    latest_env = db.query(EnvTimeseries).filter(EnvTimeseries.ouvrage_id == ouvrage_id).order_by(desc(EnvTimeseries.date)).first()
    iae = latest_env.iae if latest_env and latest_env.iae else 0.0
    
    # Get latest IAD
    latest_insar = db.query(InsarPoint).filter(InsarPoint.ouvrage_id == ouvrage_id).order_by(desc(InsarPoint.date_end)).first()
    iad = latest_insar.iad if latest_insar and latest_insar.iad else 0.0
    
    # Get all probabilities for this ouvrage
    probas = db.query(Proba).filter(Proba.ouvrage_id == ouvrage_id).all()
    
    for p in probas:
        p0_val = p.p0 / 100.0  # p0 is stored as percentage
        if p0_val <= 0:
            p.p_current = 0
            continue
            
        # 1. Convert P0 to base log-odds (Z0)
        z0 = logit(p0_val)
        
        # 2. Add dynamic environmental and deformation factors
        # z = z0 + 1.0*IAE + 0.9*IAD
        z_new = z0 + 1.0 * iae + 0.9 * iad
        
        # 3. Convert back to probability
        p_current_val = sigmoid(z_new)
        
        p.p_current = round(p_current_val * 100.0, 2)
        p.iae = iae
        p.iad = iad
        p.source = "Dynamic CDC Logistic Model"
        
    db.commit()
