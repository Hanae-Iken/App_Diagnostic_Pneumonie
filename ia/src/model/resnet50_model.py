import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout

class ResNet50Model:
    """
    ResNet50 model for pneumonia detection
    """
    
    def __init__(self, input_shape=(224, 224, 3), num_classes=2):
        """
        Initialize the ResNet50 model
        
        Args:
            input_shape (tuple): Input shape for the model (height, width, channels)
            num_classes (int): Number of output classes
        """
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = None
    
    def build(self, trainable_base=False):
        """
        Build the ResNet50 model with custom top layers
        
        Args:
            trainable_base (bool): Whether to make base model layers trainable
            
        Returns:
            tf.keras.Model: The complete model
        """
        # Create base model (ResNet50)
        base_model = ResNet50(
            weights='imagenet',
            include_top=False,
            input_shape=self.input_shape
        )
        
        # Set trainable status of base model layers
        for layer in base_model.layers:
            layer.trainable = trainable_base
        
        # Add custom top layers
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.5)(x)
        predictions = Dense(self.num_classes, activation='softmax')(x)
        
        # Create full model
        self.model = Model(inputs=base_model.input, outputs=predictions)
        
        return self.model
    
    def unfreeze_top_layers(self, num_layers=15):
        """
        Unfreeze top layers of the base model for fine-tuning
        
        Args:
            num_layers (int): Number of layers to unfreeze from the top
        """
        if self.model is None:
            raise ValueError("Model has not been built yet. Call build() first.")
        
        # Get the base model (the first layer should be the ResNet50 model)
        base_model = self.model.layers[0]
        
        # Unfreeze the specified number of top layers
        for layer in base_model.layers[-(num_layers):]:
            layer.trainable = True
        
        return self.model
    
    def summary(self):
        """
        Print model summary
        """
        if self.model is None:
            raise ValueError("Model has not been built yet. Call build() first.")
        
        return self.model.summary()
    
    def save(self, path):
        """
        Save the model to the specified path
        
        Args:
            path (str): Path to save the model
        """
        if self.model is None:
            raise ValueError("Model has not been built yet. Call build() first.")
        
        self.model.save(path)
        print(f"Model saved to {path}")
    
    def load(self, path):
        """
        Load a saved model
        
        Args:
            path (str): Path to the saved model
        """
        self.model = tf.keras.models.load_model(path)
        return self.model