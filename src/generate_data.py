# generate_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)
start_date = datetime(2022, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(1095)]  # 3 years daily data


def generate_data():
    # Start with integer columns so no FutureWarning
    df = pd.DataFrame({
        'date': dates,
        'reported_cases': np.random.poisson(lam=15, size=len(dates)).astype('float64'),
        'fever_reports': np.random.poisson(lam=30, size=len(dates)).astype('float64'),
        'hospital_visits': np.random.poisson(lam=50, size=len(dates)).astype('float64'),
        'temperature': 20 + 15 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365) + np.random.normal(0, 3, len(dates)),
        'humidity': 50 + 30 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365 + np.pi/2) + np.random.normal(0, 10, len(dates)),
        'population_mobility': np.random.gamma(10, 2, len(dates))
    })

    # Inject 4 realistic outbreaks (bigger spikes)
    outbreaks = [
        (150, 180, 5),    # ~May-June 2022
        (400, 420, 4),    # ~Feb 2023
        (700, 730, 6),    # ~Dec 2023 - Jan 2024
        (950, 970, 3.5)   # ~Aug-Sep 2024
    ]

    for start, end, multiplier in outbreaks:
        df.loc[start:end, 'reported_cases'] *= multiplier
        df.loc[start:end, 'fever_reports'] *= multiplier * 0.9
        df.loc[start:end, 'hospital_visits'] *= multiplier * 0.8

    # Round to realistic integers only at the end
    df['reported_cases'] = df['reported_cases'].round().astype(int)
    df['fever_reports'] = df['fever_reports'].round().astype(int)
    df['hospital_visits'] = df['hospital_visits'].round().astype(int)

    # Create data folder if not exists
    os.makedirs("data", exist_ok=True)
    
    df.to_csv('data/synthetic_health_data.csv', index=False)
    
    # Fixed arrow (uses plain ASCII)
    print("Synthetic data generated successfully -> data/synthetic_health_data.csv")


if __name__ == "__main__":
    generate_data()