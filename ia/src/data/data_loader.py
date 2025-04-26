# src/data/data_loader.py
import os
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def load_dataset(data_dir, target_size=(224, 224), batch_size=32, class_mode='binary'):
    """
    Charge un ensemble de données à partir d'un répertoire en utilisant ImageDataGenerator.
    
    Args:
        data_dir: Chemin vers le répertoire contenant les sous-dossiers de classes
        target_size: Dimensions cibles des images
        batch_size: Taille des lots pour le chargement
        class_mode: Mode de classification ('binary', 'categorical', etc.)
        
    Returns:
        Un générateur d'images
    """
    datagen = ImageDataGenerator(rescale=1./255)
    
    generator = datagen.flow_from_directory(
        data_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode=class_mode,
        shuffle=False
    )
    
    return generator

def load_and_augment_training_data(train_dir, val_dir, target_size=(224, 224), batch_size=32):
    """
    Charge les données d'entraînement avec augmentation et les données de validation.
    
    Args:
        train_dir: Chemin vers le répertoire d'entraînement
        val_dir: Chemin vers le répertoire de validation
        target_size: Dimensions cibles des images
        batch_size: Taille des lots pour le chargement
        
    Returns:
        Générateurs pour l'entraînement et la validation
    """
    # Générateur avec augmentation pour l'entraînement
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Générateur sans augmentation pour la validation
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Créer les générateurs
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary'
    )
    
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary'
    )
    
    return train_generator, val_generator

def get_class_distribution(data_dir):
    """
    Calcule la distribution des classes dans un répertoire de données.
    
    Args:
        data_dir: Chemin vers le répertoire contenant les sous-dossiers de classes
        
    Returns:
        Un dictionnaire avec le nombre d'échantillons par classe
    """
    distribution = {}
    
    for class_name in os.listdir(data_dir):
        class_dir = os.path.join(data_dir, class_name)
        if os.path.isdir(class_dir):
            # Compter le nombre de fichiers images
            n_samples = len([f for f in os.listdir(class_dir) 
                            if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            distribution[class_name] = n_samples
    
    return distribution

def load_metadata(metadata_file):
    """
    Charge les métadonnées des images depuis un fichier CSV.
    
    Args:
        metadata_file: Chemin vers le fichier CSV de métadonnées
        
    Returns:
        DataFrame pandas contenant les métadonnées
    """
    if not os.path.exists(metadata_file):
        print(f"Le fichier de métadonnées {metadata_file} n'existe pas.")
        return None
    
    metadata_df = pd.read_csv(metadata_file)
    return metadata_df