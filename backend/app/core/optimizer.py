from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value
from typing import List, Dict

def run_budget_optimization(actions: List[Dict], budget_max: float, scenario: str) -> Dict:
    """
    Run PuLP budget optimization for maintenance actions.
    - S1 (économique): pure optimization
    - S2 (équilibré): force all class A critical actions
    - S3 (sécurité max): no compromise on high-gain actions
    
    actions format: [{'id': 1, 'ouvrage_id': 10, 'cost': 50000, 'risk_gain': 0.8, 'is_class_a_critical': True}]
    """
    prob = LpProblem("Maintenance_Optimization", LpMaximize)
    
    # Decision variables: x[i] = 1 if action is selected, 0 otherwise
    action_vars = {}
    for a in actions:
        action_vars[a['id']] = LpVariable(f"x_{a['id']}", cat='Binary')
        
    # Objective function: maximize total risk reduction
    prob += lpSum([a['risk_gain'] * action_vars[a['id']] for a in actions]), "Total_Risk_Gain"
    
    # Constraint 1: Budget limit
    prob += lpSum([a['cost'] * action_vars[a['id']] for a in actions]) <= budget_max, "Budget_Constraint"
    
    # Scenario constraints
    if scenario in ['S2', 'S3']:
        # Force all critical class A actions
        for a in actions:
            if a.get('is_class_a_critical', False):
                prob += action_vars[a['id']] == 1, f"Force_ClassA_Critical_{a['id']}"
                
    if scenario == 'S3':
        for a in actions:
            if a.get('is_class_a_high', False):
                prob += action_vars[a['id']] == 1, f"Force_ClassA_High_{a['id']}"
                
    # Solve
    prob.solve()
    
    status = LpStatus[prob.status]
    
    selected_actions = []
    total_cost = 0
    total_gain = 0
    
    for a in actions:
        if action_vars[a['id']].varValue == 1.0:
            selected_actions.append(a['id'])
            total_cost += a['cost']
            total_gain += a['risk_gain']
            
    return {
        "status": status,
        "selected_actions": selected_actions,
        "total_cost": total_cost,
        "total_gain": total_gain,
        "scenario": scenario,
        "budget_used_pct": (total_cost / budget_max * 100) if budget_max > 0 else 0
    }
