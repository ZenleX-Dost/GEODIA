"""
GEODIA — Unit Tests for Core Business Logic

Tests: probabilistic model, alert engine, budget optimizer,
       InSAR pipeline, environmental indices.
"""
import math
import pytest


# ═══════════════════════════════════════════════════════════════════
# 1. PROBABILISTIC MODEL  (app/core/model_proba.py)
# ═══════════════════════════════════════════════════════════════════

class TestModelProba:
    def test_sigmoid_center(self):
        from app.core.model_proba import sigmoid
        assert sigmoid(0) == pytest.approx(0.5, abs=1e-9)

    def test_sigmoid_large_positive(self):
        from app.core.model_proba import sigmoid
        assert sigmoid(100) == pytest.approx(1.0, abs=1e-6)

    def test_sigmoid_large_negative(self):
        from app.core.model_proba import sigmoid
        assert sigmoid(-100) == pytest.approx(0.0, abs=1e-6)

    def test_sigmoid_range(self):
        from app.core.model_proba import sigmoid
        for x in [-10, -5, 0, 5, 10]:
            val = sigmoid(x)
            assert 0 <= val <= 1, f"sigmoid({x}) = {val} out of [0,1]"

    def test_logit_inverse_sigmoid(self):
        from app.core.model_proba import sigmoid, logit
        for p in [0.1, 0.3, 0.5, 0.7, 0.9]:
            assert sigmoid(logit(p)) == pytest.approx(p, abs=1e-9)

    def test_compute_proba_pure_zero_inputs(self):
        from app.core.model_proba import compute_proba
        p = compute_proba(0, 0, 0, 0, 0, 0, 0, {"b0": 0})
        assert p == pytest.approx(0.5, abs=1e-9)

    def test_compute_proba_high_iad_raises_proba(self):
        from app.core.model_proba import compute_proba
        beta = {"b0": -1.0, "b7": 3.0}   # strong IAD coefficient
        p_low_iad = compute_proba(0, 0, 0, 0, 0, 0, 0.1, beta)
        p_high_iad = compute_proba(0, 0, 0, 0, 0, 0, 0.9, beta)
        assert p_high_iad > p_low_iad, "Higher IAD should increase probability"

    def test_classify_probability(self):
        from app.core.model_proba import classify_probability
        assert classify_probability(0.10) == "Low"
        assert classify_probability(0.30) == "Moderate"
        assert classify_probability(0.60) == "High"
        assert classify_probability(0.85) == "Very High"

    def test_recalculate_probabilities_updates_db(self, db_session, seed_proba, seed_env, seed_insar):
        from app.core.model_proba import recalculate_probabilities
        ouvrage_id = seed_proba[0].ouvrage_id
        # Should not raise
        recalculate_probabilities(db_session, ouvrage_id)
        # Re-query updated row
        from app.models.proba import Proba
        updated = db_session.query(Proba).filter(
            Proba.ouvrage_id == ouvrage_id
        ).first()
        assert updated is not None
        # p_current should now be set to a numeric value
        assert updated.p_current is not None
        assert 0 <= updated.p_current <= 100


# ═══════════════════════════════════════════════════════════════════
# 2. ALERT ENGINE  (app/core/alerts.py)
# ═══════════════════════════════════════════════════════════════════

class TestAlertEngine:
    def test_no_alerts_baseline(self):
        from app.core.alerts import evaluate_alerts
        alerts = evaluate_alerts(
            {"classe": "C", "iad": 0.0, "iae": 0.0, "etat_global": "E0"},
            {}, {}, {}
        )
        assert alerts == []

    def test_class_a_p2_critical_alert(self):
        from app.core.alerts import evaluate_alerts
        alerts = evaluate_alerts(
            {"classe": "A", "iad": 0.0, "iae": 0.0, "etat_global": "E0"},
            {"P2": 0.75}, {}, {}
        )
        types = [a["type"] for a in alerts]
        assert "corrosion_critique" in types

    def test_class_a_p2_below_threshold_no_alert(self):
        from app.core.alerts import evaluate_alerts
        alerts = evaluate_alerts(
            {"classe": "A", "iad": 0.0, "iae": 0.0, "etat_global": "E0"},
            {"P2": 0.50}, {}, {}     # 50% ≤ 60% threshold
        )
        types = [a["type"] for a in alerts]
        assert "corrosion_critique" not in types

    def test_insar_anomaly_alert(self):
        from app.core.alerts import evaluate_alerts
        alerts = evaluate_alerts(
            {"classe": "B", "iad": 0.75, "iae": 0.3, "etat_global": "E0"},
            {}, {"consensus_max": 3}, {}
        )
        types = [a["type"] for a in alerts]
        assert "anomalie_insar" in types

    def test_insar_alert_missing_consensus(self):
        from app.core.alerts import evaluate_alerts
        # High IAD but consensus < 2 → no alert
        alerts = evaluate_alerts(
            {"classe": "B", "iad": 0.75, "iae": 0.3, "etat_global": "E0"},
            {}, {"consensus_max": 1}, {}
        )
        types = [a["type"] for a in alerts]
        assert "anomalie_insar" not in types

    def test_chemical_attack_alert(self):
        from app.core.alerts import evaluate_alerts
        alerts = evaluate_alerts(
            {"classe": "C", "iad": 0.0, "iae": 0.80, "etat_global": "E0"},
            {"P8": 0.65}, {}, {}
        )
        types = [a["type"] for a in alerts]
        assert "attaque_chimique" in types

    def test_emergency_state_e3(self):
        from app.core.alerts import evaluate_alerts
        alerts = evaluate_alerts(
            {"classe": "D", "iad": 0.0, "iae": 0.0, "etat_global": "E3"},
            {}, {}, {}
        )
        types = [a["type"] for a in alerts]
        levels = [a["level"] for a in alerts]
        assert "etat_urgence" in types
        assert "emergency" in levels

    def test_multiple_alerts_simultaneously(self):
        from app.core.alerts import evaluate_alerts
        alerts = evaluate_alerts(
            {"classe": "A", "iad": 0.85, "iae": 0.80, "etat_global": "E3"},
            {"P2": 0.80, "P8": 0.70}, {"consensus_max": 3}, {}
        )
        # Should trigger all 4 rules
        assert len(alerts) >= 4

    def test_alert_has_required_keys(self):
        from app.core.alerts import evaluate_alerts
        alerts = evaluate_alerts(
            {"classe": "A", "iad": 0.0, "iae": 0.0, "etat_global": "E3"},
            {}, {}, {}
        )
        for alert in alerts:
            assert "type" in alert
            assert "level" in alert
            assert "message" in alert


