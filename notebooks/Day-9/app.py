from fastapi import FastAPI, HTTPException
from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION

app = FastAPI(
title=“Insurance Premium Prediction API”,
description=“Predict insurance premium category using Machine Learning”,
version=MODEL_VERSION
)

@app.get(”/”)
def home():
return {
“message”: “Insurance Premium Prediction API is running 🚀”
}

@app.get(”/health”)
def health_check():
return {
“status”: “OK”,
“version”: MODEL_VERSION,
“model_loaded”: model is not None
}

@app.post(
“/predict”,
response_model=PredictionResponse
)
def predict_premium(data: UserInput):

try:
    user_input = {
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }
    result = predict_output(user_input)
    return PredictionResponse(
        predicted_category=result["predicted_category"],
        confidence=result["confidence"],
        class_probabilities=result["class_probabilities"]
    )
except Exception as e:
    raise HTTPException(
        status_code=500,
        detail=f"Prediction failed: {str(e)}"
    )