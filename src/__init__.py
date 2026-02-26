"""
Crop Risk Predictor Package
Professional modular ML application
"""

__version__ = "1.0.0"
__author__ = "Maharashtra AgriTech"
__description__ = "IMD-validated crop yield loss prediction system"

from .model import CropRiskModel
from .data_gen import DISTRICTS, CROPS, get_current_weather
from .risk_logic import analyze_risk

__all__ = ['CropRiskModel', 'analyze_risk', 'DISTRICTS', 'CROPS']
