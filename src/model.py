import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class CropYieldLossModel:
    """
    LinearRegression model for predicting crop yield loss based on weather features.
    
    Features:
        - rainfall_pct: Percentage of rainfall (0-100)
        - heatwave_days: Number of days with heatwave conditions
        - dry_days: Number of dry days
        - humidity: Humidity percentage (0-100)
    """
    
    def __init__(self):
        """Initialize the LinearRegression model."""
        self.model = LinearRegression()
        self.features = ['rainfall_pct', 'heatwave_days', 'dry_days', 'humidity']
        self.is_fitted = False
    
    def fit(self, df):
        """
        Train the model on the provided dataframe.
        
        Args:
            df (pd.DataFrame): DataFrame containing features and target variable.
                              Must have columns: rainfall_pct, heatwave_days, dry_days, 
                              humidity, and a target column (yield_loss).
        
        Returns:
            self: Returns self for method chaining.
        """
        if 'yield_loss' not in df.columns:
            raise ValueError("DataFrame must contain 'yield_loss' column as target.")
        
        # Check if all required features are present
        missing_features = [f for f in self.features if f not in df.columns]
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
        
        # Extract features and target
        X = df[self.features].values
        y = df['yield_loss'].values
        
        # Train the model
        self.model.fit(X, y)
        self.is_fitted = True
        
        return self
    
    def predict(self, weather_dict):
        """
        Predict crop yield loss for given weather conditions.
        
        Args:
            weather_dict (dict): Dictionary containing weather features.
                                Example: {
                                    'rainfall_pct': 60,
                                    'heatwave_days': 15,
                                    'dry_days': 8,
                                    'humidity': 75
                                }
        
        Returns:
            float: Predicted yield loss value.
        
        Raises:
            ValueError: If model has not been fitted or required features are missing.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions.")
        
        # Check if all required features are present
        missing_features = [f for f in self.features if f not in weather_dict]
        if missing_features:
            raise ValueError(f"Missing required features in weather_dict: {missing_features}")
        
        # Extract feature values in the correct order
        X = np.array([[weather_dict[f] for f in self.features]])
        
        # Make prediction
        yield_loss = self.model.predict(X)[0]
        
        return yield_loss
    
    def get_coefficients(self):
        """
        Get the model coefficients for each feature.
        
        Returns:
            dict: Dictionary mapping feature names to their coefficients.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before accessing coefficients.")
        
        return {feature: coef for feature, coef in zip(self.features, self.model.coef_)}
    
    def get_intercept(self):
        """
        Get the model intercept.
        
        Returns:
            float: The intercept value.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before accessing intercept.")
        
        return self.model.intercept_


# Alias for compatibility
CropRiskModel = CropYieldLossModel
