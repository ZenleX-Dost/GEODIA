import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest

def compute_insar_descriptors(points_data: list) -> list:
    """
    Compute derived descriptors for each InSAR point.
    Returns the points with added descriptors: cumul, acceleration, etc.
    """
    for pt in points_data:
        # Example logic for descriptors based on time series of displacements
        # In a real implementation, we would compute this from the actual TS data
        v = pt.get('vitesse_los', 0.0)
        pt['cumul'] = v * 5  # Mock 5-year accumulation
        pt['acceleration'] = 0.0
        pt['anomaly_score'] = 0.0
        pt['consensus_level'] = 0
    return points_data

def run_dbscan_clustering(points_data: list, eps=50, min_samples=3) -> list:
    """
    Run DBSCAN spatial clustering on InSAR points.
    """
    if not points_data:
        return []
        
    # Extract coords
    coords = np.array([[pt.get('lat', 0), pt.get('lon', 0)] for pt in points_data])
    
    # DBSCAN requires metric='haversine' for lat/lon, but keeping it simple for stub
    clustering = DBSCAN(eps=eps/111320.0, min_samples=min_samples).fit(coords)
    
    for i, pt in enumerate(points_data):
        pt['cluster_id'] = int(clustering.labels_[i])
        
    return points_data

def run_isolation_forest(points_data: list) -> list:
    """
    Run Multivariate Isolation Forest for anomaly detection.
    """
    if not points_data:
        return []
        
    features = np.array([[pt.get('vitesse_los', 0), pt.get('cumul', 0)] for pt in points_data])
    clf = IsolationForest(contamination=0.1, random_state=42)
    preds = clf.fit_predict(features)
    
    for i, pt in enumerate(points_data):
        # preds is -1 for outliers, 1 for inliers
        pt['is_anomaly_iso'] = bool(preds[i] == -1)
        
    return points_data

def evaluate_consensus(points_data: list) -> list:
    """
    Evaluate consensus voting: strong (3/3), medium (2/3), weak (1/3).
    Mocking 3 conditions: threshold, dbscan (cluster != -1), iso forest.
    """
    for pt in points_data:
        votes = 0
        if pt.get('vitesse_los', 0) < -5.0 or pt.get('cumul', 0) < -10.0:
            votes += 1
        if pt.get('cluster_id', -1) != -1:
            votes += 1
        if pt.get('is_anomaly_iso', False):
            votes += 1
            
        pt['consensus_level'] = votes
        
    return points_data

def execute_insar_pipeline(points_data: list) -> list:
    """
    Execute the full InSAR anomaly pipeline.
    """
    points = compute_insar_descriptors(points_data)
    points = run_dbscan_clustering(points)
    points = run_isolation_forest(points)
    points = evaluate_consensus(points)
    return points
