from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.metrics import AUC, Precision, Recall

def build_model(input_shape=(224, 224, 3), dropout_rate=0.5, dense_units=128):
    """
    Construit un modèle CNN basé sur ResNet50 avec transfert learning.
    """
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
    base_model.trainable = False  # On commence avec les poids gelés

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(dropout_rate)(x)
    x = Dense(dense_units, activation='relu')(x)
    x = Dropout(0.3)(x)
    predictions = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    return model

def get_metrics():
    return ['accuracy', AUC(name='auc'), Precision(name='precision'), Recall(name='recall')]