import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cv2

def get_img_array(img_path, target_size):
    """
    Charge et prétraite une image pour ResNet50.
    """
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, target_size)
    img = img / 255.0
    img_array = np.expand_dims(img, axis=0)
    return img_array, img

def make_gradcam_heatmap(img_array, model, last_conv_layer_name):
    """
    Génère une carte de chaleur Grad-CAM pour visualiser les zones importantes.
    """
    # Modèle pour extraire la dernière couche de convolution et les prédictions
    grad_model = tf.keras.models.Model(
        [model.inputs], 
        [model.get_layer(last_conv_layer_name).output, model.output]
    )
    
    # Enregistrer le gradient de la sortie par rapport à la dernière couche de convolution
    with tf.GradientTape() as tape:
        conv_output, preds = grad_model(img_array)
        # Pour une classification binaire (pneumonie vs normal)
        class_channel = preds[:, 0]
    
    # Gradient de la classe par rapport à la sortie de la dernière couche de convolution
    grads = tape.gradient(class_channel, conv_output)
    
    # Moyenne des gradients
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # Multiplier les gradients par la sortie de la dernière couche de convolution
    conv_output = conv_output[0]
    heatmap = conv_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    
    # Normaliser la carte de chaleur
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    
    return heatmap.numpy()

def display_gradcam(img_path, heatmap, cam_path="gradcam.jpg", alpha=0.4):
    """
    Superpose la carte de chaleur Grad-CAM sur l'image originale.
    """
    # Charger l'image originale
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = img.shape
    
    # Redimensionner la carte de chaleur à la taille de l'image originale
    heatmap = cv2.resize(heatmap, (width, height))
    
    # Convertir la carte de chaleur en RGB
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    
    # Superposer la carte de chaleur sur l'image originale
    superimposed_img = heatmap * alpha + img
    superimposed_img = np.clip(superimposed_img, 0, 255).astype("uint8")
    
    # Afficher l'image originale et la carte de chaleur
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))
    ax[0].imshow(img)
    ax[0].set_title('Image originale')
    ax[0].axis('off')
    
    ax[1].imshow(superimposed_img)
    ax[1].set_title('Carte de chaleur Grad-CAM')
    ax[1].axis('off')
    
    plt.tight_layout()
    plt.savefig(cam_path)
    plt.show()
    
    return superimposed_img