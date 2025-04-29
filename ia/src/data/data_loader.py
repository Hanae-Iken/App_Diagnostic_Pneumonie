# ia/src/data_loader.py
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def create_data_generators(processed_data_dir=None, batch_size=32, img_size=(224, 224)):
    """
    Create train, validation, and test data generators for pneumonia dataset
    with enhanced augmentation and preprocessing
   
    Args:
        processed_data_dir (str): Path to processed data. If None, defaults to appropriate path
        batch_size (int): Batch size for training
        img_size (tuple): Image size for model input
       
    Returns:
        tuple: (train_generator, validation_generator, test_generator, class_weights)
    """
    # Path to the dataset
    if processed_data_dir is None:
        # Déterminer le chemin des données par rapport à ce fichier
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ia_root = os.path.dirname(os.path.dirname(current_dir))
        processed_data_dir = os.path.join(ia_root, "data", "processed")
    
    print(f"Using processed data from: {processed_data_dir}")
    
    train_dir = os.path.join(processed_data_dir, "train")
    val_dir = os.path.join(processed_data_dir, "val")
    test_dir = os.path.join(processed_data_dir, "test")
   
    # Check if directories exist
    for directory in [train_dir, val_dir, test_dir]:
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}. Please run data preprocessing first.")
   
    # Vérifier si les sous-répertoires pour les classes existent
    has_subfolders = False
    for directory in [train_dir, val_dir, test_dir]:
        subfolders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
        if not subfolders:
            print(f"Warning: No class subfolders found in {directory}")
        else:
            has_subfolders = True
            print(f"Found classes in {directory}: {subfolders}")
            
    if not has_subfolders:
        raise ValueError("No class subfolders found. Please check your data preprocessing step.")
   
    # Custom preprocessing function for chest X-rays
    def preprocess_input(x):
        # The images have already been preprocessed, just normalize to [-1, 1]
        x = x / 127.5 - 1
        return x
   
    # Enhanced data augmentation for training
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=15,  # Reduced since we already process the images
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )
   
    # Consistent preprocessing for validation and test data
    val_test_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input
    )
   
    # Create generators with class weighting for imbalanced data
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True
    )
   
    validation_generator = val_test_datagen.flow_from_directory(
        val_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )
   
    test_generator = val_test_datagen.flow_from_directory(
        test_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )
   
    # Vérifier si les générateurs ont trouvé des images
    if train_generator.samples == 0 or validation_generator.samples == 0 or test_generator.samples == 0:
        raise ValueError("No images found in one or more directories. Please check your data.")
   
    # Calculate class weights based on the training set
    class_weights = {}
    if hasattr(train_generator, 'class_indices') and hasattr(train_generator, 'classes'):
        class_counts = {}
        for cls in train_generator.classes:
            if cls not in class_counts:
                class_counts[cls] = 0
            class_counts[cls] += 1
       
        # Calculate weights inversely proportional to class frequencies
        if class_counts:  # Vérifier que le dictionnaire n'est pas vide
            max_count = max(class_counts.values())
            for cls, count in class_counts.items():
                class_weights[cls] = max_count / count
        else:
            # Fournir des poids par défaut si aucune classe n'est trouvée
            for i in range(len(train_generator.class_indices)):
                class_weights[i] = 1.0
    else:
        # Fournir des poids par défaut
        for i in range(2):  # Par défaut pour 2 classes (normal/pneumonia)
            class_weights[i] = 1.0
   
    print(f"Found {train_generator.samples} training images")
    print(f"Found {validation_generator.samples} validation images")
    print(f"Found {test_generator.samples} test images")
    print(f"Class weights: {class_weights}")
   
    return train_generator, validation_generator, test_generator, class_weights