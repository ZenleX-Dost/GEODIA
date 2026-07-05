import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000/api"

def print_header(title):
    print("\n" + "="*50)
    print(f"--- {title} ---")
    print("="*50)

def print_result(step, success, details=""):
    status = "PASS" if success else "FAIL"
    print(f"[{status}] | {step}")
    if details:
        print(f"   > {details}")

def run_tests():
    print_header("GEODIA END-TO-END SCENARIO TESTS")
    
    # ---------------------------------------------------------
    # SCENARIO 1: Basic Assets Check
    # ---------------------------------------------------------
    print_header("SCENARIO 1: Basic Data Integrity")
    resp = requests.get(f"{BASE_URL}/assets")
    ouvrages = resp.json()
    success = resp.status_code == 200 and len(ouvrages) > 0
    print_result("Fetch Ouvrages", success, f"Found {len(ouvrages)} structures.")
    
    if not success:
        return
        
    target_ouvrage_id = ouvrages[0]["id"]
    
    # ---------------------------------------------------------
    # SCENARIO 2: InSAR ML Pipeline
    # ---------------------------------------------------------
    print_header("SCENARIO 2: Satellite InSAR Deformation")
    resp = requests.post(f"{BASE_URL}/insar/recompute")
    success = resp.status_code == 200
    print_result("Run InSAR Pipeline", success, resp.json().get("message", ""))
    
    resp = requests.get(f"{BASE_URL}/insar/anomalies")
    success = resp.status_code == 200
    if success:
        anomalies = resp.json()
        print_result("Fetch Anomalies", True, f"Detected {len(anomalies)} anomalies (Consensus >= 2).")
    else:
        print_result("Fetch Anomalies", False, f"Status {resp.status_code}: {resp.text}")

    # ---------------------------------------------------------
    # SCENARIO 3: Environmental API Sync
    # ---------------------------------------------------------
    print_header("SCENARIO 3: Environmental Aggressiveness (IAE)")
    resp = requests.post(f"{BASE_URL}/env/sync")
    success = resp.status_code == 200
    print_result("Sync NASA Earthdata", success, resp.json().get("message", ""))
    
    # ---------------------------------------------------------
    # SCENARIO 4: Dynamic Probabilistic Model (CDC Logistic)
    # ---------------------------------------------------------
    print_header("SCENARIO 4: Risk Recalculation")
    resp = requests.get(f"{BASE_URL}/compute/proba/matrix")
    matrix = resp.json()
    success = resp.status_code == 200 and len(matrix) > 0
    print_result("Fetch Probability Matrix", success, f"Matrix calculated for {len(matrix)} structures.")
    
    if success:
        target_matrix = next((m for m in matrix if m["ouvrage_id"] == target_ouvrage_id), None)
        if target_matrix:
            probs = target_matrix["probabilities"]
            p_values = list(probs.values())
            is_valid = all(0 <= p <= 100 for p in p_values)
            print_result("Verify Probability Bounds (0-100%)", is_valid, f"Values range: {min(p_values):.1f}% to {max(p_values):.1f}%")
            
            # Print a specific high risk pathology
            highest_p = max(probs, key=probs.get)
            print_result("Identify Critical Pathology", True, f"{highest_p} has maximum risk of {probs[highest_p]:.1f}%.")

    # ---------------------------------------------------------
    # SCENARIO 5: Budget Optimization (Prescriptive Maintenance)
    # ---------------------------------------------------------
    print_header("SCENARIO 5: Prescriptive AI (Budget Allocation)")
    budget = 500000 # 500,000 DH
    payload = {
        "scenario_id": "budget_restricted_q3",
        "budget": budget,
        "objectives": ["risk_reduction"]
    }
    resp = requests.post(f"{BASE_URL}/compute/optimize", json=payload)
    success = resp.status_code == 200
    opt_data = resp.json()
    if success:
        cost = opt_data.get("total_cost", 0)
        selected = len(opt_data.get("selected_actions_ids", []))
        is_under_budget = cost <= budget
        print_result("Run Knapsack Optimization", is_under_budget, f"Selected {selected} actions. Cost: {cost:,} DH / {budget:,} DH")
    else:
        print_result("Run Knapsack Optimization", False, resp.text)
        
    print_header("TEST RUN COMPLETED")

if __name__ == "__main__":
    try:
        run_tests()
    except requests.exceptions.ConnectionError:
        print("❌ CRITICAL ERROR: Could not connect to API. Is the FastAPI server running on http://127.0.0.1:8000?")
