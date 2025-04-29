#ia/src/visualization/pneumonia_detection_gui.py
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tensorflow.keras.models import load_model
from PIL import Image, ImageTk

class PneumoniaDetectionGUI:
    def __init__(self, root, model_path):
        """
        Initialize the GUI application
        
        Args:
            root: Tkinter root window
            model_path (str): Path to the trained model file
        """
        self.root = root
        self.root.title("Pneumonia Detection System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Load model
        try:
            self.model = load_model(model_path)
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model: {e}")
            root.destroy()
            return
        
        self.img_size = 224  # Expected input size for the model
        self.classes = ['NORMAL', 'PNEUMONIA']
        
        # Create GUI components
        self.create_widgets()
        
        # Currently loaded image
        self.current_image_path = None
        self.current_image = None
        
    def create_widgets(self):
        """Create GUI widgets"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="Pneumonia Detection System", 
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            pady=10
        )
        title_label.pack()
        
        # Frame for buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        # Load image button
        self.load_btn = tk.Button(
            button_frame,
            text="Load X-ray Image",
            command=self.load_image,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5
        )
        self.load_btn.pack(side=tk.LEFT, padx=10)
        
        # Predict button
        self.predict_btn = tk.Button(
            button_frame,
            text="Predict",
            command=self.predict,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=5,
            state=tk.DISABLED  # Disabled until an image is loaded
        )
        self.predict_btn.pack(side=tk.LEFT, padx=10)
        
        # Frame for image display
        self.image_frame = tk.Frame(self.root, bg="white", width=500, height=400)
        self.image_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Label for displaying image
        self.image_label = tk.Label(self.image_frame, bg="white")
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Frame for prediction results
        result_frame = tk.Frame(self.root, bg="#f0f0f0")
        result_frame.pack(pady=10, fill=tk.X)
        
        # Label for prediction result
        self.result_var = tk.StringVar()
        self.result_var.set("No prediction yet")
        
        result_label = tk.Label(
            result_frame,
            textvariable=self.result_var,
            font=("Arial", 14),
            bg="#f0f0f0",
            pady=10
        )
        result_label.pack()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_image(self):
        """Load an image file"""
        # Open file dialog to select an image
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png"),
            ("All files", "*.*")
        ]
        
        image_path = filedialog.askopenfilename(
            title="Select X-ray Image",
            filetypes=filetypes
        )
        
        if image_path:
            try:
                # Read and display the image
                self.display_image(image_path)
                self.current_image_path = image_path
                self.status_var.set(f"Image loaded: {os.path.basename(image_path)}")
                self.predict_btn.config(state=tk.NORMAL)  # Enable predict button
                self.result_var.set("No prediction yet")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")
                self.status_var.set("Failed to load image")
    
    def display_image(self, image_path):
        """Display the loaded image"""
        # Read image using PIL
        img = Image.open(image_path)
        
        # Resize to fit the frame while maintaining aspect ratio
        width, height = img.size
        max_size = 400
        
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        
        # Resize and convert to PhotoImage
        img = img.resize((new_width, new_height), Image.LANCZOS)
        self.current_image = ImageTk.PhotoImage(img)
        
        # Update label
        self.image_label.config(image=self.current_image)
        self.image_label.image = self.current_image  # Keep a reference
    
    def preprocess_image(self, img_path):
        """Preprocess image for prediction"""
        # Read image
        img = cv2.imread(img_path)
        
        # Convert to RGB (from BGR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize to the expected size
        img = cv2.resize(img, (self.img_size, self.img_size))
        
        # Normalize
        img = img / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def predict(self):
        """Make prediction on the loaded image"""
        if not self.current_image_path:
            messagebox.showinfo("Info", "Please load an image first")
            return
        
        try:
            self.status_var.set("Processing...")
            self.root.update()
            
            # Preprocess image
            preprocessed_img = self.preprocess_image(self.current_image_path)
            
            # Make prediction with the model
            prediction = self.model.predict(preprocessed_img)
            
            # Get class index and probability
            class_idx = np.argmax(prediction[0])
            probability = prediction[0][class_idx]
            
            predicted_class = self.classes[class_idx]
            
            # Update result
            result_text = f"Prediction: {predicted_class}\nConfidence: {probability:.2%}"
            self.result_var.set(result_text)
            
            # Color code the result (green for normal, red for pneumonia)
            if predicted_class == "NORMAL":
                self.image_label.config(borderwidth=5, relief=tk.SOLID, bd=5, highlightbackground="green", highlightcolor="green")
            else:
                self.image_label.config(borderwidth=5, relief=tk.SOLID, bd=5, highlightbackground="red", highlightcolor="red")
            
            self.status_var.set(f"Prediction complete: {predicted_class}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {e}")
            self.status_var.set("Prediction failed")

def main():
    # Find model path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
    model_path = os.path.join(project_root, "models", "resnet50_base.keras")
    
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        sys.exit(1)
    
    # Create Tkinter root
    root = tk.Tk()
    
    # Create app
    app = PneumoniaDetectionGUI(root, model_path)
    
    # Run app
    root.mainloop()

if __name__ == "__main__":
    main()