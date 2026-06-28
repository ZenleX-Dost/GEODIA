"""
Core computed indices for GÉODIA.
Implements: ICF, IVP, IPD, IED (Sprint 1), IAE (Sprint 4), IAD (Sprint 5), IPM (Sprint 6).
"""


def compute_ipd(icf: float, ivp: float) -> float:
    """
    Diagnostic Priority Index.
    IPD = 0.70 * ICF + 0.30 * IVP
    Class A if IPD >= 90%
    """
    return round(0.70 * icf + 0.30 * ivp, 2)


def compute_ied(
    inspection_complexity: float,
    aggressiveness: float,
    criticality: float,
    accessibility: float,
    uncertainty: float,
) -> float:
    """
    Diagnostic Effort Index.
    IED = 100 * (0.35*I + 0.25*A + 0.20*C + 0.10*Acc + 0.10*Inc)
    All inputs normalized 0-1.
    """
    return round(
        100 * (
            0.35 * inspection_complexity
            + 0.25 * aggressiveness
            + 0.20 * criticality
            + 0.10 * accessibility
            + 0.10 * uncertainty
        ),
        2,
    )


def classify_ipd(ipd: float) -> str:
    """Classify IPD into A/B/C/D."""
    if ipd >= 90:
        return "A"
    elif ipd >= 60:
        return "B"
    elif ipd >= 30:
        return "C"
    else:
        return "D"


# --- Sprint 4 additions (stubs for now) ---


def compute_iae(
    t: float, h: float, m: float, r: float, p: float, w: float
) -> float:
    """
    Environmental Aggressiveness Index.
    IAE = 0.20*T + 0.20*H + 0.20*M + 0.15*R + 0.15*P + 0.10*W
    All inputs normalized 0-1.
    """
    return round(0.20 * t + 0.20 * h + 0.20 * m + 0.15 * r + 0.15 * p + 0.10 * w, 4)


# --- Sprint 5 additions (stubs for now) ---


def compute_iad(
    v: float, d: float, a: float, c: float, q: float
) -> float:
    """
    Deformation Anomaly Index (InSAR).
    IAD = 0.30*V + 0.25*D + 0.20*A + 0.15*C + 0.10*Q
    All inputs normalized 0-1.
    """
    return round(0.30 * v + 0.25 * d + 0.20 * a + 0.15 * c + 0.10 * q, 4)


# --- Sprint 6 additions (stubs for now) ---


def compute_ipm(
    ipd_n: float, e_n: float, p0_n: float, iae: float, iad: float
) -> float:
    """
    Maintenance Priority Index.
    IPM = 0.30*IPD_n + 0.20*E_n + 0.20*P0_n + 0.15*IAE + 0.15*IAD
    All inputs normalized 0-1.
    """
    return round(
        0.30 * ipd_n + 0.20 * e_n + 0.20 * p0_n + 0.15 * iae + 0.15 * iad, 4
    )
