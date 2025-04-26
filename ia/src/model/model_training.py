# train_model.py - Script complet pour l'entraînement du modèle
import os
import sys
import argparse
import tensorflow as tf
import matplotlib.pyplot as plt
from pathlib import Path

# Ajouter le répertoire racine au chemin Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Ajoutez le répertoire racine au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.data.data_loader import load_and_augment_training_data, get_class_distribution
from src.model.resnet50_model import create_resnet50_model
# from src.model.model_training import (
#     train_model, 
#     fine_tune_and_train, 
#     evaluate_model, 
#     plot_training_history, 
#     plot_confusion_matrix, 
#     print_classification_report
# )

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Entraînement du modèle ResNet50 pour la détection de pneumonie')
    parser.add_argument('--data_dir', type=str, default='data/processed',
                        help='Répertoire contenant les données prétraitées')
    parser.add_argument('--models_dir', type=str, default='models',
                        help='Répertoire pour sauvegarder les modèles')
    parser.add_argument('--epochs', type=int, default=20,
                        help='Nombre d\'époques pour l\'entraînement initial')
    parser.add_argument('--fine_tune_epochs', type=int, default=10,
                        help='Nombre d\'époques pour le fine-tuning')
    parser.add_argument('--batch_size', type=int, default=32,
                        help='Taille des lots pour l\'entraînement')
    parser.add_argument('--image_size', type=int, default=224,
                        help='Taille des images (côté)')
    return parser.parse_args()

def main():
    # Analyser les arguments
    args = parse_arguments()
    
    # Configuration
    IMAGE_SIZE = (args.image_size, args.image_size)
    BATCH_SIZE = args.batch_size
    EPOCHS = args.epochs
    EPOCHS_FINE_TUNE = args.fine_tune_epochs
    
    # Répertoires de données
    train_dir = os.path.join(args.data_dir, 'train')
    val_dir = os.path.join(args.data_dir, 'val')
    test_dir = os.path.join(args.data_dir, 'test')
    
    # Créer les répertoires pour les modèles
    os.makedirs(args.models_dir, exist_ok=True)
    checkpoint_dir = os.path.join(args.models_dir, 'checkpoints')
    os.makedirs(checkpoint_dir, exist_ok=True)
    
    # Vérifier la distribution des classes
    print("Distribution des classes:")
    print("Entraînement:", get_class_distribution(train_dir))
    print("Validation:", get_class_distribution(val_dir))
    print("Test:", get_class_distribution(test_dir))
    
    # Charger les données
    print("Chargement des données...")
    train_generator, val_generator = load_and_augment_training_data(
        train_dir, val_dir, 
        target_size=IMAGE_SIZE, 
        batch_size=BATCH_SIZE
    )
    
    # Générateur de test sans augmentation
    test_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255).flow_from_directory(
        test_dir,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        shuffle=False
    )
    
    # Créer le modèle
    print("Création du modèle ResNet50...")
    model = create_resnet50_model(input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3))
    model.summary()
    
    # Entraînement initial
    print(f"Démarrage de l'entraînement initial ({EPOCHS} époques)...")
    history = train_model(
        model, 
        train_generator, 
        val_generator, 
        epochs=EPOCHS,
        checkpoint_dir=checkpoint_dir,
        model_name='resnet50_base'
    )
    
    # Sauvegarder le modèle de base
    base_model_path = os.path.join(args.models_dir, 'resnet50_base.h5')
    model.save(base_model_path)
    print(f"Modèle de base sauvegardé à {base_model_path}")
    
    # Visualiser les résultats d'entraînement
    plot_training_history(history)
    
    # Fine-tuning
    print(f"Démarrage du fine-tuning ({EPOCHS_FINE_TUNE} époques)...")
    fine_tuned_model, history_fine_tune = fine_tune_and_train(
        model,
        train_generator,
        val_generator,
        fine_tune_epochs=EPOCHS_FINE_TUNE,
        checkpoint_dir=checkpoint_dir,
        model_name='resnet50_finetune'
    )
    
    # Sauvegarder le modèle final
    final_model_path = os.path.join(args.models_dir, 'resnet50_finetune.h5')
    fine_tuned_model.save(final_model_path)
    print(f"Modèle après fine-tuning sauvegardé à {final_model_path}")
    
    # Visualiser les résultats du fine-tuning
    plot_training_history(history_fine_tune)
    
    # Évaluation sur l'ensemble de test
    print("Évaluation sur l'ensemble de test...")
    test_results, predictions, predictions_binary, true_labels = evaluate_model(
        fine_tuned_model, 
        test_generator
    )
    
    # Afficher les métriques
    print(f"Résultats du test - Perte: {test_results[0]:.4f}, Précision: {test_results[1]:.4f}")
    if len(test_results) > 2:
        print(f"Precision: {test_results[2]:.4f}, Recall: {test_results[3]:.4f}, AUC: {test_results[4]:.4f}")
    
    # Afficher la matrice de confusion
    cm = plot_confusion_matrix(true_labels, predictions_binary)
    
    # Afficher le rapport de classification
    report = print_classification_report(true_labels, predictions_binary)
    
    # Sauvegarder les métriques
    metrics_path = os.path.join(args.models_dir, 'evaluation_metrics.txt')
    with open(metrics_path, 'w') as f:
        f.write(f"Perte: {test_results[0]:.4f}\n")
        f.write(f"Précision: {test_results[1]:.4f}\n")
        if len(test_results) > 2:
            f.write(f"Precision: {test_results[2]:.4f}\n")
            f.write(f"Recall: {test_results[3]:.4f}\n")
            f.write(f"AUC: {test_results[4]:.4f}\n")
        f.write("\nMatrice de confusion:\n")
        f.write(str(cm))
        f.write("\n\nRapport de classification:\n")
        f.write(report)
    
    print(f"Métriques d'évaluation sauvegardées à {metrics_path}")
    print("Entraînement et évaluation terminés avec succès!")

if __name__ == "__main__":
    main()