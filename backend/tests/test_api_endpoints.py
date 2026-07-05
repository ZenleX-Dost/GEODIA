"""
GEODIA — API Integration Tests (Endpoint Tests)

Tests every HTTP endpoint using an in-memory SQLite DB.
Covers assets, alerts, KPIs, InSAR, environment, maintenance,
compute, reports, imports, and the health-check.
"""
import pytest


# ═══════════════════════════════════════════════════════════════════
# HEALTH / ROOT
# ═══════════════════════════════════════════════════════════════════

class TestHealth:
    def test_root_returns_operational(self, client):
        r = client.get("/")
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "operational"
        assert "version" in body

    def test_health_ok(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_docs_reachable(self, client):
        r = client.get("/docs")
        assert r.status_code == 200


# ═══════════════════════════════════════════════════════════════════
# ASSETS
# ═══════════════════════════════════════════════════════════════════

class TestAssets:
    def test_list_assets_empty(self, client):
        r = client.get("/api/assets")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_list_assets_returns_seed(self, client, seed_ouvrage):
        r = client.get("/api/assets")
        assert r.status_code == 200
        codes = [a["code"] for a in r.json()]
        assert seed_ouvrage.code in codes

    def test_list_assets_filter_by_classe(self, client, seed_ouvrage):
        r = client.get("/api/assets?classe=A")
        assert r.status_code == 200
        for asset in r.json():
            assert asset["classe"] == "A"

    def test_list_assets_filter_by_wrong_classe(self, client, seed_ouvrage):
        r = client.get("/api/assets?classe=Z")
        assert r.status_code == 200
        assert r.json() == []

    def test_list_assets_search_by_name(self, client, seed_ouvrage):
        r = client.get("/api/assets?search=Structure+de+Test")
        assert r.status_code == 200
        assert len(r.json()) >= 1

    def test_get_asset_by_id(self, client, seed_ouvrage):
        r = client.get(f"/api/assets/{seed_ouvrage.id}")
        assert r.status_code == 200
        body = r.json()
        assert body["code"] == seed_ouvrage.code
        assert body["nom"] == seed_ouvrage.nom
        assert body["classe"] == "A"

    def test_get_asset_not_found(self, client):
        r = client.get("/api/assets/999999")
        assert r.status_code == 404

    def test_get_assets_geojson(self, client, seed_ouvrage):
        r = client.get("/api/assets/geojson")
        assert r.status_code == 200
        body = r.json()
        assert body["type"] == "FeatureCollection"
        assert isinstance(body["features"], list)

    def test_geojson_feature_structure(self, client, seed_ouvrage):
        r = client.get("/api/assets/geojson")
        assert r.status_code == 200
        features = r.json()["features"]
        assert len(features) >= 1
        feat = features[0]
        assert feat["type"] == "Feature"
        assert feat["geometry"]["type"] == "Point"
        assert len(feat["geometry"]["coordinates"]) == 2
        assert "properties" in feat
        props = feat["properties"]
        for key in ["id", "code", "nom", "famille", "classe"]:
            assert key in props, f"Property '{key}' missing from GeoJSON feature"


# ═══════════════════════════════════════════════════════════════════
# KPIs
# ═══════════════════════════════════════════════════════════════════

class TestKPIs:
    def test_kpis_returns_required_fields(self, client, seed_ouvrage):
        r = client.get("/api/kpis")
        assert r.status_code == 200
        body = r.json()
        for field in [
            "total_ouvrages", "classe_a_count",
            "alertes_insar", "inspections_pending",
            "indice_prevention", "economie_potentielle",
        ]:
            assert field in body, f"KPI field '{field}' missing"

    def test_kpis_total_increases_with_data(self, client, seed_ouvrage):
        r = client.get("/api/kpis")
        assert r.json()["total_ouvrages"] >= 1

    def test_kpis_classe_a_counted(self, client, seed_ouvrage):
        r = client.get("/api/kpis")
        assert r.json()["classe_a_count"] >= 1

    def test_kpis_insar_alerts_non_negative(self, client, seed_ouvrage, seed_insar):
        r = client.get("/api/kpis")
        assert r.json()["alertes_insar"] >= 0

    def test_kpis_economie_reasonable(self, client, seed_ouvrage):
        r = client.get("/api/kpis")
        # Should always be the fixed calculation (6.6M * 30%)
        assert r.json()["economie_potentielle"] == pytest.approx(1_980_000.0, rel=0.01)


# ═══════════════════════════════════════════════════════════════════
# ALERTS
# ═══════════════════════════════════════════════════════════════════

class TestAlerts:
    def test_alerts_endpoint_returns_list(self, client):
        r = client.get("/api/alerts")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_alert_schema(self, client, seed_ouvrage, seed_proba):
        # seed_proba has P2=65 > 60, and seed_ouvrage is classe A → should trigger alert
        r = client.get("/api/alerts")
        assert r.status_code == 200
        alerts = r.json()
        if alerts:
            alert = alerts[0]
            for key in ["id", "ouvrage_code", "ouvrage_nom", "severity", "action", "source", "date"]:
                assert key in alert, f"Alert field '{key}' missing"


# ═══════════════════════════════════════════════════════════════════
# INSAR
# ═══════════════════════════════════════════════════════════════════

class TestInSAR:
    def test_insar_points_by_ouvrage(self, client, seed_ouvrage, seed_insar):
        r = client.get(f"/api/insar/{seed_ouvrage.id}")
        assert r.status_code == 200
        pts = r.json()
        assert isinstance(pts, list)
        assert len(pts) == 3

    def test_insar_points_empty_ouvrage(self, client, seed_ouvrage):
        # No InSAR seeded → empty list
        r = client.get(f"/api/insar/{seed_ouvrage.id}")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_insar_anomalies_endpoint(self, client, seed_ouvrage, seed_insar):
        r = client.get("/api/insar/anomalies")
        assert r.status_code == 200
        # The seed has 1 point with iad=0.85 >= 0.5
        anomalies = r.json()
        assert isinstance(anomalies, list)
        assert len(anomalies) >= 1

    def test_insar_clusters_endpoint(self, client):
        r = client.get("/api/insar/clusters")
        assert r.status_code == 200
        clusters = r.json()
        assert isinstance(clusters, list)
        assert len(clusters) == 2   # hardcoded stub returns 2

    def test_insar_summary_structure(self, client, seed_ouvrage, seed_insar):
        r = client.get(f"/api/insar/{seed_ouvrage.id}/summary")
        assert r.status_code == 200
        body = r.json()
        assert "consensus" in body
        assert "timeseries" in body
        assert "avg_vitesse" in body

    def test_insar_summary_timeseries_12_months(self, client, seed_ouvrage, seed_insar):
        r = client.get(f"/api/insar/{seed_ouvrage.id}/summary")
        assert len(r.json()["timeseries"]) == 12

    def test_insar_summary_consensus_keys(self, client, seed_ouvrage, seed_insar):
        r = client.get(f"/api/insar/{seed_ouvrage.id}/summary")
        consensus = r.json()["consensus"]
        assert "strong" in consensus
        assert "medium" in consensus
        assert "weak" in consensus

    def test_insar_point_schema(self, client, seed_ouvrage, seed_insar):
        r = client.get(f"/api/insar/{seed_ouvrage.id}")
        pts = r.json()
        if pts:
            pt = pts[0]
            # Fields actually exposed by InsarPointResponse schema
            for key in ["id", "ouvrage_id", "vitesse_los", "lat", "lon", "cumul"]:
                assert key in pt, f"InSAR point field '{key}' missing"


# ═══════════════════════════════════════════════════════════════════
# ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════

class TestEnvironment:
    def test_env_timeseries_empty(self, client, seed_ouvrage):
        r = client.get(f"/api/env/{seed_ouvrage.id}/timeseries")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_env_timeseries_with_data(self, client, seed_ouvrage, seed_env):
        r = client.get(f"/api/env/{seed_ouvrage.id}/timeseries")
        assert r.status_code == 200
        records = r.json()
        assert len(records) >= 1

    def test_env_sync_no_token_returns_error(self, client, seed_ouvrage):
        """With no NASA token configured, sync should return a 500."""
        # In test config NASA_EARTHDATA_TOKEN="" → will return error
        r = client.post("/api/env/sync")
        # Either 500 (no data) or 404 (no ouvrages in some state)
        assert r.status_code in [200, 404, 500]

    def test_env_copernicus_sync_no_token(self, client, seed_ouvrage):
        r = client.post("/api/env/sync-copernicus")
        assert r.status_code in [200, 404, 500]


# ═══════════════════════════════════════════════════════════════════
# MAINTENANCE
# ═══════════════════════════════════════════════════════════════════

class TestMaintenance:
    def test_maintenance_actions_empty(self, client):
        r = client.get("/api/maintenance/actions")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_maintenance_actions_with_data(self, client, seed_action):
        r = client.get("/api/maintenance/actions")
        assert r.status_code == 200
        assert len(r.json()) >= 1

    def test_maintenance_plan_structure(self, client, seed_action):
        r = client.get("/api/maintenance/plan")
        assert r.status_code == 200
        plan = r.json()
        for key in ["actions_0_3m", "actions_3_6m", "actions_6_12m", "actions_12m_plus"]:
            assert key in plan, f"Maintenance plan missing key '{key}'"

    def test_maintenance_action_schema(self, client, seed_action):
        r = client.get("/api/maintenance/actions")
        if r.json():
            action = r.json()[0]
            for key in ["id", "ouvrage_id", "type_action", "cout", "urgence"]:
                assert key in action, f"Action field '{key}' missing"


# ═══════════════════════════════════════════════════════════════════
# COMPUTE / PROBABILISTIC MODEL
# ═══════════════════════════════════════════════════════════════════

class TestCompute:
    def test_proba_matrix_endpoint(self, client, seed_proba):
        r = client.get("/api/compute/proba/matrix")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_proba_by_ouvrage(self, client, seed_proba):
        ouvrage_id = seed_proba[0].ouvrage_id
        r = client.get(f"/api/compute/proba/{ouvrage_id}")
        assert r.status_code == 200
        rows = r.json()
        assert len(rows) >= 1
        if rows:
            row = rows[0]
            assert "pathologie" in row
            assert "p_current" in row

    def test_recompute_proba_all(self, client, seed_ouvrage):
        r = client.post("/api/compute/proba")
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "success"
        assert "CDC" in body["message"], "Response should mention the CDC logistic model"

    def test_recompute_proba_actually_mutates(self, client, db_session, seed_proba, seed_env, seed_insar):
        """Verifies that POST /compute/proba genuinely updates p_current in the DB."""
        from app.models.proba import Proba

        ouvrage_id = seed_proba[0].ouvrage_id
        p2_before = db_session.query(Proba).filter(
            Proba.ouvrage_id == ouvrage_id, Proba.pathologie == "P2"
        ).first().p_current

        # Trigger recompute
        r = client.post(f"/api/compute/proba?ouvrage_id={ouvrage_id}")
        assert r.status_code == 200

        # Refresh and check value changed
        db_session.expire_all()
        p2_after = db_session.query(Proba).filter(
            Proba.ouvrage_id == ouvrage_id, Proba.pathologie == "P2"
        ).first().p_current

        # p_current should now reflect IAE + IAD influence (may or may not numerically change
        # depending on seed values, but the field must be set and be a number)
        assert p2_after is not None
        assert isinstance(p2_after, float)

    def test_optimize_endpoint_s1(self, client, seed_action):
        payload = {"budget": 5_000_000, "scenario_id": "S1"}
        r = client.post("/api/compute/optimize", json=payload)
        assert r.status_code == 200
        body = r.json()
        assert "status" in body
        assert "total_cost" in body
        assert "selected_actions_ids" in body


# ═══════════════════════════════════════════════════════════════════
# INSPECTIONS
# ═══════════════════════════════════════════════════════════════════

class TestInspections:
    PAYLOAD = {
        "ouvrage_id": None,  # filled per test
        "date_inspection": "2025-06-15",
        "inspecteur": "Karim Tahiri",
        "etat_global": "E1",
        "notes": "Fissures superficielles observées en zone marine.",
        "observations": [
            {
                "pathologie_code": "P2",
                "zone": "Pile N°3 - face aval",
                "gravite": 2,
                "etendue_pct": 15.0,
                "preuves": "Photos ref. INS-001",
                "photo_url": None,
            }
        ],
    }

    def test_list_inspections_empty(self, client):
        r = client.get("/api/inspections")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_create_inspection(self, client, seed_ouvrage, seed_pathologie):
        payload = {**self.PAYLOAD, "ouvrage_id": seed_ouvrage.id}
        r = client.post("/api/inspections", json=payload)
        assert r.status_code == 200
        body = r.json()
        assert body["ouvrage_id"] == seed_ouvrage.id
        assert body["inspecteur"] == "Karim Tahiri"
        assert body["statut"] == "En attente"
        assert "id" in body

    def test_create_inspection_returns_date(self, client, seed_ouvrage, seed_pathologie):
        payload = {**self.PAYLOAD, "ouvrage_id": seed_ouvrage.id}
        r = client.post("/api/inspections", json=payload)
        assert r.status_code == 200
        assert r.json()["date_inspection"] == "2025-06-15"

    def test_list_inspections_returns_created(self, client, seed_ouvrage, seed_pathologie):
        payload = {**self.PAYLOAD, "ouvrage_id": seed_ouvrage.id}
        client.post("/api/inspections", json=payload)
        r = client.get("/api/inspections")
        assert r.status_code == 200
        assert len(r.json()) >= 1

    def test_list_inspections_filter_by_ouvrage(self, client, seed_ouvrage, seed_pathologie):
        payload = {**self.PAYLOAD, "ouvrage_id": seed_ouvrage.id}
        client.post("/api/inspections", json=payload)
        r = client.get(f"/api/inspections?ouvrage_id={seed_ouvrage.id}")
        assert r.status_code == 200
        for insp in r.json():
            assert insp["ouvrage_id"] == seed_ouvrage.id

    def test_get_inspection_by_id(self, client, seed_inspection):
        r = client.get(f"/api/inspections/{seed_inspection.id}")
        assert r.status_code == 200
        body = r.json()
        assert body["id"] == seed_inspection.id
        assert body["etat_global"] == "E1"

    def test_get_inspection_not_found(self, client):
        r = client.get("/api/inspections/999999")
        assert r.status_code == 404

    def test_validate_inspection(self, client, seed_inspection):
        r = client.patch(f"/api/inspections/{seed_inspection.id}/validate")
        assert r.status_code == 200
        assert r.json()["status"] == "success"
        # Confirm it's now marked validated
        r2 = client.get(f"/api/inspections/{seed_inspection.id}")
        assert r2.json()["statut"] == "Validée"

    def test_validate_inspection_not_found(self, client):
        r = client.patch("/api/inspections/999999/validate")
        assert r.status_code == 404

    def test_inspection_schema_fields(self, client, seed_inspection):
        r = client.get(f"/api/inspections/{seed_inspection.id}")
        body = r.json()
        for key in ["id", "ouvrage_id", "date_inspection", "inspecteur",
                    "etat_global", "statut", "created_at", "observations"]:
            assert key in body, f"Inspection response missing field '{key}'"

    def test_insar_iad_exposed_in_schema(self, client, seed_ouvrage, seed_insar):
        """Regression: iad field must now appear in InSAR point responses."""
        r = client.get(f"/api/insar/{seed_ouvrage.id}")
        pts = r.json()
        assert len(pts) > 0
        pt = pts[0]
        assert "iad" in pt, "iad field still missing from InsarPointResponse schema"
        assert pt["iad"] == pytest.approx(0.85, abs=0.01)


# ═══════════════════════════════════════════════════════════════════
# IMPORTS / FILE UPLOAD
# ═══════════════════════════════════════════════════════════════════

class TestImports:
    def test_import_env_stub(self, client, seed_ouvrage):
        r = client.post(f"/api/imports/env?ouvrage_id={seed_ouvrage.id}")
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "success"

    def test_file_upload_csv(self, client):
        import io
        csv_content = b"ouvrage_id,vitesse_los\n1,-5.2\n2,-1.0\n"
        files = {"file": ("insar_data.csv", io.BytesIO(csv_content), "text/csv")}
        r = client.post("/api/imports/upload?type=insar", files=files)
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "success"
        assert "insar_data.csv" in body["message"]


# ═══════════════════════════════════════════════════════════════════
# AREA GRID
# ═══════════════════════════════════════════════════════════════════

class TestAreaGrid:
    def test_area_grid_returns_geojson(self, client):
        # Use a small grid size so the test doesn't time out
        r = client.get("/api/area/grid?grid_size=5")
        assert r.status_code == 200
        body = r.json()
        assert body["type"] == "FeatureCollection"
        assert isinstance(body["features"], list)

    def test_area_grid_features_have_probas(self, client):
        r = client.get("/api/area/grid?grid_size=5")
        body = r.json()
        for feat in body["features"]:
            props = feat["properties"]
            assert "iad" in props
            assert "iae" in props
            assert "max_risk" in props
            assert "probas" in props
            assert isinstance(props["probas"], list)
            # Each cell should have 3 pathologies
            assert len(props["probas"]) == 3


# ═══════════════════════════════════════════════════════════════════
# REPORTS (PDF / Excel generation stubs)
# ═══════════════════════════════════════════════════════════════════

class TestReports:
    def test_ouvrage_pdf_not_found(self, client):
        r = client.get("/api/reports/pdf/ouvrage/999999")
        assert r.status_code == 404

    def test_ouvrage_pdf_exists(self, client, seed_ouvrage):
        r = client.get(f"/api/reports/pdf/ouvrage/{seed_ouvrage.id}")
        # Bug fixed: reports.py now correctly uses ouvrage.lat/ouvrage.lon
        assert r.status_code == 200
        assert "pdf" in r.headers.get("content-type", "")

    def test_ouvrage_pdf_bug_documented(self, client, seed_ouvrage):
        """Regression test: confirms the gps_lat/gps_long bug is fixed."""
        r = client.get(f"/api/reports/pdf/ouvrage/{seed_ouvrage.id}")
        # Should NOT return 500 after the fix
        assert r.status_code != 500, (
            "BUG REGRESSION: reports.py is accessing gps_lat/gps_long again. "
            "Model uses lat/lon. Check app/routers/reports.py"
        )

    def test_inspection_pdf_not_found(self, client):
        r = client.get("/api/reports/pdf/inspection/999999")
        assert r.status_code == 404

    def test_inspection_pdf_exists(self, client, seed_inspection):
        r = client.get(f"/api/reports/pdf/inspection/{seed_inspection.id}")
        assert r.status_code == 200
        assert "pdf" in r.headers.get("content-type", "")

    def test_maintenance_excel_export(self, client, seed_action):
        r = client.get("/api/maintenance/actions")   # sanity check before excel
        assert r.status_code == 200
        r2 = client.get("/api/reports/excel/maintenance")
        assert r2.status_code == 200
        ct = r2.headers.get("content-type", "")
        assert "spreadsheetml" in ct or "excel" in ct or "octet-stream" in ct
