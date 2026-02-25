def explain_risk(yield_loss, rainfall_pct, heatwave_days, dry_days, humidity):
    """
    Generate a human-readable explanation of crop risk based on yield loss prediction.
    
    Args:
        yield_loss (float): Predicted yield loss percentage (0-100).
        rainfall_pct (float): Percentage of normal rainfall (0-100).
        heatwave_days (int): Number of heatwave days.
        dry_days (int): Number of dry days.
        humidity (float): Humidity percentage (0-100).
    
    Returns:
        dict: Dictionary containing risk level and explanation.
              Keys: 'risk_level', 'yield_loss', 'explanation', 'recommendations'
    """
    
    # Determine risk level based on yield loss
    if yield_loss < 10:
        risk_level = "LOW"
        risk_emoji = "🟢"
    elif yield_loss < 30:
        risk_level = "MEDIUM"
        risk_emoji = "🟡"
    elif yield_loss < 60:
        risk_level = "HIGH"
        risk_emoji = "🔴"
    else:
        risk_level = "CRITICAL"
        risk_emoji = "⚫"
    
    # Build explanation
    risk_factors = []
    
    if rainfall_pct < 50:
        risk_factors.append(f"Low rainfall ({rainfall_pct:.1f}% of normal) is severely stressing crops")
    elif rainfall_pct < 75:
        risk_factors.append(f"Below-average rainfall ({rainfall_pct:.1f}% of normal) is affecting crop health")
    
    if heatwave_days > 15:
        risk_factors.append(f"Prolonged heatwave ({heatwave_days} days) is damaging crops")
    elif heatwave_days > 5:
        risk_factors.append(f"Heatwave conditions ({heatwave_days} days) are stressing plants")
    
    if dry_days > 10:
        risk_factors.append(f"Extended dry period ({dry_days} days) is causing water stress")
    elif dry_days > 5:
        risk_factors.append(f"Dry conditions ({dry_days} days) are affecting soil moisture")
    
    if humidity < 40:
        risk_factors.append(f"Low humidity ({humidity:.1f}%) is increasing evaporation stress")
    
    # Create recommendation based on risk factors
    recommendations = []
    if rainfall_pct < 60:
        recommendations.append("Implement or increase irrigation")
    if heatwave_days > 10:
        recommendations.append("Provide shade or cooling measures if possible")
    if dry_days > 10:
        recommendations.append("Use mulching to retain soil moisture")
    if not recommendations:
        recommendations.append("Continue normal crop management practices")
    
    # Build final explanation string
    if risk_factors:
        explanation = "Risk factors: " + "; ".join(risk_factors) + "."
    else:
        explanation = "Weather conditions are favorable for crop growth."
    
    return {
        'risk_level': risk_level,
        'risk_emoji': risk_emoji,
        'yield_loss': round(yield_loss, 2),
        'explanation': explanation,
        'recommendations': recommendations
    }
