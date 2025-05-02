# Rapport de modèle ResNet50 pour la détection de pneumonie

## Architecture du modèle

Ce projet utilise un modèle ResNet50 préentraîné sur ImageNet, modifié pour la classification binaire des radiographies pulmonaires (normal vs pneumonie). ResNet50 a été choisi pour sa grande capacité à apprendre des caractéristiques complexes grâce à sa profondeur, tout en évitant le problème de dégradation du gradient grâce à ses connexions résiduelles.

### Modifications apportées au ResNet50 standard

1. **Transfer Learning** : Nous utilisons les poids préentraînés sur ImageNet comme point de départ
2. **Couche de classification personnalisée** : Remplacement de la couche de sortie par une architecture adaptée à notre problème binaire
3. **Fine-tuning** : Dégel progressif des couches supérieures pour l'adaptation aux radiographies

### Schéma de l'architecture

```
ResNet50 (poids ImageNet) → GlobalAveragePooling2D → Dense(512, ReLU) → Dropout(0.5) → Dense(1, Sigmoid)
```

## Prétraitement des données

Les images subissent plusieurs transformations avant d'être utilisées pour l'entraînement :

1. Redimensionnement à 224×224 pixels (taille d'entrée standard pour ResNet50)
2. Normalisation des valeurs de pixels entre 0 et 1
3. Augmentation de données pendant l'entraînement :



## Interprétabilité avec GradCAM

GradCAM (Gradient-weighted Class Activation Mapping) est utilisé pour visualiser les zones de l'image qui ont le plus influencé la décision du modèle.

Observations clés de la visualisation GradCAM :
- Pour les cas de pneumonie, le modèle se concentre généralement sur les zones d'opacité pulmonaire
- Pour les cas normaux, l'attention est plus diffuse ou se concentre sur les structures normales des poumons
- La visualisation confirme que le modèle base ses décisions sur des caractéristiques anatomiquement pertinentes

## Limites et considérations

1. **Biais de données** : Le modèle a été entraîné sur un ensemble de données spécifique qui peut ne pas représenter toutes les variations de pneumonie dans différentes populations ou contextes cliniques
2. **Sensibilité à la qualité d'image** : La performance peut diminuer sur des radiographies de faible qualité ou prises avec des équipements différents
3. **Distinction des pathologies** : Le modèle différencie uniquement "normal" vs "pneumonie" et ne distingue pas entre différents types de pneumonie ou d'autres pathologies pulmonaires
4. **Outil d'aide à la décision** : Ce système doit être utilisé comme support au diagnostic et non comme remplacement de l'expertise d'un radiologue
