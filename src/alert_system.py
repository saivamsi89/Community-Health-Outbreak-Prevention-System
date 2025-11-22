# src/alert_system.py
import pandas as pd
from .risk_model import calculate_risk_score   # This is the key line!

def generate_alerts(df, threshold=65):
    # Calculate risk score using the function from risk_model.py
    df['risk_score'] = df.apply(calculate_risk_score, axis=1)
    
    # Add the sustained increase bonus (same logic as in risk_model)
    df['sustained_increase'] = (df['cases_7d_ma'] > df['reported_cases'].shift(7).rolling(7).mean() * 1.5)
    df.loc[df['sustained_increase'], 'risk_score'] += 30
    df['risk_score'] = df['risk_score'].clip(upper=100)

    # Assign alert levels
    df['alert_level'] = pd.cut(df['risk_score'],
                               bins=[0, 40, 65, 100],
                               labels=['Low', 'Moderate', 'High'])

    current = df.iloc[-1]
    print(f"\n=== COMMUNITY HEALTH ALERT SYSTEM ===")
    print(f"Date       : {current['date'].date()}")
    print(f"Risk Score : {current['risk_score']:.1f}/100")
    print(f"Alert Level: {current['alert_level']}")
    print(f"Reported Cases (7d avg): {current['cases_7d_ma']:.1f}")

    recommendations = [
        "Situation normal. Continue routine surveillance."
    ]
    if current['alert_level'] == 'Moderate':
        recommendations = [
            "Monitor closely for next 72 hours",
            "Increase community sampling rate",
            "Public awareness campaign on symptoms",
            "Prepare rapid response team"
        ]
    elif current['alert_level'] == 'High':
        recommendations = [
            "HIGH RISK: Immediate contact tracing required",
            "Activate mobile testing units in affected areas",
            "Issue public mask mandate & social distancing advisory",
            "Increase hospital bed & oxygen readiness",
            "Start school closure consideration"
        ]

    print("\nRecommended Interventions:")
    for r in recommendations:
        print("• " + r)
    
    return df