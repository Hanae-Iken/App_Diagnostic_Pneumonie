import os
import sys
import numpy as np
import gradio as gr
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2

# Ajouter le répertoire parent au chemin Python
sys.path.append(os.path.abspath('..'))

from src.data.data_preprocessing import DataPreprocessor
from src.visualization.gradcam import GradCAM

# Charger le modèle
MODEL_PATH = '../models/resnet50_finetune.h5'
model = load_model(MODEL_PATH)

# Initialiser le préprocesseur
preprocessor = DataPreprocessor(target_size=(224, 224))

# Initialiser GradCAM
gradcam = GradCAM(model, "conv5_block3_out")

def predict_pneumonia(image):
    """
    Fonction qui prend une image, prédit la présence de pneumonie et génère une carte de chaleur.
    
    Args:
        image: Image à analyser (numpy array)
        
    Returns:
        tuple: (résultat textuel, probabilité, image originale, carte de chaleur, image avec carte de chaleur superposée)
    """
    # Prétraiter l'image
    if image.shape[2] == 4:  # Si l'image a un canal alpha (RGBA)
        image = image[:, :, :3]  # Convertir en RGB
    
    # Redimensionner l'image
    processed_image = preprocessor.preprocess_image(image)
    
    # Faire une prédiction
    img_batch = np.expand_dims(processed_image, axis=0)
    prediction = model.predict(img_batch)[0][0]
    
    # Générer la carte de chaleur GradCAM
    heatmap = gradcam.compute_heatmap(img_batch, pred_class=0 if prediction <= 0.5 else 1)
    cam_image = gradcam.overlay_heatmap(processed_image, heatmap, alpha=0.5)
    
    # Déterminer le résultat
    if prediction > 0.5:
        result = "Pneumonie détectée"
    else:
        result = "Pas de pneumonie détectée"
    
    # Convertir la carte de chaleur en image RGB pour l'affichage
    heatmap_rgb = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
    heatmap_rgb = cv2.cvtColor(heatmap_rgb, cv2.COLOR_BGR2RGB)
    
    return result, float(prediction), processed_image, heatmap_rgb, cam_image

# Définir l'interface Gradio
iface = gr.Interface(
    fn=predict_pneumonia,
    inputs=gr.Image(type="numpy"),
    outputs=[
        gr.Text(label="Résultat"),
        gr.Number(label="Probabilité de pneumonie"),
        gr.Image(label="Image prétraitée"),
        gr.Image(label="Carte de chaleur GradCAM"),
        gr.Image(label="Superposition GradCAM"),
    ],
    title="Détection de pneumonie par IA",
    description="Téléchargez une radiographie pulmonaire pour détecter la présence de pneumonie.",
    examples=[
        ["../data/raw/test/NORMAL/IM-0001-0001.jpeg"],
        ["../data/raw/test/PNEUMONIA/person1_bacteria_1.jpeg"]
    ],
    allow_flagging="never",
)

if __name__ == "__main__":
    iface.launch(share=True)