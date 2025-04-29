import os
import sys
import argparse
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

# Correction des chemins d'importation
current_dir = os.path.dirname(os.path.abspath(__file__))
# Remonte de deux niveaux pour atteindre la racine du projet "ia"
parent_dir = os.path.dirname(current_dir)
ia_root = os.path.dirname(parent_dir)
project_root = os.path.dirname(ia_root)  # Racine du projet complet

# Ajouter les chemins nécessaires au sys.path
sys.path.append(ia_root)

# Import nos modules avec les chemins corrects
from src.data.data_preprocessing import DataPreprocessor
from src.data.data_loader import create_data_generators

def preprocess_data():
    """
    Run the data preprocessing pipeline
    """
    print("Starting data preprocessing...")
    
    # Chemins pour les données par rapport à la racine du projet "ia"
    # Modifié pour pointer vers ia/data au lieu de projet_pneumonie_ia/data
    raw_data_dir = os.path.join(ia_root, "data", "raw")
    processed_data_dir = os.path.join(ia_root, "data", "processed")
    
    # Créer les répertoires s'ils n'existent pas
    os.makedirs(raw_data_dir, exist_ok=True)
    os.makedirs(processed_data_dir, exist_ok=True)
    
    print(f"Raw data directory: {raw_data_dir}")
    print(f"Processed data directory: {processed_data_dir}")
    
    # Créer et exécuter le préprocesseur
    preprocessor = DataPreprocessor(raw_data_dir, processed_data_dir)
    preprocessor.preprocess_and_save()
    
    # Optionnel: équilibrer les classes
    # preprocessor.balance_classes()
    
    print("Data preprocessing completed!")
    
    return processed_data_dir

def build_model(input_shape=(224, 224, 3), num_classes=2):
    """
    Build a ResNet50 model for pneumonia classification
    
    Args:
        input_shape (tuple): Input shape for the model
        num_classes (int): Number of output classes
        
    Returns:
        Model: Compiled Keras model
    """
    # Load ResNet50 with pre-trained weights
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
    
    # Add classification head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Freeze the base model layers
    for layer in base_model.layers:
        layer.trainable = False
    
    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )
    
    return model

def train_model(model, train_generator, validation_generator, class_weights, epochs=20):
    """
    Train the model
    
    Args:
        model: Compiled Keras model
        train_generator: Training data generator
        validation_generator: Validation data generator
        class_weights: Class weights for imbalanced data
        epochs (int): Number of epochs to train
        
    Returns:
        History: Training history
    """
    # Create callbacks
    models_dir = os.path.join(ia_root, "models")  # Modifié ici
    os.makedirs(models_dir, exist_ok=True)
    checkpoint_path = os.path.join(models_dir, "pneumonia_model_best.h5")
    
    callbacks = [
        ModelCheckpoint(checkpoint_path, monitor='val_accuracy', save_best_only=True, mode='max'),
        EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=1e-6)
    ]
    
    # Train the model
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // train_generator.batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // validation_generator.batch_size,
        callbacks=callbacks,
        class_weight=class_weights,
        verbose=1
    )
    
    return history

def evaluate_model(model, test_generator):
    """
    Evaluate the model on test data
    
    Args:
        model: Trained Keras model
        test_generator: Test data generator
        
    Returns:
        tuple: (loss, accuracy, precision, recall)
    """
    results = model.evaluate(test_generator, steps=test_generator.samples // test_generator.batch_size)
    print(f"Test loss: {results[0]}")
    print(f"Test accuracy: {results[1]}")
    print(f"Test precision: {results[2]}")
    print(f"Test recall: {results[3]}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Pneumonia classification training pipeline")
    parser.add_argument("--skip-preprocessing", action="store_true", help="Skip data preprocessing")
    parser.add_argument("--epochs", type=int, default=20, help="Number of epochs for training")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size for training")
    args = parser.parse_args()
    
    # Run preprocessing or use existing processed data
    if args.skip_preprocessing:
        processed_data_dir = os.path.join(ia_root, "data", "processed")  # Modifié ici
        if not os.path.exists(processed_data_dir):
            print("Processed data directory not found. Running preprocessing...")
            processed_data_dir = preprocess_data()
    else:
        processed_data_dir = preprocess_data()
    
    # Create data generators
    train_generator, validation_generator, test_generator, class_weights = create_data_generators(
        processed_data_dir=processed_data_dir,
        batch_size=args.batch_size
    )
    
    # Build model
    model = build_model()
    
    # Print model summary
    model.summary()
    
    # Train model
    history = train_model(model, train_generator, validation_generator, class_weights, epochs=args.epochs)
    
    # Evaluate model
    evaluate_model(model, test_generator)
    
    print("Training completed!")

if __name__ == "__main__":
    main()