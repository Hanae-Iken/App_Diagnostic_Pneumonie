import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ajouter le répertoire parent au chemin Python
sys.path.append(os.path.abspath('..'))

from src.data.data_preprocessing import DataPreprocessor
from src.visualization.gradcam import GradCAM

class PneumoniaDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Détection de Pneumonie")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Chargement du modèle
        self.load_model()
        
        # Création de l'interface
        self.create_widgets()
        
        # Variables pour stocker les données
        self.current_image = None
        self.processed_image = None
        self.history = []

    def load_model(self):
        try:
            MODEL_PATH = '../models/resnet50_finetune.h5'
            self.model = load_model(MODEL_PATH)
            self.preprocessor = DataPreprocessor(target_size=(224, 224))
            self.gradcam = GradCAM(self.model, "conv5_block3_out")
            print("Modèle chargé avec succès!")
        except Exception as e:
            print(f"Erreur lors du chargement du modèle: {e}")
            messagebox.showerror("Erreur", f"Impossible de charger le modèle: {e}")
            self.root.quit()

    def create_widgets(self):
        # Frame principale
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre
        title_label = tk.Label(main_frame, text="Détection de Pneumonie par IA", 
                              font=("Arial", 24, "bold"), bg="#f0f0f0")
        title_label.pack(pady=(0, 20))
        
        # Zone de contrôle (gauche)
        control_frame = tk.Frame(main_frame, bg="#f0f0f0", width=300)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Bouton de chargement d'image
        load_button = tk.Button(control_frame, text="Charger une radiographie", 
                                command=self.load_image, 
                                font=("Arial", 12), padx=10, pady=5,
                                bg="#4CAF50", fg="white")
        load_button.pack(fill=tk.X, pady=(0, 20))
        
        # Cadre pour les résultats
        result_frame = tk.LabelFrame(control_frame, text="Résultats", 
                                    font=("Arial", 12, "bold"), bg="#f0f0f0",
                                    padx=10, pady=10)
        result_frame.pack(fill=tk.X)
        
        self.result_label = tk.Label(result_frame, text="Pas d'analyse effectuée", 
                                     font=("Arial", 12), bg="#f0f0f0",
                                     justify=tk.LEFT, wraplength=250)
        self.result_label.pack(fill=tk.X, pady=5)
        
        self.probability_label = tk.Label(result_frame, text="", 
                                         font=("Arial", 12), bg="#f0f0f0")
        self.probability_label.pack(fill=tk.X, pady=5)
        
        # Bouton d'analyse
        analyze_button = tk.Button(control_frame, text="Analyser l'image", 
                                  command=self.analyze_image, 
                                  font=("Arial", 12), padx=10, pady=5,
                                  bg="#2196F3", fg="white")
        analyze_button.pack(fill=tk.X, pady=20)
        
        # Historique
        history_frame = tk.LabelFrame(control_frame, text="Historique", 
                                     font=("Arial", 12, "bold"), bg="#f0f0f0",
                                     padx=10, pady=10)
        history_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.history_listbox = tk.Listbox(history_frame, height=10, font=("Arial", 10))
        self.history_listbox.pack(fill=tk.X)
        
        # Zone d'affichage (droite)
        display_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief=tk.GROOVE)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Créer un canevas matplotlib pour l'affichage des images
        self.fig, self.axes = plt.subplots(1, 3, figsize=(12, 4))
        self.fig.subplots_adjust(wspace=0.3)
        
        for ax in self.axes:
            ax.axis('off')
        
        self.axes[0].set_title("Image originale")
        self.axes[1].set_title("Carte de chaleur GradCAM")
        self.axes[2].set_title("Superposition")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=display_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Note de bas de page
        footer = tk.Label(main_frame, text="Ce logiciel est un outil d'aide à la décision et ne remplace pas l'expertise d'un radiologue.", 
                          font=("Arial", 10, "italic"), bg="#f0f0f0")
        footer.pack(side=tk.BOTTOM, pady=(20, 0))

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Sélectionner une radiographie",
            filetypes=[
                ("Images", "*.jpg *.jpeg *.png *.bmp"),
                ("DICOM", "*.dcm"),
                ("Tous les fichiers", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        try:
            # Charger l'image
            if file_path.lower().endswith('.dcm'):
                # Traitement des fichiers DICOM
                import pydicom
                dicom_data = pydicom.dcmread(file_path)
                img = dicom_data.pixel_array
                
                # Normaliser l'image
                img = (img - img.min()) / (img.max() - img.min()) * 255
                img = img.astype(np.uint8)
                
                # Convertir en RGB si nécessaire
                if len(img.shape) == 2:
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            else:
                # Traitement des formats d'image standard
                img = cv2.imread(file_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Stocker l'image
            self.current_image = img
            
            # Afficher l'image originale
            self.axes[0].clear()
            self.axes[0].imshow(img)
            self.axes[0].set_title("Image originale")
            self.axes[0].axis('off')
            
            # Effacer les autres axes
            self.axes[1].clear()
            self.axes[1].set_title("Carte de chaleur GradCAM")
            self.axes[1].axis('off')
            
            self.axes[2].clear()
            self.axes[2].set_title("Superposition")
            self.axes[2].axis('off')
            
            self.canvas.draw()
            
            # Réinitialiser les résultats
            self.result_label.config(text="Pas d'analyse effectuée")
            self.probability_label.config(text="")
            
            # Ajouter à l'historique
            file_name = os.path.basename(file_path)
            self.history_listbox.insert(0, file_name)
            self.history.insert(0, {"name": file_name, "path": file_path})
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger l'image: {e}")

    def analyze_image(self):
        if self.current_image is None:
            messagebox.showinfo("Info", "Veuillez d'abord charger une image.")
            return
        
        try:
            # Prétraiter l'image
            processed_image = self.preprocessor.preprocess_image(self.current_image)
            self.processed_image = processed_image
            
            # Faire une prédiction
            img_batch = np.expand_dims(processed_image, axis=0)
            prediction = self.model.predict(img_batch)[0][0]
            
            # Générer la carte de chaleur GradCAM
            heatmap = self.gradcam.compute_heatmap(img_batch, pred_class=0 if prediction <= 0.5 else 1)
            cam_image = self.gradcam.overlay_heatmap(processed_image, heatmap, alpha=0.5)
            
            # Afficher les résultats
            if prediction > 0.5:
                result_text = "Pneumonie détectée"
                self.result_label.config(text=result_text, fg="#E53935")
            else:
                result_text = "Pas de pneumonie détectée"
                self.result_label.config(text=result_text, fg="#43A047")
            
            self.probability_label.config(text=f"Probabilité: {prediction*100:.2f}%")
            
            # Mettre à jour l'historique
            current_item = self.history[0]
            current_item["result"] = result_text
            current_item["probability"] = f"{prediction*100:.2f}%"
            
            # Afficher la carte de chaleur
            self.axes[1].clear()
            self.axes[1].imshow(heatmap, cmap='jet')
            self.axes[1].set_title("Carte de chaleur GradCAM")
            self.axes[1].axis('off')
            
            # Afficher la superposition
            self.axes[2].clear()
            self.axes[2].imshow(cam_image)
            self.axes[2].set_title("Superposition")
            self.axes[2].axis('off')
            
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'analyse: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PneumoniaDetectionApp(root)
    root.mainloop()