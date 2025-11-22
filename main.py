# main.py
import os
from src.data_aggregator import load_and_prepare_data
from src.outbreak_detector import forecast_with_prophet, detect_anomalies
from src.risk_model import optimize_threshold
from src.alert_system import generate_alerts

if __name__ == "__main__":
    print("Starting Community Health Outbreak Prevention System...\n")
    
    df = load_and_prepare_data()
    forecast = forecast_with_prophet(df)
    df = detect_anomalies(df, forecast)
    
    # Optimize threshold on historical data
    optimal_thresh = optimize_threshold(df)
    print(f"Optimized alert threshold: {optimal_thresh}\n")
    
    # Generate final alerts
    df = generate_alerts(df, threshold=optimal_thresh)