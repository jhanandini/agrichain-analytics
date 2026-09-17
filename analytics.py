import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_yield_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    if len(df) < 3:
        df['is_fraudulent_yield'] = False
        return df
        
    # ML model to catch fake volume claims based on yield-to-area ratios
    model = IsolationForest(contamination=0.1, random_state=42)
    features = df[['land_size_acres', 'harvest_weight_kg', 'yield_per_acre']]
    
    # -1 indicates anomaly, 1 indicates normal
    predictions = model.fit_predict(features)
    df['is_fraudulent_yield'] = predictions == -1
    
    return df