#ia/src/visualization/heatmap_generator.py
import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.cm as cm

class GradCAMGenerator:
    """
    Generates Grad-CAM (Gradient-weighted Class Activation Mapping) heatmaps 
    to highlight regions that influence the model's predictions
    """
    
    def __init__(self, model, last_conv_layer_name=None, classifier_layer_names=None):
        """
        Initialize GradCAM generator
        
        Args:
            model (tf.keras.Model): Trained model
            last_conv_layer_name (str): Name of the last convolutional layer
            classifier_layer_names (list): Names of classifier layers after the last conv layer
        """
        self.model = model
        
        # If layer names are not provided, try to find them automatically
        if last_conv_layer_name is None:
            # For ResNet50, the last conv layer is usually the last layer with 'conv' in its name
            for layer in reversed(model.layers):
                if 'conv' in layer.name.lower():
                    last_conv_layer_name = layer.name
                    break
        
        if classifier_layer_names is None:
            classifier_layer_names = []
            # Find dense layers after the last conv layer
            found_conv = False
            for layer in model.layers:
                if layer.name == last_conv_layer_name:
                    found_conv = True
                    continue
                if found_conv and 'dense' in layer.name.lower():
                    classifier_layer_names.append(layer.name)
        
        self.last_conv_layer_name = last_conv_layer_name
        self.classifier_layer_names = classifier_layer_names
        
        # Print detected layers for debugging
        print(f"Last convolutional layer: {self.last_conv_layer_name}")
        print(f"Classifier layers: {self.classifier_layer_names}")
        
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
        # First, get the convolutional layer output
        conv_layer = self.model.get_layer(self.last_conv_layer_name)
        
        # Next, get classifier layer inputs and outputs
        classifier_input = conv_layer.output
        classifier_outputs = []
        
        # For ResNet50 with global average pooling, we need to handle the flow
        x = classifier_input
        
        # If there are classifier layers specified, trace through them
        if self.classifier_layer_names:
            for layer_name in self.classifier_layer_names:
                x = self.model.get_layer(layer_name)(x)
                classifier_outputs.append(x)
        else:
            # Otherwise, trace through the model from the conv layer to the end
            found_conv = False
            for layer in self.model.layers:
                if layer.name == self.last_conv_layer_name:
                    found_conv = True
                    continue
                if found_conv:
                    x = layer(x)
            classifier_outputs.append(self.model.output)
        
        # Create grad model
        return Model(
            inputs=self.model.inputs,
            outputs=[conv_layer.output, self.model.output]
        )
    
    def generate_heatmap(self, img_path, class_idx=None, preprocess_input=None, alpha=0.4):
        """
        Generate a heatmap for a specific image
        
        Args:
            img_path (str): Path to the image
            class_idx (int): Index of the class to generate heatmap for (default is predicted class)
            preprocess_input (function): Function to preprocess input image
            alpha (float): Transparency of the heatmap overlay (0-1)
            
        Returns:
            tuple: (superimposed_img, heatmap, prediction, class_idx)
        """
        # Load and preprocess image
        original_img = load_img(img_path, target_size=(self.model.input_shape[1], self.model.input_shape[2]))
        img_array = img_to_array(original_img)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Apply preprocessing if provided
        if preprocess_input:
            img_array = preprocess_input(img_array)
        else:
            # Default preprocessing (rescale to [-1, 1])
            img_array = img_array / 127.5 - 1
        
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
    
    def save_heatmap(self, img_path, output_path, class_names=None, preprocess_input=None):
        """
        Generate and save heatmap for a specific image
        
        Args:
            img_path (str): Path to the image
            output_path (str): Path to save the output image
            class_names (list): List of class names
            preprocess_input (function): Function to preprocess input image
            
        Returns:
            tuple: (prediction_class, confidence)
        """
        # Generate heatmap
        superimposed_img, heatmap, score, class_idx = self.generate_heatmap(
            img_path, preprocess_input=preprocess_input
        )
        
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
    
    def generate_multiple_heatmaps(self, img_dir, output_dir, class_names=None, 
                                  preprocess_input=None, limit=10, file_extensions=('.jpg', '.jpeg', '.png')):
        """
        Generate heatmaps for multiple images in a directory
        
        Args:
            img_dir (str): Directory containing images
            output_dir (str): Directory to save output images
            class_names (list): List of class names
            preprocess_input (function): Function to preprocess input image
            limit (int): Maximum number of images to process
            file_extensions (tuple): File extensions to process
            
        Returns:
            list: List of (image_path, prediction_class, confidence) tuples
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Get list of image files
        img_files = []
        for root, _, files in os.walk(img_dir):
            for file in files:
                if file.lower().endswith(file_extensions):
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
                
                # Generate and save heatmap
                class_idx, score = self.save_heatmap(
                    img_path, output_path, class_names, preprocess_input
                )
                
                results.append((img_path, class_idx, score))
            except Exception as e:
                print(f"Error processing {img_path}: {e}")
        
        return results

def preprocess_for_resnet50(x):
    """
    Standard preprocessing for ResNet50
    
    Args:
        x (numpy.ndarray): Input image
        
    Returns:
        numpy.ndarray: Preprocessed image
    """
    return x / 127.5 - 1

def create_sample_heatmap_visualization(original_img, heatmap, superimposed_img, 
                                      prediction, class_names, output_path):
    """
    Create a sample visualization with original image, heatmap, and superimposed image
    
    Args:
        original_img: Original image
        heatmap: Heatmap array
        superimposed_img: Superimposed image (heatmap on original)
        prediction (tuple): (class_idx, score)
        class_names (list): List of class names
        output_path (str): Path to save the visualization
    """
    # Convert PIL to numpy if needed
    if not isinstance(original_img, np.ndarray):
        original_img = tf.keras.preprocessing.image.img_to_array(original_img)
    
    if not isinstance(superimposed_img, np.ndarray):
        superimposed_img = tf.keras.preprocessing.image.img_to_array(superimposed_img)
    
    # Create figure with subplots
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot original image
    ax[0].imshow(original_img / 255.)
    ax[0].set_title('Original Image')
    ax[0].axis('off')
    
    # Plot heatmap
    ax[1].imshow(heatmap, cmap='jet')
    ax[1].set_title('Grad-CAM Heatmap')
    ax[1].axis('off')
    
    # Plot superimposed image
    ax[2].imshow(superimposed_img / 255.)
    class_idx, score = prediction
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