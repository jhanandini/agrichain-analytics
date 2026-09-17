import pandas as pd
import numpy as np

def validate_farm_batch(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    required_cols = ['farm_id', 'region', 'commodity', 'land_size_acres', 'harvest_weight_kg']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required field: {col}")
            
    df['land_size_acres'] = pd.to_numeric(df['land_size_acres'], errors='coerce')
    df['harvest_weight_kg'] = pd.to_numeric(df['harvest_weight_kg'], errors='coerce')
    
    df = df.dropna(subset=['land_size_acres', 'harvest_weight_kg'])
    df = df[(df['land_size_acres'] > 0) & (df['harvest_weight_kg'] > 0)]
    
    # Calculate Yield per Acre Ratio
    df['yield_per_acre'] = df['harvest_weight_kg'] / df['land_size_acres']
    return df