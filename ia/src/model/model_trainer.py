# src/model/model_trainer.py
import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import seaborn as sns
import tensorflow as tf
from ..visualization.heatmap_generator import GradCAMGenerator

class PneumoniaModelTrainer:
    def __init__(self, model, train_gen, val_gen, test_gen):
        """
        Initialize the model trainer
        
        Args:
            model (tf.keras.Model): Model to train
            train_gen: Training data generator
            val_gen: Validation data generator
            test_gen: Test data generator
        """
        self.model = model
        self.train_gen = train_gen
        self.val_gen = val_gen
        self.test_gen = test_gen
        self.history = None
        
    def compile_model(self, optimizer, loss='categorical_crossentropy', metrics=['accuracy']):
        """
        Compile the model
        
        Args:
            optimizer: Optimizer to use
            loss (str): Loss function
            metrics (list): Metrics to track
        """
        self.model.compile(
            optimizer=optimizer,
            loss=loss,
            metrics=metrics
        )
    
    def train(self, epochs=10, callbacks=None, steps_per_epoch=None, validation_steps=None, class_weights=None):
        """
        Train the model
        
        Args:
            epochs (int): Number of epochs to train
            callbacks (list): List of callbacks
            steps_per_epoch (int): Steps per epoch
            validation_steps (int): Validation steps
            class_weights (dict): Class weights for imbalanced data
            
        Returns:
            History object containing training metrics
        """
        if steps_per_epoch is None:
            steps_per_epoch = len(self.train_gen)
        
        if validation_steps is None:
            validation_steps = len(self.val_gen)
        
        self.history = self.model.fit(
            self.train_gen,
            epochs=epochs,
            validation_data=self.val_gen,
            callbacks=callbacks,
            steps_per_epoch=steps_per_epoch,
            validation_steps=validation_steps,
            class_weight=class_weights
        )
        
        return self.history
    
    def evaluate(self, generate_heatmaps=False, num_heatmap_samples=5):
        """
        Evaluate the model on test data
        
        Args:
            generate_heatmaps (bool): Whether to generate heatmaps for sample images
            num_heatmap_samples (int): Number of sample images to generate heatmaps for
            
        Returns:
            tuple: (loss, accuracy)
        """
        test_loss, test_accuracy, *other_metrics = self.model.evaluate(self.test_gen)
        print(f"Test Loss: {test_loss:.4f}")
        print(f"Test Accuracy: {test_accuracy:.4f}")
        
        # Generate predictions
        predictions = self.model.predict(self.test_gen)
        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = self.test_gen.classes
        
        # Print classification report
        print("\nClassification Report:")
        target_names = list(self.test_gen.class_indices.keys())
        print(classification_report(true_classes, predicted_classes, target_names=target_names))
        
        # Generate and display confusion matrix
        cm = confusion_matrix(true_classes, predicted_classes)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=target_names, yticklabels=target_names)
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix')
        plt.tight_layout()
        
        # Create models directory if it doesn't exist
        models_dir = os.path.join(os.path.dirname(__file__), "../../../models")
        os.makedirs(models_dir, exist_ok=True)
        
        # Save confusion matrix
        cm_path = os.path.join(models_dir, "confusion_matrix.png")
        plt.savefig(cm_path)
        
        # Generate ROC curve for binary classification
        if len(target_names) == 2:
            fpr, tpr, _ = roc_curve(true_classes, predictions[:, 1])
            roc_auc = auc(fpr, tpr)
            
            plt.figure(figsize=(8, 6))
            plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('Receiver Operating Characteristic')
            plt.legend(loc="lower right")
            plt.tight_layout()
            
            # Save ROC curve
            roc_path = os.path.join(models_dir, "roc_curve.png")
            plt.savefig(roc_path)
        
        # Generate heatmaps for sample images if requested
        if generate_heatmaps:
            self.generate_sample_heatmaps(num_samples=num_heatmap_samples, target_names=target_names)
        
        return test_loss, test_accuracy
    
    def generate_sample_heatmaps(self, num_samples=5, target_names=None):
        """
        Generate heatmaps for sample test images
        
        Args:
            num_samples (int): Number of samples to generate heatmaps for
            target_names (list): List of class names
        """
        print("\nGenerating heatmaps for sample images...")
        
        # Create GradCAM generator
        gradcam_generator = GradCAMGenerator(self.model)
        
        # Create directory for heatmaps
        heatmap_dir = os.path.join(os.path.dirname(__file__), "../../../models/heatmaps")
        os.makedirs(heatmap_dir, exist_ok=True)
        
        # Find the last convolutional layer
        last_conv_layer = None
        for layer in reversed(self.model.layers):
            if 'conv' in layer.name.lower():
                last_conv_layer = layer.name
                break
        
        # Get sample images from test directory
        test_dir = self.test_gen.directory
        
        # Get class directories
        class_dirs = [d for d in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, d))]
        
        samples_per_class = max(1, num_samples // len(class_dirs))
        total_samples = 0
        
        # Process each class directory
        for class_dir in class_dirs:
            class_path = os.path.join(test_dir, class_dir)
            image_files = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            # Select a sample of images
            sample_files = image_files[:samples_per_class]
            
            # Process each sample image
            for img_file in sample_files:
                if total_samples >= num_samples:
                    break
                    
                img_path = os.path.join(class_path, img_file)
                output_path = os.path.join(heatmap_dir, f"{class_dir}_{img_file.split('.')[0]}_heatmap.png")
                
                try:
                    # Standard preprocessing function for ResNet50
                    def preprocess_input(x):
                        return x / 127.5 - 1
                    
                    # Generate and save heatmap
                    gradcam_generator.save_heatmap(
                        img_path=img_path,
                        output_path=output_path,
                        class_names=target_names,
                        preprocess_input=preprocess_input
                    )
                    
                    total_samples += 1
                    
                except Exception as e:
                    print(f"Error generating heatmap for {img_path}: {e}")
        
        print(f"Generated {total_samples} heatmaps in {heatmap_dir}")
    
    def save_model(self, model_path):
        """
        Save the model
        
        Args:
            model_path (str): Path to save the model
        """
        # Change file extension to .keras if it's .h5
        if model_path.endswith('.h5'):
            model_path = model_path.replace('.h5', '.keras')
            
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save with the keras format
        self.model.save(model_path, save_format='keras')
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path):
        """
        Load a saved model
        
        Args:
            model_path (str): Path to the saved model
            
        Returns:
            tf.keras.Model: Loaded model
        """
        # Change file extension to .keras if it's .h5
        if model_path.endswith('.h5'):
            keras_path = model_path.replace('.h5', '.keras')
            if os.path.exists(keras_path):
                model_path = keras_path
        
        # Add custom objects if needed
        custom_objects = {}
        
        # Load the model
        try:
            self.model = tf.keras.models.load_model(model_path, custom_objects=custom_objects)
            return self.model
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Trying alternative loading method...")
            # Alternative loading method for compatibility
            self.model = tf.keras.models.load_model(model_path, compile=False)
            return self.model
    
    def plot_training_history(self, save_path=None):
        """
        Plot training history
        
        Args:
            save_path (str, optional): Path to save the plot
        """
        if self.history is None:
            print("No training history available")
            return
        
        metrics = [m for m in self.history.history.keys() if not m.startswith('val_')]
        num_metrics = len(metrics)
        fig_rows = (num_metrics + 1) // 2  # Calculate rows needed (2 plots per row)
        
        plt.figure(figsize=(15, 5 * fig_rows))
        
        for i, metric in enumerate(metrics):
            plt.subplot(fig_rows, 2, i+1)
            plt.plot(self.history.history[metric])
            if f'val_{metric}' in self.history.history:
                plt.plot(self.history.history[f'val_{metric}'])
                plt.legend(['Train', 'Validation'], loc='best')
            else:
                plt.legend(['Train'], loc='best')
            plt.title(f'Model {metric.capitalize()}')
            plt.ylabel(metric.capitalize())
            plt.xlabel('Epoch')
            
        plt.tight_layout()
        
        if save_path:
            # Change file extension to .png if it's not already
            if not save_path.endswith('.png'):
                save_path = save_path + '.png'
            plt.savefig(save_path)
            print(f"Training history plots saved to {save_path}")
            
        plt.show()