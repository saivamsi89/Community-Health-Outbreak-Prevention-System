# src/data_aggregator.py
import pandas as pd
import os

def load_and_prepare_data():
    path = os.path.join(os.path.dirname(__file__), "../data/synthetic_health_data.csv")
    if not os.path.exists(path):
        raise FileNotFoundError("Run generate_data.py first!")
    
    df = pd.read_csv(path, parse_dates=['date'])
    df = df.sort_values('date').reset_index(drop=True)
    
    # Feature engineering
    df['cases_7d_ma'] = df['reported_cases'].rolling(7, min_periods=1).mean()
    df['cases_change'] = df['reported_cases'].pct_change().fillna(0)
    
    return df