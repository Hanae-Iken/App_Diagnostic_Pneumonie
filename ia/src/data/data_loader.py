# src/data/data_loader.py
import os
import numpy as np
import pandas as pd
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical

class PneumoniaDataLoader:
    def __init__(self, data_dir, img_size=224, batch_size=32):
        """
        Initialize the data loader for pneumonia detection project
        
        Args:
            data_dir (str): Base directory containing the data
            img_size (int): Size to which images will be resized
            batch_size (int): Batch size for training/validation/testing
        """
        self.data_dir = data_dir
        self.img_size = img_size
        self.batch_size = batch_size
        self.labels = ['NORMAL', 'PNEUMONIA']
        
    def get_data_generators(self):
        """
        Create data generators for training, validation, and testing
        
        Returns:
            tuple: (train_generator, valid_generator, test_generator)
        """
        # Data augmentation for training data
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            horizontal_flip=True,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            fill_mode='nearest'
        )
        
        # Only rescaling for validation and test data
        valid_test_datagen = ImageDataGenerator(rescale=1./255)
        
        # Create generators
        train_generator = train_datagen.flow_from_directory(
            os.path.join(self.data_dir, 'train'),
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=True,
            color_mode='rgb'
        )
        
        valid_generator = valid_test_datagen.flow_from_directory(
            os.path.join(self.data_dir, 'val'),
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False,
            color_mode='rgb'
        )
        
        test_generator = valid_test_datagen.flow_from_directory(
            os.path.join(self.data_dir, 'test'),
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False,
            color_mode='rgb'
        )
        
        return train_generator, valid_generator, test_generator
    
    def load_raw_data(self):
        """
        Load raw image data for exploration and custom preprocessing
        
        Returns:
            dict: Dictionary containing train, validation, and test data with labels
        """
        data = {
            'train': self._load_dataset_from_folder(os.path.join(self.data_dir, 'train')),
            'val': self._load_dataset_from_folder(os.path.join(self.data_dir, 'val')),
            'test': self._load_dataset_from_folder(os.path.join(self.data_dir, 'test'))
        }
        return data
    
    def _load_dataset_from_folder(self, folder_path):
        """
        Helper method to load images from a folder
        
        Args:
            folder_path (str): Path to the folder containing class subfolders
            
        Returns:
            list: List of [image_array, class_index] pairs
        """
        data = []
        for label in self.labels:
            class_path = os.path.join(folder_path, label)
            class_index = self.labels.index(label)
            
            if not os.path.exists(class_path):
                continue
                
            for img_name in os.listdir(class_path):
                try:
                    img_path = os.path.join(class_path, img_name)
                    img = cv2.imread(img_path)
                    
                    if img is None:
                        continue
                        
                    # Convert BGR to RGB
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    
                    # Resize image
                    img = cv2.resize(img, (self.img_size, self.img_size))
                    
                    data.append([img, class_index])
                except Exception as e:
                    print(f"Error processing {img_name}: {e}")
        
        return data