# ═══════════════════════════════════════════════════════════════════
# 3. BUDGET OPTIMIZER  (app/core/optimizer.py)
# ═══════════════════════════════════════════════════════════════════

class TestOptimizer:
    ACTIONS = [
        {"id": 1, "ouvrage_id": 1, "cost": 50_000, "risk_gain": 0.9,
         "is_class_a_critical": True, "is_class_a_high": False},
        {"id": 2, "ouvrage_id": 2, "cost": 80_000, "risk_gain": 0.7,
         "is_class_a_critical": False, "is_class_a_high": True},
        {"id": 3, "ouvrage_id": 3, "cost": 200_000, "risk_gain": 0.4,
         "is_class_a_critical": False, "is_class_a_high": False},
    ]

    def test_s1_within_budget(self):
        from app.core.optimizer import run_budget_optimization
        result = run_budget_optimization(self.ACTIONS, 130_000, "S1")
        assert result["status"] == "Optimal"
        assert result["total_cost"] <= 130_000

    def test_s2_forces_critical_actions(self):
        from app.core.optimizer import run_budget_optimization
        result = run_budget_optimization(self.ACTIONS, 500_000, "S2")
        # Action 1 is class A critical → must be selected
        assert 1 in result["selected_actions"]

    def test_s3_forces_high_actions(self):
        from app.core.optimizer import run_budget_optimization
        result = run_budget_optimization(self.ACTIONS, 500_000, "S3")
        # Both critical and high must be selected
        assert 1 in result["selected_actions"]
        assert 2 in result["selected_actions"]

    def test_budget_zero_selects_nothing(self):
        from app.core.optimizer import run_budget_optimization
        result = run_budget_optimization(
            [a for a in self.ACTIONS if not a["is_class_a_critical"]],
            0.0, "S1"
        )
        assert result["total_cost"] == 0

    def test_budget_pct_correct(self):
        from app.core.optimizer import run_budget_optimization
        result = run_budget_optimization(self.ACTIONS, 100_000, "S1")
        expected_pct = result["total_cost"] / 100_000 * 100
        assert result["budget_used_pct"] == pytest.approx(expected_pct, abs=0.01)

    def test_empty_actions_list(self):
        from app.core.optimizer import run_budget_optimization
        result = run_budget_optimization([], 500_000, "S1")
        assert result["total_cost"] == 0
        assert result["selected_actions"] == []


# ═══════════════════════════════════════════════════════════════════
# 4. ENVIRONMENTAL INDICES  (app/core/indices.py)
# ═══════════════════════════════════════════════════════════════════

class TestIndices:
    def test_iae_range(self):
        from app.core.indices import compute_iae
        iae = compute_iae(t=0.5, h=0.7, m=0.8, r=0.3, p=0.2, w=0.4)
        assert 0 <= iae <= 1, f"IAE = {iae} is out of [0, 1]"

    def test_iae_increases_with_pollution(self):
        from app.core.indices import compute_iae
        iae_low = compute_iae(t=0.5, h=0.5, m=0.5, r=0.0, p=0.0, w=0.2)
        iae_high = compute_iae(t=0.5, h=0.5, m=0.5, r=0.0, p=1.0, w=0.2)
        assert iae_high >= iae_low, "Higher pollution should not decrease IAE"

    def test_iae_max_conditions(self):
        from app.core.indices import compute_iae
        iae = compute_iae(t=1.0, h=1.0, m=1.0, r=1.0, p=1.0, w=1.0)
        assert iae <= 1.0, "IAE should be clamped to 1.0 at max conditions"

    def test_iae_min_conditions(self):
        from app.core.indices import compute_iae
        iae = compute_iae(t=0.0, h=0.0, m=0.0, r=0.0, p=0.0, w=0.0)
        assert iae >= 0.0, "IAE should be >= 0 at zero conditions"


