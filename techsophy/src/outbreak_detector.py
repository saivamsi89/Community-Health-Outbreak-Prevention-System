# src/outbreak_detector.py
import numpy as np
import pandas as pd
from prophet import Prophet
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

def forecast_with_prophet(df):
    prophet_df = df[['date', 'reported_cases']].rename(columns={'date': 'ds', 'reported_cases': 'y'})
    m = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    m.fit(prophet_df)
    future = m.make_future_dataframe(periods=14)
    forecast = m.predict(future)
    return forecast

def detect_anomalies(df, forecast):
    merged = df.merge(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], 
                     left_on='date', right_on='ds', how='left')
    
    merged['residual'] = merged['reported_cases'] - merged['yhat']
    merged['is_anomaly'] = merged['reported_cases'] > merged['yhat_upper']
    
    # Clustering on anomaly features
    features = merged[['residual', 'cases_change', 'temperature', 'humidity', 'population_mobility']]
    scaler = StandardScaler()
    X = scaler.fit_transform(features)
    
    clustering = DBSCAN(eps=0.7, min_samples=3).fit(X)
    merged['cluster'] = clustering.labels_
    
    # Cluster -1 = noise, ≥0 = potential outbreak groups
    merged['outbreak_cluster'] = merged['cluster'].apply(lambda x: x if x >= 0 else -1)
    
    return merged