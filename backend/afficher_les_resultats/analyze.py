from flask import Blueprint, request, jsonify
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision import models
import os

analyze_bp = Blueprint('analyze_bp', __name__)

# Charger le modèle pré-entraîné
model = models.resnet18(pretrained=True)
model.eval()

# Prétraitement de l'image
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

@analyze_bp.route('/analyze', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    file = request.files['file']
    image = Image.open(file).convert('RGB')  # si PNG/JPG

    # Appliquer les transformations
    input_tensor = transform(image).unsqueeze(0)  # batch size 1

    # Inférence
    with torch.no_grad():
        output = model(input_tensor)
        probability = torch.nn.functional.softmax(output[0], dim=0)
        confidence, predicted_class = torch.max(probability, 0)

    return jsonify({
        "diagnostic": f"Classe {predicted_class.item()}",
        "probability": round(confidence.item(), 4)
    }), 200
