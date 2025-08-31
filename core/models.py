from django.db import models
from django.utils import timezone


class StockPrediction(models.Model):
    """Model to store stock prediction results"""
    symbol = models.CharField(max_length=10)
    prediction_date = models.DateTimeField(default=timezone.now)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    model_version = models.CharField(max_length=50, default='LSTM_v1')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.symbol} - {self.prediction_date.strftime('%Y-%m-%d')}"


class SentimentAnalysis(models.Model):
    """Model to store sentiment analysis results"""
    SENTIMENT_CHOICES = [
        ('bullish', 'Bullish'),
        ('bearish', 'Bearish'),
        ('neutral', 'Neutral'),
    ]
    
    text = models.TextField()
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)
    confidence = models.DecimalField(max_digits=5, decimal_places=4)
    source = models.CharField(max_length=100, default='Financial News')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sentiment} - {self.text[:50]}..."


class StockData(models.Model):
    """Model to store historical stock data"""
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['symbol', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.symbol} - {self.date} - ${self.close_price}"
