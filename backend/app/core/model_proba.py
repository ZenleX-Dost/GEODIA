import math

def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))

def compute_proba(E: int, F: float, H: float, V: float, D: float, IAE: float, IAD: float, beta_coeffs: dict) -> float:
    """
    Compute logistic probability from spec.
    p = 1 / (1 + e^-(beta0 + beta1*E + beta2*F + beta3*H + beta4*V + beta5*D + beta6*IAE + beta7*IAD))
    """
    b0 = beta_coeffs.get('b0', 0)
    b1 = beta_coeffs.get('b1', 0)
    b2 = beta_coeffs.get('b2', 0)
    b3 = beta_coeffs.get('b3', 0)
    b4 = beta_coeffs.get('b4', 0)
    b5 = beta_coeffs.get('b5', 0)
    b6 = beta_coeffs.get('b6', 0)
    b7 = beta_coeffs.get('b7', 0)
    
    logit = b0 + (b1 * E) + (b2 * F) + (b3 * H) + (b4 * V) + (b5 * D) + (b6 * IAE) + (b7 * IAD)
    return sigmoid(logit)

def classify_probability(p: float) -> str:
    if p < 0.25:
        return "Low"
    elif p < 0.50:
        return "Moderate"
    elif p < 0.75:
        return "High"
    else:
        return "Very High"
