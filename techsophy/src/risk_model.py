# src/risk_model.py
import numpy as np
import pandas as pd

def calculate_risk_score(row):
    score = 0
    if row['is_anomaly']:
        score += 40
    if row['outbreak_cluster'] != -1:
        score += 25
    if row['temperature'] > 30 and row['humidity'] > 70:
        score += 15
    return min(score, 100)

def optimize_threshold(df, thresholds=range(30, 91, 5)):
    # Temporary risk score calculation for threshold tuning
    temp_df = df.copy()
    temp_df['risk_score'] = temp_df.apply(calculate_risk_score, axis=1)
    temp_df['sustained_increase'] = (temp_df['cases_7d_ma'] > temp_df['reported_cases'].shift(7).rolling(7).mean() * 1.5)
    temp_df.loc[temp_df['sustained_increase'], 'risk_score'] += 30
    temp_df['risk_score'] = temp_df['risk_score'].clip(upper=100)

    actual = temp_df['date'].dt.date.isin([
        pd.to_datetime('2022-05-30').date(),
        pd.to_datetime('2023-02-05').date(),
        pd.to_datetime('2023-12-06').date(),
        pd.to_datetime('2024-09-01').date(),
    ]).astype(int)

    best_f1 = 0
    best_thresh = 60
    for t in thresholds:
        pred = (temp_df['risk_score'] >= t).astype(int)
        tp = ((pred == 1) & (actual == 1)).sum()
        fp = ((pred == 1) & (actual == 0)).sum()
        fn = ((pred == 0) & (actual == 1)).sum()
        precision = tp / (tp + fp + 1e-6)
        recall = tp / (tp + fn + 1e-6)
        f1 = 2 * precision * recall / (precision + recall + 1e-6)
        if f1 > best_f1:
            best_f1 = f1
            best_thresh = t
    return best_thresh