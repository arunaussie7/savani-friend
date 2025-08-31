import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Dict, List, Optional
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set matplotlib backend to Agg for non-interactive environments
plt.switch_backend('Agg')

# Set style
plt.style.use('default')


class StockVisualizer:
    """Class for creating stock price visualizations"""
    
    def __init__(self, output_dir: str = 'static/images'):
        """
        Initialize the visualizer
        
        Args:
            output_dir (str): Directory to save generated plots
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set figure size and DPI for better quality
        self.figsize = (12, 8)
        self.dpi = 100
        
        # Color scheme
        self.colors = {
            'actual': '#1f77b4',
            'predicted': '#ff7f0e',
            'background': '#f8f9fa',
            'grid': '#e9ecef',
            'text': '#212529'
        }
    
    def plot_actual_vs_predicted(self, actual_prices: List[float], 
                                predicted_prices: List[float],
                                dates: List[str],
                                symbol: str,
                                save_plot: bool = True) -> str:
        """
        Create actual vs predicted price comparison plot
        
        Args:
            actual_prices (List[float]): List of actual prices
            predicted_prices (List[float]): List of predicted prices
            dates (List[str]): List of dates
            symbol (str): Stock symbol
            save_plot (bool): Whether to save the plot
        
        Returns:
            str: Path to saved plot or plot data
        """
        try:
            # Create figure and axis
            fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
            
            # Convert dates to datetime if they're strings
            if isinstance(dates[0], str):
                dates = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
            
            # Plot actual vs predicted
            ax.plot(dates, actual_prices, 
                   color=self.colors['actual'], 
                   linewidth=2, 
                   label='Actual Price', 
                   marker='o', 
                   markersize=4)
            
            ax.plot(dates, predicted_prices, 
                   color=self.colors['predicted'], 
                   linewidth=2, 
                   label='Predicted Price', 
                   marker='s', 
                   markersize=4)
            
            # Customize the plot
            ax.set_title(f'{symbol} Stock Price: Actual vs Predicted', 
                        fontsize=16, fontweight='bold', color=self.colors['text'])
            ax.set_xlabel('Date', fontsize=12, color=self.colors['text'])
            ax.set_ylabel('Price ($)', fontsize=12, color=self.colors['text'])
            ax.legend(fontsize=11, framealpha=0.9)
            
            # Format x-axis dates
            ax.xaxis.set_major_locator(plt.MaxNLocator(8))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # Add grid
            ax.grid(True, alpha=0.3, color=self.colors['grid'])
            ax.set_facecolor(self.colors['background'])
            
            # Tight layout
            plt.tight_layout()
            
            if save_plot:
                # Generate filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'{symbol}_actual_vs_predicted_{timestamp}.png'
                filepath = os.path.join(self.output_dir, filename)
                
                # Save plot
                plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
                plt.close()
                
                return filepath
            else:
                return fig
        
        except Exception as e:
            print(f"Error creating plot: {str(e)}")
            return None
    
    def plot_price_history(self, data: pd.DataFrame, symbol: str,
                          save_plot: bool = True) -> str:
        """
        Create price history plot with OHLC data
        
        Args:
            data (pd.DataFrame): Stock data with OHLC columns
            symbol (str): Stock symbol
            save_plot (bool): Whether to save the plot
        
        Returns:
            str: Path to saved plot or plot data
        """
        try:
            # Create figure and axis
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=self.dpi)
            
            # Convert dates if needed
            if 'Date' in data.columns:
                dates = data['Date']
            else:
                dates = data.index
            
            # Plot 1: Price chart
            ax1.plot(dates, data['Close'], 
                    color=self.colors['actual'], 
                    linewidth=2, 
                    label='Close Price')
            
            ax1.set_title(f'{symbol} Stock Price History', 
                         fontsize=16, fontweight='bold', color=self.colors['text'])
            ax1.set_ylabel('Price ($)', fontsize=12, color=self.colors['text'])
            ax1.legend(fontsize=11)
            ax1.grid(True, alpha=0.3, color=self.colors['grid'])
            ax1.set_facecolor(self.colors['background'])
            
            # Plot 2: Volume chart
            ax2.bar(dates, data['Volume'], 
                   color=self.colors['actual'], 
                   alpha=0.7, 
                   label='Volume')
            
            ax2.set_title(f'{symbol} Trading Volume', 
                         fontsize=14, fontweight='bold', color=self.colors['text'])
            ax2.set_xlabel('Date', fontsize=12, color=self.colors['text'])
            ax2.set_ylabel('Volume', fontsize=12, color=self.colors['text'])
            ax2.legend(fontsize=11)
            ax2.grid(True, alpha=0.3, color=self.colors['grid'])
            ax2.set_facecolor(self.colors['background'])
            
            # Format x-axis dates
            for ax in [ax1, ax2]:
                ax.xaxis.set_major_locator(plt.MaxNLocator(8))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # Tight layout
            plt.tight_layout()
            
            if save_plot:
                # Generate filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'{symbol}_price_history_{timestamp}.png'
                filepath = os.path.join(self.output_dir, filename)
                
                # Save plot
                plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
                plt.close()
                
                return filepath
            else:
                return fig
        
        except Exception as e:
            print(f"Error creating price history plot: {str(e)}")
            return None
    
    def plot_prediction_confidence(self, predictions: List[float], 
                                 confidence_scores: List[float],
                                 dates: List[str], symbol: str,
                                 save_plot: bool = True) -> str:
        """
        Create prediction confidence plot
        
        Args:
            predictions (List[float]): List of predicted prices
            confidence_scores (List[float]): List of confidence scores
            dates (List[str]): List of dates
            symbol (str): Stock symbol
            save_plot (bool): Whether to save the plot
        
        Returns:
            str: Path to saved plot or plot data
        """
        try:
            # Create figure and axis
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=self.dpi)
            
            # Convert dates if needed
            if isinstance(dates[0], str):
                dates = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
            
            # Plot 1: Predictions
            ax1.plot(dates, predictions, 
                    color=self.colors['predicted'], 
                    linewidth=2, 
                    marker='o', 
                    markersize=6,
                    label='Predicted Price')
            
            ax1.set_title(f'{symbol} Price Predictions', 
                         fontsize=16, fontweight='bold', color=self.colors['text'])
            ax1.set_ylabel('Price ($)', fontsize=12, color=self.colors['text'])
            ax1.legend(fontsize=11)
            ax1.grid(True, alpha=0.3, color=self.colors['grid'])
            ax1.set_facecolor(self.colors['background'])
            
            # Plot 2: Confidence scores
            ax2.bar(dates, confidence_scores, 
                   color=self.colors['actual'], 
                   alpha=0.7,
                   label='Confidence Score')
            
            ax2.set_title(f'{symbol} Prediction Confidence', 
                         fontsize=14, fontweight='bold', color=self.colors['text'])
            ax2.set_xlabel('Date', fontsize=12, color=self.colors['text'])
            ax2.set_ylabel('Confidence', fontsize=12, color=self.colors['text'])
            ax2.set_ylim(0, 1)
            ax2.legend(fontsize=11)
            ax2.grid(True, alpha=0.3, color=self.colors['grid'])
            ax2.set_facecolor(self.colors['background'])
            
            # Format x-axis dates
            for ax in [ax1, ax2]:
                ax.xaxis.set_major_locator(plt.MaxNLocator(8))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # Tight layout
            plt.tight_layout()
            
            if save_plot:
                # Generate filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'{symbol}_prediction_confidence_{timestamp}.png'
                filepath = os.path.join(self.output_dir, filename)
                
                # Save plot
                plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
                plt.close()
                
                return filepath
            else:
                return fig
        
        except Exception as e:
            print(f"Error creating confidence plot: {str(e)}")
            return None
    
    def create_dashboard_plot(self, symbol: str, 
                            actual_prices: List[float],
                            predicted_prices: List[float],
                            dates: List[str],
                            save_plot: bool = True) -> str:
        """
        Create a comprehensive dashboard plot
        
        Args:
            symbol (str): Stock symbol
            actual_prices (List[float]): Actual prices
            predicted_prices (List[float]): Predicted prices
            dates (List[str]): Dates
            save_plot (bool): Whether to save the plot
        
        Returns:
            str: Path to saved plot or plot data
        """
        try:
            # Create figure with subplots
            fig = plt.figure(figsize=(16, 12), dpi=self.dpi)
            
            # Main price comparison plot
            ax1 = plt.subplot(2, 2, (1, 2))
            ax1.plot(dates, actual_prices, 
                    color=self.colors['actual'], 
                    linewidth=2, 
                    label='Actual Price', 
                    marker='o', 
                    markersize=4)
            ax1.plot(dates, predicted_prices, 
                    color=self.colors['predicted'], 
                    linewidth=2, 
                    label='Predicted Price', 
                    marker='s', 
                    markersize=4)
            ax1.set_title(f'{symbol} Stock Price Analysis', 
                         fontsize=18, fontweight='bold', color=self.colors['text'])
            ax1.set_ylabel('Price ($)', fontsize=12, color=self.colors['text'])
            ax1.legend(fontsize=11)
            ax1.grid(True, alpha=0.3, color=self.colors['grid'])
            ax1.set_facecolor(self.colors['background'])
            
            # Error analysis
            ax2 = plt.subplot(2, 2, 3)
            errors = np.array(actual_prices) - np.array(predicted_prices)
            ax2.hist(errors, bins=20, color=self.colors['actual'], alpha=0.7, edgecolor='black')
            ax2.set_title('Prediction Error Distribution', fontsize=14, fontweight='bold', color=self.colors['text'])
            ax2.set_xlabel('Prediction Error ($)', fontsize=12, color=self.colors['text'])
            ax2.set_ylabel('Frequency', fontsize=12, color=self.colors['text'])
            ax2.grid(True, alpha=0.3, color=self.colors['grid'])
            ax2.set_facecolor(self.colors['background'])
            
            # Performance metrics
            ax3 = plt.subplot(2, 2, 4)
            mse = np.mean(errors**2)
            rmse = np.sqrt(mse)
            mae = np.mean(np.abs(errors))
            mape = np.mean(np.abs(errors / np.array(actual_prices))) * 100
            
            metrics_text = f'MSE: ${mse:.2f}\nRMSE: ${rmse:.2f}\nMAE: ${mae:.2f}\nMAPE: {mape:.2f}%'
            ax3.text(0.1, 0.5, metrics_text, transform=ax3.transAxes, 
                    fontsize=12, verticalalignment='center',
                    bbox=dict(boxstyle='round', facecolor=self.colors['background'], alpha=0.8))
            ax3.set_title('Model Performance Metrics', fontsize=14, fontweight='bold', color=self.colors['text'])
            ax3.axis('off')
            
            # Format x-axis dates for main plot
            ax1.xaxis.set_major_locator(plt.MaxNLocator(8))
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # Tight layout
            plt.tight_layout()
            
            if save_plot:
                # Generate filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'{symbol}_dashboard_{timestamp}.png'
                filepath = os.path.join(self.output_dir, filename)
                
                # Save plot
                plt.savefig(filepath, dpi=self.dpi, bbox_inches='tight', 
                           facecolor='white', edgecolor='none')
                plt.close()
                
                return filepath
            else:
                return fig
        
        except Exception as e:
            print(f"Error creating dashboard plot: {str(e)}")
            return None
    
    def cleanup_old_plots(self, max_age_hours: int = 24):
        """
        Clean up old plot files
        
        Args:
            max_age_hours (int): Maximum age of plots to keep
        """
        try:
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(hours=max_age_hours)
            
            for filename in os.listdir(self.output_dir):
                if filename.endswith('.png'):
                    filepath = os.path.join(self.output_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                    
                    if file_time < cutoff_time:
                        os.remove(filepath)
                        print(f"Removed old plot: {filename}")
        
        except Exception as e:
            print(f"Error cleaning up plots: {str(e)}")
