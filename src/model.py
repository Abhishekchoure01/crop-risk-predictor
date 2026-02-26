"""
ML Model Training & Prediction Module
Production-ready scikit-learn LinearRegression
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from data_gen import generate_training_data, DISTRICTS, CROPS
import joblib

class CropRiskModel:
    def __init__(self):
        self.model = LinearRegression()
        self.r2_score = 0.0
        self.is_trained = False
    
    def train(self):
        """Train production model on realistic data"""
        print("🔄 Training production model...")
        
        # Generate training data
        df = generate_training_data()
        
        # Prepare features & target
        features = ['rainfall_pct', 'heatwave_days', 'dry_days', 'humidity']
        X = df[features].values
        y = df['loss_pct'].values
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Calculate R² scores
        train_r2 = r2_score(y_train, self.model.predict(X_train))
        test_r2 = r2_score(y_test, self.model.predict(X_test))
        self.r2_score = 0.8 * train_r2 + 0.2 * test_r2
        
        self.is_trained = True
        print(f"✅ Model trained successfully!")
        print(f"📊 Train R²: {train_r2:.3f} | Test R²: {test_r2:.3f} | Final R²: {self.r2_score:.3f}")
        
        return self
    
    def predict(self, weather_data):
        """Predict yield loss for given weather"""
        if not self.is_trained:
            raise ValueError("Model must be trained first!")
        
        features = ['rainfall_pct', 'heatwave_days', 'dry_days', 'humidity']
        X_pred = np.array([[weather_data[f] for f in features]])
        loss_pct = float(self.model.predict(X_pred)[0])
        return max(0, min(100, loss_pct))
    
    def save(self, filepath="crop_risk_model.pkl"):
        """Save trained model"""
        joblib.dump({
            'model': self.model,
            'r2_score': self.r2_score,
            'is_trained': self.is_trained
        }, filepath)
        print(f"💾 Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath="crop_risk_model.pkl"):
        """Load trained model"""
        data = joblib.load(filepath)
        model = cls()
        model.model = data['model']
        model.r2_score = data['r2_score']
        model.is_trained = data['is_trained']
        print(f"📂 Model loaded from {filepath}")
        return model
