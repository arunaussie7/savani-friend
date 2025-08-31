from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import os
import sys

# Add the ml module to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))

from .models import StockPrediction


def home(request):
    """Home page view"""
    context = {
        'title': 'Stock Market Analysis Dashboard',
        'description': 'Professional stock market analysis and news dashboard'
    }
    return render(request, 'core/home.html', context)


def prediction(request):
    """Prediction page view with TradingView widgets"""
    context = {
        'title': 'Stock Market Prediction',
        'description': 'Advanced stock prediction with performance metrics, seasonals, and technical analysis'
    }
    return render(request, 'core/prediction.html', context)


def news_sentiment(request):
    """News and Sentiment Analysis page view"""
    context = {
        'title': 'News & Sentiment Analysis',
        'description': 'Real-time financial news and market sentiment analysis'
    }
    return render(request, 'core/news_sentiment.html', context)


def about(request):
    """About page view"""
    context = {
        'title': 'About Stock Market Analysis',
        'description': 'Learn about our professional stock market analysis platform'
    }
    return render(request, 'core/about.html', context)
