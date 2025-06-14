import numpy as np
import cv2
import tensorflow as tf
from PIL import Image
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import visualization module if needed
# from src.visualization.gradcam import GradCAM

class PneumoniaPredictor:
    def __init__(self, model_path, img_size=224):
        """
        Initialize the pneumonia predictor
        
        Args:
            model_path (str): Path to the trained model
            img_size (int): Size to which images will be resized
        """
        self.model = tf.keras.models.load_model(model_path)
        self.img_size = img_size
        self.class_names = ['NORMAL', 'PNEUMONIA']
        
    def preprocess_image(self, image):
        """
        Preprocess image for prediction
        
        Args:
            image (PIL.Image or numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Preprocessed image
        """
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
            
        # Convert to RGB if grayscale
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 1:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        
        # Resize image
        image = cv2.resize(image, (self.img_size, self.img_size))
        
        # Normalize pixel values to [0, 1]
        image = image / 255.0
        
        return image
    
    def predict(self, image):
        """
        Make prediction for an image
        
        Args:
            image (PIL.Image or numpy.ndarray): Input image
            
        Returns:
            dict: Prediction results
        """
        # Preprocess image
        processed_img = self.preprocess_image(image)
        
        # Add batch dimension
        input_img = np.expand_dims(processed_img, axis=0)
        
        # Make prediction
        predictions = self.model.predict(input_img)
        predicted_class_idx = np.argmax(predictions[0])
        predicted_class = self.class_names[predicted_class_idx]
        confidence = float(predictions[0][predicted_class_idx])
        
        # Generate GradCAM if needed
        # gradcam = GradCAM(self.model)
        # heatmap = gradcam.compute_heatmap(processed_img)
        
        # Return results
        result = {
            "prediction": predicted_class,
            "confidence": confidence,
            "probabilities": {
                self.class_names[i]: float(predictions[0][i])
                for i in range(len(self.class_names))
            }
        }
        
        return result