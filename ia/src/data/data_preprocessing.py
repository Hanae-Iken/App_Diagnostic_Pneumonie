import os
import cv2
import numpy as np
import pandas as pd
from pathlib import Path

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Prétraite une image pour ResNet50.
    
    Args:
        image_path: Chemin de l'image
        target_size: Taille cible pour le redimensionnement
        
    Returns:
        Image prétraitée
    """
    # Charger l'image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Impossible de charger l'image: {image_path}")
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Redimensionner
    image = cv2.resize(image, target_size)
    
    # Normaliser pour ResNet50
    image = image / 255.0
    
    return image

def process_dataset(input_dir, output_dir, target_size=(224, 224)):
    """
    Prétraite toutes les images d'un répertoire pour ResNet50.
    
    Args:
        input_dir: Répertoire des images brutes
        output_dir: Répertoire pour les images prétraitées
        target_size: Taille cible pour le redimensionnement
        
    Returns:
        DataFrame avec les métadonnées des images
    """
    os.makedirs(output_dir, exist_ok=True)
    
    metadata = []
    
    # Parcourir les classes (NORMAL, PNEUMONIA)
    for class_name in os.listdir(input_dir):
        class_dir = os.path.join(input_dir, class_name)
        if not os.path.isdir(class_dir):
            continue
            
        output_class_dir = os.path.join(output_dir, class_name)
        os.makedirs(output_class_dir, exist_ok=True)
        
        # Parcourir les images
        for image_file in os.listdir(class_dir):
            if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            input_path = os.path.join(class_dir, image_file)
            output_path = os.path.join(output_class_dir, image_file)
            
            # Prétraiter et sauvegarder l'image
            try:
                processed_image = preprocess_image(input_path, target_size)
                cv2.imwrite(
                    output_path, 
                    cv2.cvtColor((processed_image * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
                )
                
                # Ajouter aux métadonnées
                metadata.append({
                    'filename': image_file,
                    'class': class_name,
                    'label': 1 if class_name == 'PNEUMONIA' else 0,
                    'original_path': input_path,
                    'processed_path': output_path
                })
            except Exception as e:
                print(f"Erreur lors du traitement de {input_path}: {e}")
    
    # Créer un DataFrame avec les métadonnées
    metadata_df = pd.DataFrame(metadata)
    
    return metadata_df

def main():
    # Chemins des répertoires
    base_dir = Path('data')
    raw_data_dir = base_dir / 'raw'
    processed_data_dir = base_dir / 'processed'
    
    # Créer les répertoires nécessaires
    os.makedirs(processed_data_dir, exist_ok=True)
    
    # Prétraiter les ensembles de données
    for dataset in ['train', 'test', 'val']:
        print(f"Prétraitement de l'ensemble {dataset}...")
        input_dir = raw_data_dir / dataset
        output_dir = processed_data_dir / dataset
        
        metadata_df = process_dataset(input_dir, output_dir)
        
        # Sauvegarder les métadonnées
        os.makedirs(base_dir, exist_ok=True)
        metadata_df.to_csv(base_dir / f"{dataset}_metadata.csv", index=False)
        
        print(f"Terminé! {len(metadata_df)} images traitées.")

if __name__ == "__main__":
    main()