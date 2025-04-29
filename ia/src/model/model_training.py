# src/model/model_training.py
import os
import argparse
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard
from tensorflow.keras.metrics import AUC, Precision, Recall
import datetime

from .model_trainer import PneumoniaModelTrainer
from .resnet50_model import ResNet50Model
from ..data.data_loader import create_data_generators

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Train ResNet50 model for pneumonia detection')
    parser.add_argument('--base_model', type=str, default=None,
                      help='Path to pre-trained model to continue training')
    parser.add_argument('--batch_size', type=int, default=16,
                      help='Batch size for training')
    parser.add_argument('--img_size', type=int, default=224,
                      help='Image size for model input')
    parser.add_argument('--epochs', type=int, default=5, # Reduced from 50 to 5 for testing
                      help='Number of epochs for each training phase')
    parser.add_argument('--lr', type=float, default=5e-5,
                      help='Initial learning rate')
    parser.add_argument('--fine_tune', action='store_true', default=False, # Changed to False for initial testing
                      help='Whether to perform fine-tuning after base training')
    parser.add_argument('--unfreeze_layers', type=int, default=50,
                      help='Number of layers to unfreeze during fine-tuning')
    return parser.parse_args()

def train_model(args=None):
    """Function to train the model with given arguments"""
    if args is None:
        args = parse_args()
    
    print("Starting pneumonia detection model training...")
    print(f"Batch size: {args.batch_size}, Image size: {args.img_size}x{args.img_size}")
    
    # Disable mixed precision to avoid Cast layer issues
    # policy = tf.keras.mixed_precision.Policy('mixed_float16')
    # tf.keras.mixed_precision.set_global_policy(policy)
    
    # Create models directory if it doesn't exist
    models_dir = os.path.join(os.path.dirname(__file__), "../../../models")
    os.makedirs(models_dir, exist_ok=True)
    
    # Create logs directory for TensorBoard
    log_dir = os.path.join(os.path.dirname(__file__), "../../../logs", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    os.makedirs(log_dir, exist_ok=True)
    
    # Create data generators with class weights
    train_gen, val_gen, test_gen, class_weights = create_data_generators(
        batch_size=args.batch_size, 
        img_size=(args.img_size, args.img_size)
    )
    
    # Initialize and build model
    if args.base_model and os.path.exists(args.base_model):
        print(f"Loading model from {args.base_model}")
        model = tf.keras.models.load_model(args.base_model)
    else:
        print("Creating new ResNet50 model")
        resnet_model = ResNet50Model(
            input_shape=(args.img_size, args.img_size, 3),
            num_classes=len(train_gen.class_indices)
        )
        model = resnet_model.build(trainable_base=False)
    
    # Create model trainer
    trainer = PneumoniaModelTrainer(
        model=model,
        train_gen=train_gen,
        val_gen=val_gen,
        test_gen=test_gen
    )
    
    # Compile model with additional metrics
    trainer.compile_model(
        optimizer=Adam(learning_rate=args.lr),
        loss='categorical_crossentropy',
        metrics=['accuracy', AUC(), Precision(), Recall()]
    )
    
    # Create callbacks for base model
    base_model_path = os.path.join(models_dir, "resnet50_base.keras")
    callbacks = [
        ModelCheckpoint(
            base_model_path,
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=5,  # Reduced from 15 to 5 for faster testing
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=3,  # Reduced from 7 to 3 for faster testing
            min_lr=1e-7,
            verbose=1
        ),
        TensorBoard(
            log_dir=log_dir,
            histogram_freq=1,
            update_freq='epoch'
        )
    ]
    
    # Train base model with class weights
    print("Training base model...")
    history = trainer.train(
        epochs=args.epochs,
        callbacks=callbacks,
        class_weights=class_weights
    )
    
    # Evaluate the model
    trainer.evaluate()
    
    # Plot training history
    history_plot_path = os.path.join(models_dir, "base_model_history.png")
    trainer.plot_training_history(save_path=history_plot_path)
    
    # Load the best model
    try:
        model = trainer.load_model(base_model_path)
        
        # Fine-tune if requested
        if args.fine_tune:
            print(f"Fine-tuning model by unfreezing {args.unfreeze_layers} layers...")
            
            # Unfreeze top layers for fine-tuning
            if not args.base_model:  # Only if we started with a new model
                resnet_model = ResNet50Model(
                    input_shape=(args.img_size, args.img_size, 3),
                    num_classes=len(train_gen.class_indices)
                )
                resnet_model.model = model
                model = resnet_model.unfreeze_top_layers(num_layers=args.unfreeze_layers)
            
            # Create trainer with fine-tuned model
            trainer = PneumoniaModelTrainer(
                model=model,
                train_gen=train_gen,
                val_gen=val_gen,
                test_gen=test_gen
            )
            
            # Compile with lower learning rate
            trainer.compile_model(
                optimizer=Adam(learning_rate=args.lr/10),
                loss='categorical_crossentropy',
                metrics=['accuracy', AUC(), Precision(), Recall()]
            )
            
            # Create callbacks for fine-tuned model
            finetune_model_path = os.path.join(models_dir, "resnet50_finetune.keras")
            callbacks[0] = ModelCheckpoint(
                finetune_model_path,
                monitor='val_accuracy',
                save_best_only=True,
                mode='max',
                verbose=1
            )
            
            # Train fine-tuned model with class weights
            history = trainer.train(
                epochs=args.epochs,
                callbacks=callbacks,
                class_weights=class_weights
            )
            
            # Evaluate the model
            trainer.evaluate()
            
            # Plot training history
            history_plot_path = os.path.join(models_dir, "finetune_model_history.png")
            trainer.plot_training_history(save_path=history_plot_path)
    
        print("Training completed successfully!")
    except Exception as e:
        print(f"An error occurred while loading the best model or fine-tuning: {e}")
        # Continue with the current model in memory
        print("Continuing with the current model...")
    
    return trainer, model

def main():
    """Main function to run the script"""
    args = parse_args()
    train_model(args)

if __name__ == "__main__":
    main()