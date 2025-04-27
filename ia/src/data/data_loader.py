import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def create_data_generators(batch_size=32, img_size=(224, 224)):
    """
    Create train, validation, and test data generators for pneumonia dataset
    
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
    
    # Data augmentation for training
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
    
    # Only rescaling for validation and test
    val_test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Create generators
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
    
    print(f"Found {train_generator.samples} training images")
    print(f"Found {validation_generator.samples} validation images")
    print(f"Found {test_generator.samples} test images")
    
    return train_generator, validation_generator, test_generator