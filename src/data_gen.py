import pandas as pd
import numpy as np


def generate_synthetic_data(num_samples=1000, seed=42):
    """
    Generate synthetic crop weather and yield loss data for training.
    
    Args:
        num_samples (int): Number of data samples to generate. Default is 1000.
        seed (int): Random seed for reproducibility. Default is 42.
    
    Returns:
        pd.DataFrame: DataFrame with features and target yield_loss.
                     Columns: rainfall_pct, heatwave_days, dry_days, humidity, yield_loss
    """
    np.random.seed(seed)
    
    # Generate synthetic weather features
    rainfall_pct = np.random.uniform(20, 100, num_samples)  # 20-100% of normal rainfall
    heatwave_days = np.random.randint(0, 30, num_samples)   # 0-30 days
    dry_days = np.random.randint(0, 20, num_samples)        # 0-20 days
    humidity = np.random.uniform(30, 95, num_samples)       # 30-95% humidity
    
    # Generate yield loss based on features with some noise
    # Lower rainfall and more heatwaves = higher yield loss
    yield_loss = (
        (100 - rainfall_pct) * 0.3 +      # Low rainfall increases loss
        heatwave_days * 1.5 +              # More heatwave days increase loss
        dry_days * 0.8 +                   # Dry days increase loss
        (100 - humidity) * 0.2 +           # Low humidity increases loss
        np.random.normal(0, 15, num_samples)  # Add noise
    )
    
    # Clip yield loss to realistic range [0, 100]
    yield_loss = np.clip(yield_loss, 0, 100)
    
    # Create DataFrame
    data = pd.DataFrame({
        'rainfall_pct': rainfall_pct,
        'heatwave_days': heatwave_days,
        'dry_days': dry_days,
        'humidity': humidity,
        'yield_loss': yield_loss
    })
    
    return data
