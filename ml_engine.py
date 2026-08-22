import numpy as np
from sklearn.ensemble import IsolationForest

class YieldAnomalyDetector:
    def __init__(self):
        # Isolation Forest model initialized
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self._train_baseline_model()

    def _train_baseline_model(self):
        # Baseline training data: Realistic yield ratios (quintals per acre)
        # Average organic yield ranges between 15 to 40 quintals per acre
        np.random.seed(42)
        normal_yields = np.random.uniform(10.0, 45.0, (100, 1))
        
        # Train model on realistic yields
        self.model.fit(normal_yields)

    def verify_yield(self, land_area_acres: float, harvest_weight_quintals: float) -> dict:
        """
        Verifies if the submitted yield is realistic or anomalous.
        """
        if land_area_acres <= 0:
            return {"status": "REJECTED", "reason": "Land area must be greater than zero."}

        yield_ratio = harvest_weight_quintals / land_area_acres
        
        # Predict using Isolation Forest: 1 = Normal, -1 = Anomaly
        prediction = self.model.predict([[yield_ratio]])[0]
        
        if prediction == -1 or yield_ratio > 50.0:
            return {
                "status": "FLAGGED",
                "yield_ratio": round(yield_ratio, 2),
                "reason": f"Unusually high yield ratio ({round(yield_ratio, 2)} q/acre) detected!"
            }
        
        return {
            "status": "PASS",
            "yield_ratio": round(yield_ratio, 2),
            "reason": "Yield ratio is within realistic agricultural thresholds."
        }

# Quick Test Run
if __name__ == "__main__":
    detector = YieldAnomalyDetector()
    
    # Test 1: Normal batch
    test1 = detector.verify_yield(land_area_acres=2.0, harvest_weight_quintals=50.0)
    print("Test 1 (Normal):", test1)

    # Test 2: Fake/Exaggerated batch
    test2 = detector.verify_yield(land_area_acres=1.0, harvest_weight_quintals=500.0)
    print("Test 2 (Fraudulent):", test2)