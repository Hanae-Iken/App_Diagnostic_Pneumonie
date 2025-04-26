import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model

def create_resnet50_model(input_shape=(224, 224, 3), weights='imagenet'):
    """
    Crée un modèle ResNet50 pour la détection de pneumonie.
    
    Args:
        input_shape: Dimensions des images d'entrée
        weights: Poids pré-entraînés ('imagenet' ou None)
        
    Returns:
        Un modèle Keras compilé
    """
    # Modèle de base ResNet50
    base_model = ResNet50(weights=weights, include_top=False, input_shape=input_shape)
    
    # Geler les couches du modèle de base
    for layer in base_model.layers:
        layer.trainable = False
    
    # Ajouter des couches personnalisées
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    
    # Couche de sortie (classification binaire: normal vs pneumonie)
    predictions = Dense(1, activation='sigmoid')(x)
    
    # Créer le modèle final
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Compiler le modèle
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall(), tf.keras.metrics.AUC()]
    )
    
    return model

def fine_tune_resnet50(model, num_layers_to_unfreeze=30):
    """
    Débloque les dernières couches du modèle ResNet50 pour fine-tuning.
    
    Args:
        model: Modèle ResNet50 pré-entraîné
        num_layers_to_unfreeze: Nombre de couches à débloquer depuis la fin
    """
    # Débloquer les dernières couches
    for layer in model.layers[-num_layers_to_unfreeze:]:
        if hasattr(layer, 'trainable'):
            layer.trainable = True
    
    # Recompiler avec un taux d'apprentissage plus faible
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall(), tf.keras.metrics.AUC()]
    )
    
    return model

def get_last_conv_layer_name(model):
    """
    Récupère le nom de la dernière couche de convolution du modèle ResNet50.
    Utile pour Grad-CAM.
    """
    for i in range(len(model.layers)-1, -1, -1):
        if 'conv' in model.layers[i].name:
            return model.layers[i].name
    return None