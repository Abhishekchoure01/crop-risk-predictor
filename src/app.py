import gradio as gr
import numpy as np
from src.model import CropRiskModel
from src.risk_logic import explain_risk


def create_gradio_app(model=None):
    """
    Create a Gradio interface for the Crop Risk Prediction system.
    
    Args:
        model (CropRiskModel, optional): Pre-trained CropRiskModel instance.
                                        If None, a new untrained model is created.
    
    Returns:
        gr.Blocks: A Gradio Blocks application object.
    """
    
    if model is None:
        model = CropRiskModel()
    
    def predict_risk(rainfall_pct, heatwave_days, dry_days, humidity):
        """Predict crop risk from weather inputs."""
        try:
            # Prepare input dictionary
            weather = {
                'rainfall_pct': float(rainfall_pct),
                'heatwave_days': int(heatwave_days),
                'dry_days': int(dry_days),
                'humidity': float(humidity)
            }
            
            # Make prediction
            if not model.is_fitted:
                return "⚠️ Error: Model not trained yet. Please train the model first."
            
            yield_loss = model.predict(weather)
            
            # Get risk explanation
            risk_info = explain_risk(
                yield_loss,
                weather['rainfall_pct'],
                weather['heatwave_days'],
                weather['dry_days'],
                weather['humidity']
            )
            
            # Format output
            output = f"""
            {risk_info['risk_emoji']} **Risk Level: {risk_info['risk_level']}**
            
            **Predicted Yield Loss:** {risk_info['yield_loss']}%
            
            **Analysis:**
            {risk_info['explanation']}
            
            **Recommendations:**
            - {chr(10).join(f"- {rec}" for rec in risk_info['recommendations'])}
            """
            
            return output
        
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    # Create Gradio interface
    with gr.Blocks(title="Crop Risk Predictor") as app:
        gr.Markdown("# 🌾 Crop Risk Prediction System")
        gr.Markdown("Predict crop yield loss based on weather conditions")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Weather Input")
                rainfall = gr.Slider(
                    minimum=0,
                    maximum=150,
                    value=75,
                    step=5,
                    label="Rainfall (% of normal)"
                )
                heatwave = gr.Slider(
                    minimum=0,
                    maximum=30,
                    value=10,
                    step=1,
                    label="Heatwave Days"
                )
                dry = gr.Slider(
                    minimum=0,
                    maximum=30,
                    value=5,
                    step=1,
                    label="Dry Days"
                )
                humidity = gr.Slider(
                    minimum=20,
                    maximum=100,
                    value=65,
                    step=5,
                    label="Humidity (%)"
                )
            
            with gr.Column():
                gr.Markdown("### Risk Assessment")
                predict_btn = gr.Button("🔍 Assess Risk", variant="primary")
                output = gr.Markdown("Enter weather data and click 'Assess Risk'")
        
        # Connect inputs to prediction function
        predict_btn.click(
            fn=predict_risk,
            inputs=[rainfall, heatwave, dry, humidity],
            outputs=output
        )
        
        gr.Markdown(
            """
            ### How it works:
            - **Rainfall**: Enter as percentage of normal (e.g., 50% means half the normal rainfall)
            - **Heatwave Days**: Number of consecutive hot days
            - **Dry Days**: Number of days without precipitation
            - **Humidity**: Current air humidity percentage
            
            The system predicts crop yield loss and provides risk assessment with recommendations.
            """
        )
    
    return app


if __name__ == "__main__":
    app = create_gradio_app()
    app.launch()
