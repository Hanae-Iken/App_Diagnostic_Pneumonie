# Guide d'utilisation de l'API de détection de pneumonie

Ce document explique comment utiliser l'API de détection de pneumonie pour intégrer la fonctionnalité de détection dans vos applications.

## Configuration requise

- Python 3.7+
- Accès à un serveur exécutant l'API (ou installation locale)
- Client HTTP capable d'envoyer des requêtes multipart/form-data

## Points d'accès (Endpoints)

L'API propose plusieurs endpoints pour répondre à différents besoins.

### 1. Détection de pneumonie

**Endpoint** : `/predict`  
**Méthode** : POST  
**Format de la requête** : multipart/form-data  
**Paramètres** :
- `image` : Fichier image (radiographie pulmonaire) - formats acceptés : JPEG, PNG, DICOM

**Exemple de requête avec cURL** :
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "image=@chemin/vers/radiographie.jpg"
```

**Exemple de réponse** :
```json
{
  "prediction": "PNEUMONIA",
  "probability": 0.9652,
  "processing_time": 0.654
}
```

### 2. Détection avec visualisation GradCAM

**Endpoint** : `/predict_with_gradcam`  
**Méthode** : POST  
**Format de la requête** : multipart/form-data  
**Paramètres** :
- `image` : Fichier image (radiographie pulmonaire) - formats acceptés : JPEG, PNG, DICOM

**Exemple de requête avec cURL** :
```bash
curl -X POST "http://localhost:8000/predict_with_gradcam" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "image=@chemin/vers/radiographie.jpg" \
     -o response_with_images.json
```

**Exemple de réponse** :
```json
{
  "prediction": "PNEUMONIA",
  "probability": 0.9652,
  "processing_time": 0.842,
  "gradcam_image": "base64_encoded_image_string",
  "overlay_image": "base64_encoded_image_string"
}
```

### 3. Vérification de l'état du service

**Endpoint** : `/health`  
**Méthode** : GET  
**Description** : Vérifie si l'API fonctionne correctement

**Exemple de requête avec cURL** :
```bash
curl -X GET "http://localhost:8000/health"
```

**Exemple de réponse** :
```json
{
  "status": "ok",
  "version": "1.0.0",
  "model_loaded": true
}
```

## Intégration dans une application

### Exemple Python avec requests

```python
import requests
import json
import base64
from PIL import Image
import io
import matplotlib.pyplot as plt

# URL de l'API
API_URL = "http://localhost:8000"

# Chemin vers l'image à analyser
image_path = "path/to/chest_xray.jpg"

# Envoi de la requête
with open(image_path, "rb") as image_file:
    files = {"image": image_file}
    response = requests.post(f"{API_URL}/predict_with_gradcam", files=files)

# Traitement de la réponse
if response.status_code == 200:
    result = response.json()
    
    # Afficher les résultats
    print(f"Prédiction: {result['prediction']}")
    print(f"Probabilité: {result['probability']:.2f}")
    
    # Afficher l'image GradCAM si elle existe
    if 'gradcam_image' in result:
        # Décoder l'image base64
        gradcam_bytes = base64.b64decode(result['gradcam_image'])
        gradcam_img = Image.open(io.BytesIO(gradcam_bytes))
        
        # Afficher l'image
        plt.figure(figsize=(10, 8))
        plt.imshow(gradcam_img)
        plt.title(f"GradCAM - Prédiction: {result['prediction']} ({result['probability']:.2f})")
        plt.axis('off')
        plt.show()
else:
    print(f"Erreur: {response.status_code}")
    print(response.text)
```

### Exemple JavaScript/HTML

```html
<!DOCTYPE html>
<html>
<head>
    <title>Détection de Pneumonie</title>
    <script>
        async function detectPneumonia() {
            const fileInput = document.getElementById('xrayImage');
            const resultDiv = document.getElementById('result');
            const gradcamDiv = document.getElementById('gradcam');
            
            if (!fileInput.files || fileInput.files.length === 0) {
                alert('Veuillez sélectionner une image');
                return;
            }
            
            const formData = new FormData();
            formData.append('image', fileInput.files[0]);
            
            resultDiv.innerHTML = 'Analyse en cours...';
            gradcamDiv.innerHTML = '';
            
            try {
                const response = await fetch('http://localhost:8000/predict_with_gradcam', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    resultDiv.innerHTML = `
                        <h3>Résultat:</h3>
                        <p>Prédiction: ${data.prediction}</p>
                        <p>Probabilité: ${(data.probability * 100).toFixed(2)}%</p>
                    `;
                    
                    if (data.overlay_image) {
                        gradcamDiv.innerHTML = `
                            <h3>Visualisation GradCAM:</h3>
                            <img src="data:image/jpeg;base64,${data.overlay_image}" 
                                 alt="GradCAM Visualization" 
                                 style="max-width: 100%;">
                        `;
                    }
                } else {
                    resultDiv.innerHTML = `Erreur: ${data.detail || 'Une erreur est survenue'}`;
                }
            } catch (error) {
                resultDiv.innerHTML = `Erreur: ${error.message}`;
            }
        }
    </script>
</head>
<body>
    <h1>Détection de Pneumonie par IA</h1>
    
    <div>
        <label for="xrayImage">Sélectionner une radiographie pulmonaire:</label>
        <input type="file" id="xrayImage" accept="image/*">
        <button onclick="detectPneumonia()">Analyser</button>
    </div>
    
    <div id="result" style="margin-top: 20px;"></div>
    <div id="gradcam" style="margin-top: 20px;"></div>
</body>
</html>
```

## Considérations et bonnes pratiques

1. **Limites de taille**: L'API limite les fichiers à 10 Mo maximum
2. **Formats d'image**: JPEG et PNG sont recommandés pour des temps de traitement optimaux
3. **Sécurité**: Utilisez HTTPS en production pour protéger les données médicales
4. **Mise en cache**: Évitez de mettre en cache les résultats, car chaque radiographie est unique
5. **Gestion des erreurs**: Implémentez une gestion robuste des erreurs dans votre application cliente

## Dépannage

| Problème | Solution possible |
|----------|-------------------|
| 413 Request Entity Too Large | Réduisez la taille de l'image ou augmentez la limite côté serveur |
| 415 Unsupported Media Type | Vérifiez que le format de l'image est supporté (JPEG, PNG, DICOM) |
| 500 Internal Server Error | Consultez les logs du serveur pour plus de détails |
| Problème de connexion | Vérifiez que le serveur API est en cours d'exécution et accessible |

Pour toute autre question ou problème, veuillez contacter l'équipe de support.