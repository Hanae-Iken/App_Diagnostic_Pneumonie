# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse
# import tensorflow as tf
# import numpy as np
# import cv2
# import io
# import sys
# import os
# import base64
# from PIL import Image

# # Ajout du chemin parent pour importer src
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from src.visualization.gradcam import make_gradcam_heatmap

# app = FastAPI(title="API de détection de pneumonie", 
#               description="Détecte la pneumonie à partir de radiographies pulmonaires")

# # Charger le modèle ResNet50
# model_path = '../models/resnet50_finetune.h5'
# model = tf.keras.models.load_model(model_path)

# # Dernière couche de convolution pour Grad-CAM
# last_conv_layer_name = None
# for layer in model.layers:
#     if 'conv' in layer.name:
#         last_conv_layer_name = layer.name

# def preprocess_image(image_bytes):
#     """Prétraite l'image téléchargée pour la prédiction."""
#     # Convertir les bytes en image
#     image = Image.open(io.BytesIO(image_bytes))
#     image = image.convert('RGB')
    
#     # Convertir en tableau numpy
#     image = np.array(image)
    
#     # Redimensionner et normaliser pour ResNet50
#     image = cv2.resize(image, (224, 224))
#     image = image / 255.0
    
#     return image

# def generate_heatmap(image, model, last_conv_layer_name):
#     """Génère une carte de chaleur Grad-CAM."""
#     # Préparation pour le modèle
#     img_array = np.expand_dims(image, axis=0)
    
#     # Générer la carte de chaleur
#     heatmap = make_gradcam_heatmap(img_array, model, last_conv_layer_name)
    
#     # Convertir en échelle de couleurs
#     heatmap = np.uint8(255 * heatmap)
#     heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
#     heatmap = cv2.resize(heatmap, (224, 224))
    
#     # Superposer sur l'image originale
#     superimposed_img = heatmap * 0.4 + (image * 255).astype('uint8')
#     superimposed_img = np.clip(superimposed_img, 0, 255).astype('uint8')
    
#     # Convertir en base64 pour le retour API
#     _, buffer = cv2.imencode('.jpg', superimposed_img)
#     img_str = base64.b64encode(buffer).decode('utf-8')
    
#     return img_str

# @app.post("/predict")
# async def predict(file: UploadFile = File(...)):
#     """Prédit la probabilité de pneumonie à partir d'une radiographie pulmonaire."""
#     # Lire le fichier image
#     image_bytes = await file.read()
    
#     # Prétraiter l'image
#     image = preprocess_image(image_bytes)
    
#     # Prédiction
#     img_array = np.expand_dims(image, axis=0)
#     prediction = model.predict(img_array)[0][0]
    
#     # Générer la carte de chaleur
#     heatmap_img = generate_heatmap(image, model, last_conv_layer_name)
    
#     # Classification
#     result = "PNEUMONIE" if prediction > 0.5 else "NORMAL"
#     confidence = float(prediction) if result == "PNEUMONIE" else float(1 - prediction)
    
#     return JSONResponse({
#         "prediction": result,
#         "confidence": confidence * 100,  # Pourcentage
#         "heatmap": heatmap_img
#     })

# @app.get("/")
# def read_root():
#     return {"message": "API de détection de pneumonie. Utilisez /predict pour analyser une radiographie."}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# api/app.py - Interface graphique pour l'application
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pathlib import Path
import threading
import datetime

# Ajouter le répertoire racine au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tensorflow.keras.models import load_model
from src.data.data_preprocessing import preprocess_image
from src.model.resnet50_model import get_last_conv_layer_name
from src.visualization.gradcam import make_gradcam_heatmap

class PneumoniaDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Détection de Pneumonie par IA")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.image_path = None
        self.model = None
        self.history = []
        
        # Chargement du modèle en arrière-plan
        self.load_model_thread = threading.Thread(target=self.load_model)
        self.load_model_thread.daemon = True
        self.load_model_thread.start()
        
        # Interface graphique
        self.setup_ui()
    
    def load_model(self):
        """Charge le modèle en arrière-plan."""
        try:
            model_path = os.path.join('models', 'resnet50_finetune.h5')
            self.model = load_model(model_path)
            self.status_label.config(text="Modèle chargé avec succès!")
        except Exception as e:
            self.status_label.config(text=f"Erreur lors du chargement du modèle: {e}")
    
    def setup_ui(self):
        """Configure l'interface utilisateur."""
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre
        title_label = tk.Label(main_frame, text="Système de Détection de Pneumonie",
                              font=("Arial", 18, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)
        
        # Frame pour l'image et les résultats
        content_frame = tk.Frame(main_frame, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame gauche pour l'image originale
        self.left_frame = tk.LabelFrame(content_frame, text="Image Originale", bg="#f0f0f0", 
                                 font=("Arial", 12))
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Placeholder pour l'image
        self.image_label = tk.Label(self.left_frame, bg="#ffffff", 
                               text="Aucune image sélectionnée\nCliquez sur 'Charger une image'",
                               height=20, width=40)
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame droit pour les résultats et la carte de chaleur
        self.right_frame = tk.LabelFrame(content_frame, text="Résultats d'Analyse", bg="#f0f0f0",
                                  font=("Arial", 12))
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame pour la carte de chaleur
        self.heatmap_frame = tk.Frame(self.right_frame, bg="#ffffff")
        self.heatmap_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Label pour les résultats
        self.result_frame = tk.Frame(self.right_frame, bg="#f0f0f0")
        self.result_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Labels pour afficher les résultats
        self.prediction_label = tk.Label(self.result_frame, text="Prédiction: -", 
                                   font=("Arial", 14), bg="#f0f0f0")
        self.prediction_label.pack(anchor=tk.W, pady=5)
        
        self.confidence_label = tk.Label(self.result_frame, text="Confiance: -", 
                                   font=("Arial", 14), bg="#f0f0f0")
        self.confidence_label.pack(anchor=tk.W, pady=5)
        
        # Frame pour les boutons
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)
        
        # Boutons
        self.load_button = tk.Button(button_frame, text="Charger une image", 
                                font=("Arial", 12), command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=10)
        
        self.analyze_button = tk.Button(button_frame, text="Analyser", 
                                  font=("Arial", 12), command=self.analyze_image,
                                  state=tk.DISABLED)
        self.analyze_button.pack(side=tk.LEFT, padx=10)
        
        self.history_button = tk.Button(button_frame, text="Historique", 
                                  font=("Arial", 12), command=self.show_history)
        self.history_button.pack(side=tk.LEFT, padx=10)
        
        # Label pour afficher le statut
        self.status_label = tk.Label(main_frame, text="Chargement du modèle...", 
                                font=("Arial", 10), bg="#f0f0f0")
        self.status_label.pack(anchor=tk.W, pady=5)
    
    def load_image(self):
        """Charge une image depuis le système de fichiers."""
        filetypes = [
            ("Images", "*.png;*.jpg;*.jpeg"),
            ("Tous les fichiers", "*.*")
        ]
        self.image_path = filedialog.askopenfilename(title="Sélectionner une image", 
                                                    filetypes=filetypes)
        if self.image_path:
            try:
                # Afficher l'image dans l'interface
                image = Image.open(self.image_path)
                image = image.resize((400, 400), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                self.image_label.config(image=photo, text="")
                self.image_label.image = photo  # Garder une référence
                
                # Activer le bouton d'analyse
                self.analyze_button.config(state=tk.NORMAL)
                self.status_label.config(text=f"Image chargée: {os.path.basename(self.image_path)}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de charger l'image: {e}")
    
    def analyze_image(self):
        """Analyse l'image pour détecter la pneumonie."""
        if not self.image_path:
            messagebox.showwarning("Avertissement", "Veuillez d'abord charger une image.")
            return
        
        if self.model is None:
            messagebox.showwarning("Avertissement", "Le modèle est encore en cours de chargement. Veuillez patienter.")
            return
        
        try:
            self.status_label.config(text="Analyse en cours...")
            self.root.update()
            
            # Prétraiter l'image
            img_array, _ = self.preprocess_image(self.image_path)
            
            # Prédiction
            prediction = self.model.predict(img_array)[0][0]
            predicted_class = "PNEUMONIE" if prediction > 0.5 else "NORMAL"
            confidence = prediction if prediction > 0.5 else 1 - prediction
            
            # Mettre à jour les labels de résultats
            self.prediction_label.config(text=f"Prédiction: {predicted_class}")
            self.confidence_label.config(text=f"Confiance: {confidence*100:.2f}%")
            
            # Générer et afficher la carte de chaleur Grad-CAM
            self.generate_gradcam(img_array)
            
            # Ajouter à l'historique
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.history.append({
                "timestamp": timestamp,
                "image_path": self.image_path,
                "prediction": predicted_class,
                "confidence": confidence
            })
            
            self.status_label.config(text="Analyse terminée avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'analyse: {e}")
            self.status_label.config(text=f"Erreur: {e}")
    
    def preprocess_image(self, image_path, target_size=(224, 224)):
        """Prétraite l'image pour la prédiction."""
        # Utilisez la fonction de prétraitement existante
        processed_img = preprocess_image(image_path, target_size)
        
        # Préparer pour le modèle (ajouter la dimension du batch)
        img_array = np.expand_dims(processed_img, axis=0)
        
        return img_array, processed_img
    
    def generate_gradcam(self, img_array):
        """Génère et affiche la carte de chaleur Grad-CAM."""
        # Vider le frame de la carte de chaleur
        for widget in self.heatmap_frame.winfo_children():
            widget.destroy()
        
        # Obtenir le nom de la dernière couche de convolution
        last_conv_layer = get_last_conv_layer_name(self.model)
        
        # Générer la carte de chaleur
        heatmap = make_gradcam_heatmap(img_array, self.model, last_conv_layer)
        
        # Charger l'image originale
        img = Image.open(self.image_path)
        img = img.resize((400, 400), Image.LANCZOS)
        img_array_display = np.array(img)
        
        # Redimensionner la carte de chaleur
        heatmap_resized = np.array(Image.fromarray(heatmap).resize((400, 400)))
        
        # Créer une figure pour l'affichage
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(img_array_display)
        
        # Superposer la carte de chaleur
        ax.imshow(heatmap_resized, cmap='jet', alpha=0.4)
        ax.set_title('Carte de chaleur Grad-CAM')
        ax.axis('off')
        
        # Afficher dans l'interface Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.heatmap_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_history(self):
        """Affiche l'historique des analyses."""
        if not self.history:
            messagebox.showinfo("Historique", "Aucune analyse n'a été effectuée.")
            return
        
        # Créer une nouvelle fenêtre pour l'historique
        history_window = tk.Toplevel(self.root)
        history_window.title("Historique des Analyses")
        history_window.geometry("600x400")
        
        # En-tête
        header_frame = tk.Frame(history_window)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        headers = ["Date", "Image", "Prédiction", "Confiance"]
        for i, header in enumerate(headers):
            tk.Label(header_frame, text=header, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10)
        
        # Frame pour la liste des analyses
        list_frame = tk.Frame(history_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Afficher chaque entrée de l'historique
        for i, entry in enumerate(self.history):
            tk.Label(list_frame, text=entry["timestamp"]).grid(row=i, column=0, padx=10, pady=5)
            tk.Label(list_frame, text=os.path.basename(entry["image_path"])).grid(row=i, column=1, padx=10, pady=5)
            tk.Label(list_frame, text=entry["prediction"]).grid(row=i, column=2, padx=10, pady=5)
            tk.Label(list_frame, text=f"{entry['confidence']*100:.2f}%").grid(row=i, column=3, padx=10, pady=5)

def main():
    # Créer l'application
    root = tk.Tk()
    app = PneumoniaDetectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()