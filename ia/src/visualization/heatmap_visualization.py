# ia/src/visualization/heatmap_visualization.py
import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.cm as cm
import argparse
import sys

# Correction des chemins d'importation
current_dir = os.path.dirname(os.path.abspath(__file__))
visualization_dir = current_dir
src_dir = os.path.dirname(visualization_dir)
ia_root = os.path.dirname(src_dir)

# Ajouter les chemins nécessaires au sys.path
sys.path.append(ia_root)
sys.path.append(src_dir)

from src.data.data_loader import create_data_generators

class PneumoniaGradCAM:
    """
    Generates Grad-CAM heatmaps for pneumonia classification model
    to highlight regions that influence the model's predictions
    """
    
    def __init__(self, model_path, last_conv_layer_name=None):
        """
        Initialize GradCAM generator
        
        Args:
            model_path (str): Path to the trained model file (.h5)
            last_conv_layer_name (str): Name of the last convolutional layer
        """
        # Load the model
        self.model = load_model(model_path)
        print(f"Model loaded from {model_path}")
        
        # If layer name is not provided, try to find it automatically
        if last_conv_layer_name is None:
            # For ResNet50, the last conv layer is usually the last layer with 'conv' in its name
            for layer in reversed(self.model.layers):
                if 'conv' in layer.name.lower():
                    last_conv_layer_name = layer.name
                    break
        
        self.last_conv_layer_name = last_conv_layer_name
        print(f"Last convolutional layer: {self.last_conv_layer_name}")
        
        # Create the grad model
        self.grad_model = self._make_gradcam_model()
    
    def _make_gradcam_model(self):
        """
        Create a model that maps from input image to:
        1. Conv layer outputs
        2. Predicted class probabilities
        
        Returns:
            tf.keras.Model: GradCAM model
        """
        # Get the convolutional layer output
        last_conv_layer = self.model.get_layer(self.last_conv_layer_name)
        
        # Create grad model
        return tf.keras.models.Model(
            inputs=self.model.inputs,
            outputs=[last_conv_layer.output, self.model.output]
        )
    
    def preprocess_image(self, img_path, target_size=(224, 224)):
        """
        Load and preprocess an image for inference
        
        Args:
            img_path (str): Path to the image
            target_size (tuple): Target size for the image
            
        Returns:
            tuple: (original image, preprocessed image array)
        """
        # Load image
        original_img = load_img(img_path, target_size=target_size)
        img_array = img_to_array(original_img)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Preprocess (normalize to [-1, 1])
        img_array = img_array / 127.5 - 1
        
        return original_img, img_array
    
    def generate_heatmap(self, img_path, class_idx=None, target_size=(224, 224), alpha=0.4):
        """
        Generate a heatmap for a specific image
        
        Args:
            img_path (str): Path to the image
            class_idx (int): Index of the class to generate heatmap for (default is predicted class)
            target_size (tuple): Target size for the image
            alpha (float): Transparency of the heatmap overlay (0-1)
            
        Returns:
            tuple: (superimposed_img, heatmap, prediction, class_idx)
        """
        # Preprocess image
        original_img, img_array = self.preprocess_image(img_path, target_size)
        
        # Make prediction
        preds = self.model.predict(img_array)
        
        # If class_idx is not specified, use the predicted class
        if class_idx is None:
            class_idx = np.argmax(preds[0])
        
        # Get the score for the specified class
        score = preds[0][class_idx]
        
        # Generate gradient-based class activation map
        with tf.GradientTape() as tape:
            # Get activations of last conv layer and predictions
            last_conv_layer_output, predictions = self.grad_model(img_array)
            
            # Watch the conv layer output
            tape.watch(last_conv_layer_output)
            
            # Get the gradient of the top predicted class with respect to the conv layer output
            grads = tape.gradient(predictions[:, class_idx], last_conv_layer_output)
        
        # Remove batch dimension and pool gradients
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Weight the channels by the gradient importance
        last_conv_layer_output = last_conv_layer_output[0]
        heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        
        # Normalize the heatmap
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        heatmap = heatmap.numpy()
        
        # Create a colored heatmap
        heatmap_img = np.uint8(255 * heatmap)
        jet_heatmap = cm.jet(heatmap_img)[..., :3]
        jet_heatmap = tf.keras.preprocessing.image.array_to_img(jet_heatmap)
        jet_heatmap = jet_heatmap.resize((original_img.width, original_img.height))
        jet_heatmap = tf.keras.preprocessing.image.img_to_array(jet_heatmap)
        
        # Superimpose the heatmap on the original image
        original_img_array = tf.keras.preprocessing.image.img_to_array(original_img)
        superimposed_img = jet_heatmap * alpha + original_img_array
        superimposed_img = tf.keras.preprocessing.image.array_to_img(superimposed_img)
        
        return superimposed_img, heatmap, score, class_idx
    
    def save_heatmap(self, img_path, output_path, class_names=None):
        """
        Generate and save heatmap for a specific image
        
        Args:
            img_path (str): Path to the image
            output_path (str): Path to save the output image
            class_names (list): List of class names
            
        Returns:
            tuple: (prediction_class, confidence)
        """
        # Generate heatmap
        superimposed_img, heatmap, score, class_idx = self.generate_heatmap(img_path)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the superimposed image
        superimposed_img.save(output_path)
        
        # Get class name
        class_name = f"Class {class_idx}"
        if class_names and class_idx < len(class_names):
            class_name = class_names[class_idx]
        
        print(f"Heatmap for {os.path.basename(img_path)} saved to {output_path}")
        print(f"Prediction: {class_name} with confidence {score:.4f}")
        
        return class_idx, score
    
    def create_visualization(self, img_path, output_path, class_names=None):
        """
        Create a comprehensive visualization with original image, heatmap, and superimposed image
        
        Args:
            img_path (str): Path to the image
            output_path (str): Path to save the visualization
            class_names (list): List of class names
            
        Returns:
            tuple: (prediction_class, confidence)
        """
        # Generate heatmap
        superimposed_img, heatmap, score, class_idx = self.generate_heatmap(img_path)
        
        # Load original image again
        original_img = load_img(img_path, target_size=(224, 224))
        original_img_array = img_to_array(original_img)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create figure with subplots
        fig, ax = plt.subplots(1, 3, figsize=(15, 5))
        
        # Plot original image
        ax[0].imshow(original_img_array / 255.)
        ax[0].set_title('Original Image')
        ax[0].axis('off')
        
        # Plot heatmap
        ax[1].imshow(heatmap, cmap='jet')
        ax[1].set_title('Grad-CAM Heatmap')
        ax[1].axis('off')
        
        # Plot superimposed image
        superimposed_img_array = img_to_array(superimposed_img)
        ax[2].imshow(superimposed_img_array / 255.)
        
        # Get class name
        class_name = f"Class {class_idx}"
        if class_names and class_idx < len(class_names):
            class_name = class_names[class_idx]
            
        ax[2].set_title(f'Prediction: {class_name}\nConfidence: {score:.2f}')
        ax[2].axis('off')
        
        # Save figure
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close(fig)
        
        print(f"Visualization saved to {output_path}")
        return class_idx, score
    
    def process_directory(self, img_dir, output_dir, class_names=None, limit=10):
        """
        Process multiple images in a directory
        
        Args:
            img_dir (str): Directory containing images
            output_dir (str): Directory to save output images
            class_names (list): List of class names
            limit (int): Maximum number of images to process
            
        Returns:
            list: List of (image_path, prediction_class, confidence) tuples
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get list of image files
        img_extensions = ('.jpg', '.jpeg', '.png')
        img_files = []
        
        for root, _, files in os.walk(img_dir):
            for file in files:
                if file.lower().endswith(img_extensions):
                    img_files.append(os.path.join(root, file))
        
        # Sort and limit
        img_files.sort()
        if limit > 0:
            img_files = img_files[:limit]
        
        results = []
        for img_path in img_files:
            try:
                # Generate output path
                relative_path = os.path.relpath(img_path, img_dir)
                output_path = os.path.join(output_dir, f"{os.path.splitext(relative_path)[0]}_heatmap.png")
                
                # Create intermediate directories
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Generate and save visualization
                class_idx, score = self.create_visualization(
                    img_path, output_path, class_names
                )
                
                results.append((img_path, class_idx, score))
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
        
        return results
    
    def process_test_set(self, processed_data_dir, output_dir, class_names=None, limit=20):
        """
        Process images from the test set
        
        Args:
            processed_data_dir (str): Path to the processed data directory
            output_dir (str): Directory to save output images
            class_names (list): List of class names
            limit (int): Maximum number of images to process per class
            
        Returns:
            dict: Results per class
        """
        test_dir = os.path.join(processed_data_dir, "test")
        if not os.path.exists(test_dir):
            raise ValueError(f"Test directory not found: {test_dir}")
        
        results = {}
        
        # Process each class directory
        for class_name in os.listdir(test_dir):
            class_dir = os.path.join(test_dir, class_name)
            if not os.path.isdir(class_dir):
                continue
                
            class_output_dir = os.path.join(output_dir, class_name)
            os.makedirs(class_output_dir, exist_ok=True)
            
            # Process images in this class
            class_results = self.process_directory(
                class_dir, class_output_dir, class_names, limit
            )
            
            results[class_name] = class_results
            
        return results


def main():
    parser = argparse.ArgumentParser(description="Generate Grad-CAM heatmaps for pneumonia classification model")
    parser.add_argument("--model", type=str, required=True, help="Path to the trained model (.h5 file)")
    parser.add_argument("--data-dir", type=str, help="Path to the processed data directory")
    parser.add_argument("--image", type=str, help="Path to a single image to process")
    parser.add_argument("--output-dir", type=str, default="results/heatmaps", help="Directory to save heatmaps")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of images to process per class")
    args = parser.parse_args()
    
    # Create GradCAM generator
    gradcam = PneumoniaGradCAM(args.model)
    
    # Define class names
    class_names = ['NORMAL', 'PNEUMONIA']
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    if args.image:
        # Process a single image
        output_path = os.path.join(args.output_dir, f"{os.path.splitext(os.path.basename(args.image))[0]}_heatmap.png")
        gradcam.create_visualization(args.image, output_path, class_names)
    elif args.data_dir:
        # Process test set
        gradcam.process_test_set(args.data_dir, args.output_dir, class_names, args.limit)
    else:
        print("Please provide either --image or --data-dir")
        return 1
    
    print("Heatmap generation completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())