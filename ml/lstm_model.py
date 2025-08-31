import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import os
import joblib
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class LSTMModel:
    """LSTM model for stock price prediction"""
    
    def __init__(self, sequence_length: int = 60, features: int = 1):
        """
        Initialize LSTM model
        
        Args:
            sequence_length (int): Number of time steps to look back
            features (int): Number of features (1 for close price only)
        """
        self.sequence_length = sequence_length
        self.features = features
        self.model = None
        self.model_path = 'ml/saved_models/lstm_model.h5'
        self.scaler_path = 'ml/saved_models/scaler.pkl'
        
        # Create directory for saved models
        os.makedirs('ml/saved_models', exist_ok=True)
    
    def build_model(self, lstm_units: int = 50, dropout_rate: float = 0.2) -> Sequential:
        """
        Build the LSTM model architecture
        
        Args:
            lstm_units (int): Number of LSTM units
            dropout_rate (float): Dropout rate for regularization
        
        Returns:
            Sequential: Compiled LSTM model
        """
        model = Sequential([
            LSTM(units=lstm_units, return_sequences=True, 
                 input_shape=(self.sequence_length, self.features)),
            Dropout(dropout_rate),
            
            LSTM(units=lstm_units, return_sequences=True),
            Dropout(dropout_rate),
            
            LSTM(units=lstm_units, return_sequences=False),
            Dropout(dropout_rate),
            
            Dense(units=25),
            Dense(units=1)
        ])
        
        # Compile the model
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mean_squared_error',
            metrics=['mae']
        )
        
        return model
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, 
              X_val: np.ndarray = None, y_val: np.ndarray = None,
              epochs: int = 100, batch_size: int = 32) -> dict:
        """
        Train the LSTM model
        
        Args:
            X_train (np.ndarray): Training input sequences
            y_train (np.ndarray): Training target values
            X_val (np.ndarray): Validation input sequences
            y_val (np.ndarray): Validation target values
            epochs (int): Number of training epochs
            batch_size (int): Batch size for training
        
        Returns:
            dict: Training history
        """
        # Build the model
        self.model = self.build_model()
        
        # Prepare validation data
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
        
        # Callbacks for better training
        callbacks = [
            EarlyStopping(
                monitor='val_loss' if validation_data else 'loss',
                patience=15,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss' if validation_data else 'loss',
                factor=0.5,
                patience=10,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        # Train the model
        history = self.model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        return history.history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions using the trained model
        
        Args:
            X (np.ndarray): Input sequences for prediction
        
        Returns:
            np.ndarray: Predicted values
        """
        if self.model is None:
            raise ValueError("Model must be trained or loaded before making predictions")
        
        return self.model.predict(X, verbose=0)
    
    def save_model(self, model_path: str = None, scaler=None):
        """
        Save the trained model and scaler
        
        Args:
            model_path (str): Path to save the model
            scaler: Scaler object to save
        """
        if model_path is None:
            model_path = self.model_path
        
        # Save the model
        if self.model is not None:
            self.model.save(model_path)
            print(f"Model saved to {model_path}")
        
        # Save the scaler
        if scaler is not None:
            joblib.dump(scaler, self.scaler_path)
            print(f"Scaler saved to {self.scaler_path}")
    
    def load_model(self, model_path: str = None) -> bool:
        """
        Load a pre-trained model
        
        Args:
            model_path (str): Path to the saved model
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        if model_path is None:
            model_path = self.model_path
        
        try:
            if os.path.exists(model_path):
                self.model = load_model(model_path)
                print(f"Model loaded from {model_path}")
                return True
            else:
                print(f"No saved model found at {model_path}")
                return False
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False
    
    def load_scaler(self, scaler_path: str = None):
        """
        Load a saved scaler
        
        Args:
            scaler_path (str): Path to the saved scaler
        
        Returns:
            Scaler object or None if loading fails
        """
        if scaler_path is None:
            scaler_path = self.scaler_path
        
        try:
            if os.path.exists(scaler_path):
                return joblib.load(scaler_path)
            else:
                print(f"No saved scaler found at {scaler_path}")
                return None
        except Exception as e:
            print(f"Error loading scaler: {str(e)}")
            return None
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> dict:
        """
        Evaluate the model performance
        
        Args:
            X_test (np.ndarray): Test input sequences
            y_test (np.ndarray): Test target values
        
        Returns:
            dict: Evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model must be trained or loaded before evaluation")
        
        # Make predictions
        y_pred = self.predict(X_test)
        
        # Calculate metrics
        mse = np.mean((y_test - y_pred.flatten()) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_test - y_pred.flatten()))
        
        # Calculate percentage error
        mape = np.mean(np.abs((y_test - y_pred.flatten()) / y_test)) * 100
        
        return {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'mape': mape
        }
    
    def get_model_summary(self) -> str:
        """
        Get model architecture summary
        
        Returns:
            str: Model summary as string
        """
        if self.model is None:
            return "No model built yet"
        
        # Capture model summary
        summary_list = []
        self.model.summary(print_fn=lambda x: summary_list.append(x))
        return '\n'.join(summary_list)
