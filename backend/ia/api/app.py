import os
import io
import numpy as np
import cv2
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from PIL import Image

# Import prediction module
from prediction import PneumoniaPredictor

app = FastAPI(
    title="Pneumonia Detection API",
    description="API for detecting pneumonia from X-ray images",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor
model_path = "../models/resnet50_finetune.h5"
predictor = PneumoniaPredictor(model_path)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pneumonia Detection API"}

@app.post("/predict/")
async def predict_pneumonia(file: UploadFile = File(...)):
    """
    Predicts whether the uploaded X-ray image shows pneumonia
    
    Args:
        file: Uploaded X-ray image
    
    Returns:
        JSON with prediction results
    """
    try:
        # Read and process the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Make prediction
        result = predictor.predict(image)
        
        return result
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"An error occurred: {str(e)}"}
        )

@app.get("/health/")
def health_check():
    """API health check"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)