import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
from typing import Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class StockDataPreprocessor:
    """Class for preprocessing stock data for LSTM model"""
    
    def __init__(self, sequence_length: int = 60):
        """
        Initialize the preprocessor
        
        Args:
            sequence_length (int): Number of time steps to look back for LSTM
        """
        self.sequence_length = sequence_length
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.is_fitted = False
    
    def fetch_stock_data(self, symbol: str, period: str = "2y") -> pd.DataFrame:
        """
        Fetch stock data from Yahoo Finance
        
        Args:
            symbol (str): Stock symbol (e.g., 'AAPL', 'GOOGL')
            period (str): Time period to fetch ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        
        Returns:
            pd.DataFrame: Stock data with OHLCV columns
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            
            # Reset index to make date a column
            data = data.reset_index()
            
            # Ensure we have the required columns
            required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in data.columns for col in required_columns):
                raise ValueError(f"Missing required columns. Available: {data.columns.tolist()}")
            
            return data
            
        except Exception as e:
            raise Exception(f"Error fetching data for {symbol}: {str(e)}")
    
    def prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """
        Prepare features for LSTM model
        
        Args:
            data (pd.DataFrame): Stock data with OHLCV columns
        
        Returns:
            np.ndarray: Scaled features ready for LSTM
        """
        # Select only the 'Close' price for now (can be extended to include other features)
        features = data[['Close']].values
        
        # Scale the features
        if not self.is_fitted:
            features_scaled = self.scaler.fit_transform(features)
            self.is_fitted = True
        else:
            features_scaled = self.scaler.transform(features)
        
        return features_scaled
    
    def create_sequences(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences for LSTM training
        
        Args:
            data (np.ndarray): Scaled feature data
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: X (input sequences) and y (target values)
        """
        X, y = [], []
        
        for i in range(self.sequence_length, len(data)):
            X.append(data[i-self.sequence_length:i])
            y.append(data[i, 0])  # Predict the next close price
        
        return np.array(X), np.array(y)
    
    def inverse_transform(self, data: np.ndarray) -> np.ndarray:
        """
        Inverse transform scaled data back to original scale
        
        Args:
            data (np.ndarray): Scaled data
        
        Returns:
            np.ndarray: Data in original scale
        """
        if not self.is_fitted:
            raise ValueError("Scaler must be fitted before inverse transform")
        
        # Reshape for inverse transform
        if len(data.shape) == 1:
            data = data.reshape(-1, 1)
        
        return self.scaler.inverse_transform(data)
    
    def prepare_prediction_data(self, data: pd.DataFrame) -> np.ndarray:
        """
        Prepare the most recent data for prediction
        
        Args:
            data (pd.DataFrame): Stock data
        
        Returns:
            np.ndarray: Last sequence_length rows ready for prediction
        """
        features = self.prepare_features(data)
        
        # Get the last sequence_length rows
        last_sequence = features[-self.sequence_length:]
        
        # Reshape for LSTM input (batch_size, sequence_length, features)
        return last_sequence.reshape(1, self.sequence_length, 1)
    
    def get_latest_price(self, data: pd.DataFrame) -> float:
        """
        Get the latest closing price
        
        Args:
            data (pd.DataFrame): Stock data
        
        Returns:
            float: Latest closing price
        """
        return float(data['Close'].iloc[-1])
    
    def get_price_change(self, data: pd.DataFrame, days: int = 1) -> float:
        """
        Calculate price change over specified days
        
        Args:
            data (pd.DataFrame): Stock data
            days (int): Number of days to look back
        
        Returns:
            float: Price change percentage
        """
        if len(data) < days + 1:
            return 0.0
        
        current_price = data['Close'].iloc[-1]
        previous_price = data['Close'].iloc[-1-days]
        
        return ((current_price - previous_price) / previous_price) * 100
