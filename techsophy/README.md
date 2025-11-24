# Community Health Outbreak Prevention System

An early warning system that detects disease outbreaks using time-series forecasting, anomaly detection, clustering, and risk scoring.

## Features
- Prophet-based forecasting with seasonality
- Anomaly detection + DBSCAN clustering of outbreak patterns
- Dynamic risk scoring with environmental factors
- Optimized alert thresholds (Precision-Recall)
- Actionable prevention recommendations

## Quick Start
```bash
pip install -r requirements.txt
python generate_data.py
python main.py