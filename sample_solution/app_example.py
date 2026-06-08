"""
app_example.py - Example FastAPI application
This shows how to build the prediction API endpoints.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
from typing import Optional

# Initialize FastAPI app
app = FastAPI(
    title="Lead Conversion Prediction API",
    description="Predicts lead conversion probability using behavioral data",
    version="1.0.0"
)

# Load trained model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Warning: model.pkl not found. Train model first with: python train.py")
    model = None

# ===== REQUEST/RESPONSE MODELS =====

class PredictionInput(BaseModel):
    """Input schema for /predict endpoint"""
    session_count: int
    total_interactions: int
    total_time_spent: float
    demo_requests: int
    pricing_views: int
    whatsapp_clicks: int
    email_opens: int
    source: str  # "Google", "Referral", "LinkedIn", etc.
    company_size: str  # "Small", "Medium", "Enterprise"
    segment: str  # "Startup", "SMB", "Enterprise", "Other"


class PredictionOutput(BaseModel):
    """Output schema for /predict endpoint"""
    conversion_probability: float
    confidence: str
    risk_level: str
    recommendation: str


class ExplanationInput(BaseModel):
    """Input schema for /explain endpoint"""
    conversion_probability: float
    demo_requests: int
    pricing_views: int
    session_count: int
    email_opens: int


class ExplanationOutput(BaseModel):
    """Output schema for /explain endpoint"""
    summary: str
    factors: list


# ===== HELPER FUNCTIONS =====

def prepare_features(input_data: PredictionInput) -> np.ndarray:
    """Convert input data to feature vector for model"""
    
    # Encode categorical variables
    source_map = {"Google": 0, "Referral": 1, "LinkedIn": 2, "Direct": 3, "Ads": 4}
    size_map = {"Small": 0, "Medium": 1, "Enterprise": 2}
    segment_map = {"Startup": 0, "SMB": 1, "Enterprise": 2, "Other": 3}
    
    source_encoded = source_map.get(input_data.source, 0)
    size_encoded = size_map.get(input_data.company_size, 1)
    segment_encoded = segment_map.get(input_data.segment, 3)
    
    # Create feature vector in same order as training
    features = [
        input_data.session_count,
        input_data.total_interactions,
        input_data.total_time_spent,
        input_data.demo_requests,
        input_data.pricing_views,
        input_data.whatsapp_clicks,
        input_data.email_opens,
        source_encoded,
        size_encoded,
        segment_encoded
    ]
    
    return np.array([features])


def get_confidence_level(probability: float) -> str:
    """Classify confidence based on probability"""
    if probability >= 0.75:
        return "high"
    elif probability >= 0.50:
        return "medium"
    else:
        return "low"


def get_risk_level(probability: float) -> str:
    """Classify risk level"""
    if probability >= 0.70:
        return "low"
    elif probability >= 0.40:
        return "medium"
    else:
        return "high"


def generate_explanation(input_data: ExplanationInput) -> tuple:
    """Generate human-readable explanation"""
    
    factors = []
    
    # Analyze high-intent signals
    if input_data.demo_requests > 0:
        factors.append("Demo request submitted (high intent)")
    
    if input_data.pricing_views >= 3:
        factors.append("Multiple pricing page visits (strong interest)")
    elif input_data.pricing_views >= 1:
        factors.append("Pricing page visited (moderate interest)")
    
    if input_data.session_count >= 5:
        factors.append("Multiple sessions indicate strong engagement")
    elif input_data.session_count >= 2:
        factors.append("Return visitor showing continued interest")
    
    if input_data.email_opens >= 3:
        factors.append("High email engagement")
    
    # Build summary
    if input_data.conversion_probability >= 0.75:
        if input_data.demo_requests > 0:
            summary = "This lead shows exceptional interest with a demo request and strong engagement across multiple sessions."
        else:
            summary = "This lead demonstrates high conversion likelihood through consistent engagement and pricing interest."
    
    elif input_data.conversion_probability >= 0.50:
        summary = "This lead shows moderate interest. Continued nurturing and engagement could improve conversion likelihood."
    
    else:
        summary = "This lead requires more engagement before conversion is likely. Focus on product education and use case alignment."
    
    return summary, factors


# ===== ENDPOINTS =====

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Lead Conversion Prediction API is running",
        "endpoints": ["/predict", "/explain", "/docs"]
    }


@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    """
    Predict lead conversion probability
    
    Example:
    ```json
    {
      "session_count": 4,
      "total_interactions": 15,
      "total_time_spent": 420.0,
      "demo_requests": 1,
      "pricing_views": 3,
      "whatsapp_clicks": 2,
      "email_opens": 5,
      "source": "Google",
      "company_size": "Medium",
      "segment": "SMB"
    }
    ```
    """
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Train model first.")
    
    try:
        # Prepare features
        features = prepare_features(input_data)
        
        # Get prediction
        probability = float(model.predict_proba(features)[0][1])
        
        # Classify confidence and risk
        confidence = get_confidence_level(probability)
        risk = get_risk_level(probability)
        
        # Generate recommendation
        if probability >= 0.70:
            recommendation = "Ready for sales outreach"
        elif probability >= 0.50:
            recommendation = "Nurture with targeted content"
        else:
            recommendation = "Focus on product education"
        
        return PredictionOutput(
            conversion_probability=round(probability, 2),
            confidence=confidence,
            risk_level=risk,
            recommendation=recommendation
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/explain", response_model=ExplanationOutput)
async def explain(input_data: ExplanationInput):
    """
    Get human-readable explanation of conversion prediction
    
    Example:
    ```json
    {
      "conversion_probability": 0.78,
      "demo_requests": 1,
      "pricing_views": 3,
      "session_count": 5,
      "email_opens": 4
    }
    ```
    """
    
    try:
        summary, factors = generate_explanation(input_data)
        
        return ExplanationOutput(
            summary=summary,
            factors=factors
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===== ERROR HANDLERS =====

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return HTTPException(status_code=400, detail=str(exc))


# ===== RUN =====
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
