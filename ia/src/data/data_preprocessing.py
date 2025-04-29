#src/data/data_preprocessing.py
import os
import cv2
import numpy as np
from tqdm import tqdm
import shutil

class DataPreprocessor:
    def __init__(self, raw_data_dir, processed_data_dir, img_size=224):
        """
        Initialize the data preprocessor
        
        Args:
            raw_data_dir (str): Directory containing raw data
            processed_data_dir (str): Directory where processed data will be saved
            img_size (int): Size to which images will be resized
        """
        self.raw_data_dir = raw_data_dir
        self.processed_data_dir = processed_data_dir
        self.img_size = img_size
        self.labels = ['NORMAL', 'PNEUMONIA']
        
    def create_directory_structure(self):
        """Create the directory structure for processed data"""
        for split in ['train', 'val', 'test']:
            for label in self.labels:
                os.makedirs(os.path.join(self.processed_data_dir, split, label), exist_ok=True)
    
    def preprocess_and_save(self):
        """Preprocess images and save them to the processed directory"""
        self.create_directory_structure()
        
        for split in ['train', 'val', 'test']:
            split_dir = os.path.join(self.raw_data_dir, split)
            
            if not os.path.exists(split_dir):
                print(f"Warning: {split_dir} does not exist. Skipping.")
                continue
                
            for label in self.labels:
                label_dir = os.path.join(split_dir, label)
                
                if not os.path.exists(label_dir):
                    print(f"Warning: {label_dir} does not exist. Skipping.")
                    continue
                
                output_dir = os.path.join(self.processed_data_dir, split, label)
                
                # Process all images in the directory
                img_files = os.listdir(label_dir)
                for img_file in tqdm(img_files, desc=f"Processing {split}/{label}"):
                    try:
                        img_path = os.path.join(label_dir, img_file)
                        if not os.path.isfile(img_path):
                            continue
                            
                        # Read and preprocess image
                        img = cv2.imread(img_path)
                        if img is None:
                            continue
                            
                        # Apply preprocessing
                        processed_img = self._preprocess_image(img)
                        
                        # Save processed image
                        output_path = os.path.join(output_dir, img_file)
                        cv2.imwrite(output_path, processed_img)
                    
                    except Exception as e:
                        print(f"Error processing {img_file}: {e}")
    
    def _preprocess_image(self, img):
        """
        Apply preprocessing to an image
        
        Args:
            img (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Preprocessed image
        """
        # Convert to grayscale
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # clahe_img = clahe.apply(gray)
        
        # Resize to target size
        resized = cv2.resize(img, (self.img_size, self.img_size))
        
        # Optional: Normalize pixel values to [0, 255]
        # normalized = cv2.normalize(resized, None, 0, 255, cv2.NORM_MINMAX)
        
        return resized
    
    def balance_classes(self, max_samples_per_class=None):
        """
        Balance classes by under-sampling the majority class
        
        Args:
            max_samples_per_class (int, optional): Maximum number of samples per class
        """
        for split in ['train', 'val', 'test']:
            split_dir = os.path.join(self.processed_data_dir, split)
            
            if not os.path.exists(split_dir):
                continue
                
            # Count samples per class
            class_counts = {}
            for label in self.labels:
                label_dir = os.path.join(split_dir, label)
                if os.path.exists(label_dir):
                    class_counts[label] = len(os.listdir(label_dir))
            
            # Determine target count
            if max_samples_per_class:
                target_count = max_samples_per_class
            else:
                target_count = min(class_counts.values())
            
            # Balance classes
            for label, count in class_counts.items():
                if count > target_count:
                    label_dir = os.path.join(split_dir, label)
                    files = os.listdir(label_dir)
                    files_to_remove = np.random.choice(files, size=count-target_count, replace=False)
                    
                    for file in files_to_remove:
                        os.remove(os.path.join(label_dir, file))
                    
                    print(f"Balanced {split}/{label}: {count} -> {target_count} images")