# ═══════════════════════════════════════════════════════════════════
# 5. INSAR PIPELINE  (app/core/insar_pipeline.py)
# ═══════════════════════════════════════════════════════════════════

class TestInsarPipeline:
    SAMPLE_POINTS = [
        {"id": 1, "lat": 33.1, "lon": -8.6, "vitesse_los": -7.0, "cumul": -21.0},
        {"id": 2, "lat": 33.2, "lon": -8.7, "vitesse_los": -2.0, "cumul":  -5.0},
        {"id": 3, "lat": 33.3, "lon": -8.8, "vitesse_los": -0.5, "cumul":  -1.0},
    ]

    def test_pipeline_returns_same_count(self):
        from app.core.insar_pipeline import execute_insar_pipeline
        result = execute_insar_pipeline(self.SAMPLE_POINTS)
        assert len(result) == len(self.SAMPLE_POINTS)

    def test_pipeline_adds_consensus_level(self):
        from app.core.insar_pipeline import execute_insar_pipeline
        result = execute_insar_pipeline(self.SAMPLE_POINTS)
        for pt in result:
            assert "consensus_level" in pt, "Each processed point should have 'consensus_level'"
            assert pt["consensus_level"] in [0, 1, 2, 3], \
                f"consensus_level = {pt['consensus_level']} not in {{0,1,2,3}}"

    def test_pipeline_adds_anomaly_flag(self):
        from app.core.insar_pipeline import execute_insar_pipeline
        result = execute_insar_pipeline(self.SAMPLE_POINTS)
        for pt in result:
            assert "is_anomaly_iso" in pt, "Each processed point should have 'is_anomaly_iso'"
            assert isinstance(pt["is_anomaly_iso"], bool)

    def test_high_velocity_gets_vote(self):
        """Point with v_los < -5 should get at least 1 consensus vote."""
        from app.core.insar_pipeline import execute_insar_pipeline
        result = execute_insar_pipeline(self.SAMPLE_POINTS)
        high_vel_pts = [pt for pt in result if pt.get("vitesse_los", 0) < -5.0]
        for pt in high_vel_pts:
            assert pt["consensus_level"] >= 1, "High-velocity point should have ≥1 vote"

    def test_empty_pipeline(self):
        from app.core.insar_pipeline import execute_insar_pipeline
        result = execute_insar_pipeline([])
        assert result == []

    def test_pipeline_adds_cluster_id(self):
        from app.core.insar_pipeline import execute_insar_pipeline
        result = execute_insar_pipeline(self.SAMPLE_POINTS)
        for pt in result:
            assert "cluster_id" in pt, "Each point should have a cluster_id after DBSCAN"


# ═══════════════════════════════════════════════════════════════════
# 6. STRUCTURAL INDICES  (app/core/indices.py)
# ═══════════════════════════════════════════════════════════════════

class TestStructuralIndices:
    def test_compute_ipd_formula(self):
        from app.core.indices import compute_ipd
        # IPD = 0.70*ICF + 0.30*IVP
        assert compute_ipd(100, 100) == pytest.approx(100.0)
        assert compute_ipd(70, 60) == pytest.approx(0.70 * 70 + 0.30 * 60, abs=0.01)

    def test_classify_ipd(self):
        from app.core.indices import classify_ipd
        assert classify_ipd(95) == "A"
        assert classify_ipd(75) == "B"
        assert classify_ipd(45) == "C"
        assert classify_ipd(10) == "D"

    def test_compute_ied_range(self):
        from app.core.indices import compute_ied
        ied = compute_ied(0.5, 0.5, 0.5, 0.5, 0.5)
        assert 0 <= ied <= 100

    def test_compute_ied_max(self):
        from app.core.indices import compute_ied
        ied = compute_ied(1.0, 1.0, 1.0, 1.0, 1.0)
        assert ied == pytest.approx(100.0)

    def test_compute_iad_formula(self):
        from app.core.indices import compute_iad
        # IAD = 0.30*V + 0.25*D + 0.20*A + 0.15*C + 0.10*Q
        iad = compute_iad(1.0, 1.0, 1.0, 1.0, 1.0)
        assert iad == pytest.approx(1.0)
        iad_zero = compute_iad(0, 0, 0, 0, 0)
        assert iad_zero == 0.0

    def test_compute_ipm_range(self):
        from app.core.indices import compute_ipm
        ipm = compute_ipm(0.5, 0.5, 0.5, 0.5, 0.5)
        assert 0 <= ipm <= 1
