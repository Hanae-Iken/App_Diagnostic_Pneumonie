import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def create_data_generators(batch_size=32, img_size=(224, 224)):
    """
    Create train, validation, and test data generators for pneumonia dataset
    with enhanced augmentation and preprocessing
    
    Args:
        batch_size (int): Batch size for training
        img_size (tuple): Image size for model input
        
    Returns:
        tuple: (train_generator, validation_generator, test_generator)
    """
    # Path to the dataset
    data_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
    train_dir = os.path.join(data_dir, "train")
    val_dir = os.path.join(data_dir, "val")
    test_dir = os.path.join(data_dir, "test")
    
    # Check if directories exist
    for directory in [train_dir, val_dir, test_dir]:
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory not found: {directory}. Please ensure the dataset is correctly placed.")
    
    # Custom preprocessing function for chest X-rays
    def preprocess_input(x):
        # Apply standard preprocessing (rescale to [-1, 1])
        x = x / 127.5 - 1
        return x
    
    # Enhanced data augmentation for training
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        brightness_range=[0.8, 1.2],
        channel_shift_range=0.1
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
    
    # Calculate class weights based on the training set
    class_weights = {}
    if hasattr(train_generator, 'class_indices') and hasattr(train_generator, 'classes'):
        total_samples = len(train_generator.classes)
        class_counts = {}
        for cls in train_generator.classes:
            if cls not in class_counts:
                class_counts[cls] = 0
            class_counts[cls] += 1
        
        # Calculate weights inversely proportional to class frequencies
        max_count = max(class_counts.values())
        for cls, count in class_counts.items():
            class_weights[cls] = max_count / count
    
    print(f"Found {train_generator.samples} training images")
    print(f"Found {validation_generator.samples} validation images")
    print(f"Found {test_generator.samples} test images")
    
    return train_generator, validation_generator, test_generator, class_weights