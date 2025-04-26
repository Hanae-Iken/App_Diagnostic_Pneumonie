# api/prediction.py
import os
import sys
import numpy as np
from pathlib import Path
from tensorflow.keras.models import load_model

# Ajouter le répertoire racine au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.data_preprocessing import preprocess_image
from src.model.resnet50_model import get_last_conv_layer_name
from src.visualization.gradcam import make_gradcam_heatmap, get_img_array

class PneumoniaPredictor:
    def __init__(self, model_path=None):
        """
        Initialise le prédicteur de pneumonie.
        
        Args:
            model_path: Chemin vers le modèle entraîné
        """
        if model_path is None:
            model_path = os.path.join('models', 'resnet50_finetune.h5')
        
        self.model_path = model_path
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Charge le modèle de détection de pneumonie."""
        try:
            self.model = load_model(self.model_path)
            print(f"Modèle chargé depuis {self.model_path}")
        except Exception as e:
            print(f"Erreur lors du chargement du modèle: {e}")
            raise
    
    def predict(self, image_path):
        """
        Fait une prédiction sur une image.
        
        Args:
            image_path: Chemin vers l'image à analyser
            
        Returns:
            Classe prédite, confiance, heatmap
        """
        if self.model is None:
            raise ValueError("Le modèle n'est pas chargé.")
        
        # Prétraiter l'image
        img_array, _ = self.preprocess_image(image_path)
        
        # Prédiction
        prediction = self.model.predict(img_array)[0][0]
        predicted_class = "PNEUMONIE" if prediction > 0.5 else "NORMAL"
        confidence = prediction if prediction > 0.5 else 1 - prediction
        
        # Générer la heatmap Grad-CAM
        last_conv_layer = get_last_conv_layer_name(self.model)
        heatmap = make_gradcam_heatmap(img_array, self.model, last_conv_layer)
        
        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "heatmap": heatmap,
            "raw_prediction": prediction
        }
    
    def preprocess_image(self, image_path, target_size=(224, 224)):
        """
        Prétraite une image pour la prédiction.
        
        Args:
            image_path: Chemin vers l'image
            target_size: Taille cible pour le redimensionnement
            
        Returns:
            Image prétraitée pour le modèle
        """
        # Utilisez la fonction de prétraitement existante
        processed_img = preprocess_image(image_path, target_size)
        
        # Préparer pour le modèle (ajouter la dimension du batch)
        img_array = np.expand_dims(processed_img, axis=0)
        
        return img_array, processed_img

# Fonction d'utilité pour les tests
def test_predictor(image_path, model_path=None):
    """
    Teste le prédicteur sur une image spécifique.
    
    Args:
        image_path: Chemin vers l'image de test
        model_path: Chemin vers le modèle entraîné (optionnel)
    """
    predictor = PneumoniaPredictor(model_path)
    result = predictor.predict(image_path)
    
    print(f"Image: {image_path}")
    print(f"Classe prédite: {result['predicted_class']}")
    print(f"Confiance: {result['confidence']*100:.2f}%")
    print(f"Prédiction brute: {result['raw_prediction']:.4f}")
    
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_predictor(sys.argv[1])
    else:
        print("Usage: python prediction.py <chemin_image>")