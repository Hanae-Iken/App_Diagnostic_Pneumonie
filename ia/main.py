# main.py - Script principal pour tester le projet
import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Ajouter le répertoire racine au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.data_preprocessing import preprocess_image
from src.model.resnet50_model import get_last_conv_layer_name
from src.visualization.gradcam import make_gradcam_heatmap, display_gradcam

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Test le modèle de détection de pneumonie')
    parser.add_argument('--image', type=str, required=True, help='Chemin vers l\'image de test')
    parser.add_argument('--model', type=str, default='models/resnet50_finetune.h5', 
                        help='Chemin vers le modèle entraîné')
    parser.add_argument('--output', type=str, default='output', 
                        help='Répertoire de sortie pour les résultats')
    return parser.parse_args()

def load_and_preprocess_image(image_path, target_size=(224, 224)):
    """Charge et prétraite une image pour la prédiction."""
    # Prétraiter l'image
    processed_img = preprocess_image(image_path, target_size)
    
    # Préparer pour le modèle (ajouter la dimension du batch)
    img_array = np.expand_dims(processed_img, axis=0)
    
    return img_array, processed_img

def predict_pneumonia(model, img_array):
    """Fait une prédiction sur l'image."""
    # Prédire
    prediction = model.predict(img_array)[0][0]
    
    # Interpréter la prédiction (pour une classification binaire)
    predicted_class = "PNEUMONIE" if prediction > 0.5 else "NORMAL"
    confidence = prediction if prediction > 0.5 else 1 - prediction
    
    return predicted_class, confidence

def main():
    # Analyser les arguments
    args = parse_arguments()
    
    # Créer le répertoire de sortie
    os.makedirs(args.output, exist_ok=True)
    
    # Charger le modèle
    print(f"Chargement du modèle depuis {args.model}...")
    model = load_model(args.model)
    
    # Charger et prétraiter l'image
    print(f"Prétraitement de l'image {args.image}...")
    img_array, processed_img = load_and_preprocess_image(args.image)
    
    # Faire une prédiction
    print("Prédiction en cours...")
    predicted_class, confidence = predict_pneumonia(model, img_array)
    
    # Générer la carte de chaleur Grad-CAM
    print("Génération de la carte de chaleur Grad-CAM...")
    last_conv_layer = get_last_conv_layer_name(model)
    heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer)
    
    # Afficher et sauvegarder la visualisation Grad-CAM
    cam_path = os.path.join(args.output, 'gradcam_result.jpg')
    superimposed_img = display_gradcam(args.image, heatmap, cam_path)
    
    # Afficher les résultats
    print("\nRésultats de l'analyse:")
    print(f"Classe prédite: {predicted_class}")
    print(f"Confiance: {confidence*100:.2f}%")
    print(f"Visualisation Grad-CAM sauvegardée à: {cam_path}")
    
    # Sauvegarder les résultats dans un fichier texte
    results_path = os.path.join(args.output, 'results.txt')
    with open(results_path, 'w') as f:
        f.write(f"Image: {args.image}\n")
        f.write(f"Classe prédite: {predicted_class}\n")
        f.write(f"Confiance: {confidence*100:.2f}%\n")
        f.write(f"Modèle utilisé: {args.model}")
    
    print(f"Résultats sauvegardés dans: {results_path}")

if __name__ == "__main__":
    main()