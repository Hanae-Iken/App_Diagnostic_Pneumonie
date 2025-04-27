import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

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
    
    def train(self, epochs=10, callbacks=None, steps_per_epoch=None, validation_steps=None):
        """
        Train the model
        
        Args:
            epochs (int): Number of epochs to train
            callbacks (list): List of callbacks
            steps_per_epoch (int): Steps per epoch
            validation_steps (int): Validation steps
            
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
            validation_steps=validation_steps
        )
        
        return self.history
    
    def evaluate(self):
        """
        Evaluate the model on test data
        
        Returns:
            tuple: (loss, accuracy)
        """
        test_loss, test_accuracy = self.model.evaluate(self.test_gen)
        print(f"Test Loss: {test_loss:.4f}")
        print(f"Test Accuracy: {test_accuracy:.4f}")
        
        return test_loss, test_accuracy
    
    def save_model(self, model_path):
        """
        Save the model
        
        Args:
            model_path (str): Path to save the model
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        self.model.save(model_path)
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path):
        """
        Load a saved model
        
        Args:
            model_path (str): Path to the saved model
            
        Returns:
            tf.keras.Model: Loaded model
        """
        self.model = load_model(model_path)
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
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot accuracy
        ax1.plot(self.history.history['accuracy'])
        ax1.plot(self.history.history['val_accuracy'])
        ax1.set_title('Model Accuracy')
        ax1.set_ylabel('Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.legend(['Train', 'Validation'], loc='lower right')
        
        # Plot loss
        ax2.plot(self.history.history['loss'])
        ax2.plot(self.history.history['val_loss'])
        ax2.set_title('Model Loss')
        ax2.set_ylabel('Loss')
        ax2.set_xlabel('Epoch')
        ax2.legend(['Train', 'Validation'], loc='upper right')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            
        plt.show()