import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
import os
from .data_preprocessing import StockDataPreprocessor
from .lstm_model import LSTMModel
import warnings
warnings.filterwarnings('ignore')


class StockPredictor:
    """Main class for stock price prediction using LSTM"""
    
    def __init__(self, sequence_length: int = 60):
        """
        Initialize the stock predictor
        
        Args:
            sequence_length (int): Number of time steps to look back
        """
        self.sequence_length = sequence_length
        self.preprocessor = StockDataPreprocessor(sequence_length)
        self.lstm_model = LSTMModel(sequence_length)
        self.is_trained = False
        
        # Try to load pre-trained model
        self._load_existing_model()
    
    def _load_existing_model(self):
        """Try to load existing trained model"""
        try:
            if self.lstm_model.load_model():
                # Load the corresponding scaler
                scaler = self.lstm_model.load_scaler()
                if scaler is not None:
                    self.preprocessor.scaler = scaler
                    self.preprocessor.is_fitted = True
                    self.is_trained = True
                    print("Pre-trained model loaded successfully")
        except Exception as e:
            print(f"Could not load existing model: {str(e)}")
    
    def train_model(self, symbol: str, period: str = "2y", 
                   train_split: float = 0.8, epochs: int = 50) -> Dict:
        """
        Train the LSTM model on stock data
        
        Args:
            symbol (str): Stock symbol to train on
            period (str): Time period for training data
            train_split (float): Fraction of data to use for training
            epochs (int): Number of training epochs
        
        Returns:
            Dict: Training results and metrics
        """
        try:
            print(f"Fetching data for {symbol}...")
            data = self.preprocessor.fetch_stock_data(symbol, period)
            
            if len(data) < self.sequence_length * 2:
                raise ValueError(f"Insufficient data for {symbol}. Need at least {self.sequence_length * 2} data points")
            
            print(f"Preparing features...")
            features_scaled = self.preprocessor.prepare_features(data)
            
            print(f"Creating sequences...")
            X, y = self.preprocessor.create_sequences(features_scaled)
            
            # Split data into train and validation sets
            split_idx = int(len(X) * train_split)
            X_train, X_val = X[:split_idx], X[split_idx:]
            y_train, y_val = y[:split_idx], y[split_idx:]
            
            print(f"Training LSTM model...")
            print(f"Training samples: {len(X_train)}, Validation samples: {len(X_val)}")
            
            # Train the model
            history = self.lstm_model.train(
                X_train, y_train, X_val, y_val, epochs=epochs
            )
            
            # Evaluate on validation set
            metrics = self.lstm_model.evaluate(X_val, y_val)
            
            # Save the trained model and scaler
            self.lstm_model.save_model(scaler=self.preprocessor.scaler)
            
            self.is_trained = True
            
            return {
                'status': 'success',
                'symbol': symbol,
                'training_samples': len(X_train),
                'validation_samples': len(X_val),
                'history': history,
                'metrics': metrics,
                'message': f'Model trained successfully on {symbol} data'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Training failed: {str(e)}'
            }
    
    def predict_stock_price(self, symbol: str, days_ahead: int = 1) -> Dict:
        """
        Predict stock price for a given symbol
        
        Args:
            symbol (str): Stock symbol to predict
            days_ahead (int): Number of days ahead to predict
        
        Returns:
            Dict: Prediction results
        """
        try:
            if not self.is_trained:
                return {
                    'status': 'error',
                    'message': 'Model not trained. Please train the model first.'
                }
            
            print(f"Fetching latest data for {symbol}...")
            data = self.preprocessor.fetch_stock_data(symbol, "3mo")
            
            if len(data) < self.sequence_length:
                raise ValueError(f"Insufficient data for {symbol}")
            
            # Get current price
            current_price = self.preprocessor.get_latest_price(data)
            
            # Prepare data for prediction
            prediction_data = self.preprocessor.prepare_prediction_data(data)
            
            # Make prediction
            print(f"Making prediction...")
            prediction_scaled = self.lstm_model.predict(prediction_data)
            
            # Convert back to original scale
            prediction = self.preprocessor.inverse_transform(prediction_scaled)[0, 0]
            
            # Calculate confidence (simple approach - can be enhanced)
            confidence = 0.85  # Placeholder confidence score
            
            # Calculate price change
            price_change = ((prediction - current_price) / current_price) * 100
            
            return {
                'status': 'success',
                'symbol': symbol,
                'current_price': round(current_price, 2),
                'predicted_price': round(prediction, 2),
                'price_change': round(price_change, 2),
                'confidence': round(confidence, 3),
                'prediction_date': data['Date'].iloc[-1].strftime('%Y-%m-%d'),
                'message': f'Prediction completed for {symbol}'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Prediction failed: {str(e)}'
            }
    
    def get_stock_info(self, symbol: str) -> Dict:
        """
        Get basic stock information
        
        Args:
            symbol (str): Stock symbol
        
        Returns:
            Dict: Stock information
        """
        try:
            data = self.preprocessor.fetch_stock_data(symbol, "1mo")
            
            current_price = self.preprocessor.get_latest_price(data)
            price_change_1d = self.preprocessor.get_price_change(data, 1)
            price_change_7d = self.preprocessor.get_price_change(data, 7)
            price_change_30d = self.preprocessor.get_price_change(data, 30)
            
            return {
                'status': 'success',
                'symbol': symbol,
                'current_price': round(current_price, 2),
                'price_change_1d': round(price_change_1d, 2),
                'price_change_7d': round(price_change_7d, 2),
                'price_change_30d': round(price_change_30d, 2),
                'volume': int(data['Volume'].iloc[-1]),
                'last_updated': data['Date'].iloc[-1].strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to get stock info: {str(e)}'
            }
    
    def batch_predict(self, symbols: list, days_ahead: int = 1) -> Dict:
        """
        Make predictions for multiple symbols
        
        Args:
            symbols (list): List of stock symbols
            days_ahead (int): Number of days ahead to predict
        
        Returns:
            Dict: Batch prediction results
        """
        results = {}
        
        for symbol in symbols:
            print(f"Processing {symbol}...")
            result = self.predict_stock_price(symbol, days_ahead)
            results[symbol] = result
        
        return {
            'status': 'success',
            'results': results,
            'total_symbols': len(symbols)
        }
    
    def get_model_status(self) -> Dict:
        """
        Get current model status
        
        Returns:
            Dict: Model status information
        """
        return {
            'is_trained': self.is_trained,
            'sequence_length': self.sequence_length,
            'model_loaded': self.lstm_model.model is not None,
            'scaler_loaded': self.preprocessor.is_fitted
        }
