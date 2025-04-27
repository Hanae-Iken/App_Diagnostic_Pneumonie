import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D

class PneumoniaResNet50:
    def __init__(self, input_shape=(224, 224, 3), num_classes=2):
        """
        Initialize the ResNet50 model for pneumonia detection
        
        Args:
            input_shape (tuple): Input shape of the model
            num_classes (int): Number of output classes
        """
        self.input_shape = input_shape
        self.num_classes = num_classes
        
    def build_base_model(self, trainable=False):
        """
        Build the base ResNet50 model with pre-trained weights
        
        Args:
            trainable (bool): Whether to make the base model trainable
            
        Returns:
            tf.keras.Model: Base ResNet50 model
        """
        base_model = ResNet50(
            include_top=False,
            weights='imagenet',
            input_shape=self.input_shape
        )
        
        # Freeze/unfreeze base model layers
        for layer in base_model.layers:
            layer.trainable = trainable
            
        return base_model
    
    def build_model(self, trainable=False):
        """
        Build the complete model with custom classification head
        
        Args:
            trainable (bool): Whether to make the base model trainable
            
        Returns:
            tf.keras.Model: Complete pneumonia detection model
        """
        base_model = self.build_base_model(trainable)
        
        # Add custom classification head
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.3)(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.3)(x)
        outputs = Dense(self.num_classes, activation='softmax')(x)
        
        model = Model(inputs=base_model.input, outputs=outputs)
        
        return model
    
    def get_optimizer(self, optimizer_name='adam', learning_rate=0.001):
        """
        Get the optimizer for training
        
        Args:
            optimizer_name (str): Name of the optimizer (adam, sgd, rmsprop)
            learning_rate (float): Learning rate
            
        Returns:
            tf.keras.optimizers.Optimizer: Configured optimizer
        """
        optimizers = {
            'adam': tf.keras.optimizers.Adam(learning_rate=learning_rate),
            'sgd': tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.9),
            'rmsprop': tf.keras.optimizers.RMSprop(learning_rate=learning_rate)
        }
        
        return optimizers.get(optimizer_name.lower(), optimizers['adam'])
    
    def get_callbacks(self, model_path, patience=5):
        """
        Get callbacks for training
        
        Args:
            model_path (str): Path to save the best model
            patience (int): Patience for early stopping
            
        Returns:
            list: List of callbacks
        """
        callbacks = [
            tf.keras.callbacks.ModelCheckpoint(
                model_path, 
                monitor='val_accuracy', 
                save_best_only=True, 
                mode='max'
            ),
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=patience,
                restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.2,
                patience=3,
                min_lr=1e-6
            )
        ]
        
        return callbacks