from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
import sys

# Add the ml module to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))

from ml.predictor import StockPredictor
from .models import StockPrediction


@csrf_exempt
@require_http_methods(["POST"])
def predict_stock(request):
    """API endpoint for stock price prediction"""
    try:
        data = json.loads(request.body)
        symbol = data.get('symbol', '').upper().strip()
        days_ahead = int(data.get('days_ahead', 1))
        
        if not symbol:
            return JsonResponse({
                'status': 'error',
                'message': 'Stock symbol is required'
            }, status=400)
        
        # Initialize predictor
        predictor = StockPredictor()
        
        # Make prediction
        result = predictor.predict_stock_price(symbol, days_ahead)
        
        if result['status'] == 'success':
            # Save prediction to database
            StockPrediction.objects.create(
                symbol=symbol,
                predicted_price=result['predicted_price'],
                confidence_score=result['confidence']
            )
            
            return JsonResponse({
                'status': 'success',
                'data': result
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': result['message']
            }, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def get_stock_info(request, symbol):
    """API endpoint to get stock information"""
    try:
        symbol = symbol.upper().strip()
        
        if not symbol:
            return JsonResponse({
                'status': 'error',
                'message': 'Stock symbol is required'
            }, status=400)
        
        # Initialize predictor
        predictor = StockPredictor()
        
        # Get stock info
        result = predictor.get_stock_info(symbol)
        
        if result['status'] == 'success':
            return JsonResponse({
                'status': 'success',
                'data': result
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': result['message']
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def train_model(request):
    """API endpoint to train the LSTM model"""
    try:
        data = json.loads(request.body)
        symbol = data.get('symbol', '').upper().strip()
        period = data.get('period', '2y')
        epochs = int(data.get('epochs', 50))
        
        if not symbol:
            return JsonResponse({
                'status': 'error',
                'message': 'Stock symbol is required'
            }, status=400)
        
        # Initialize predictor
        predictor = StockPredictor()
        
        # Train model
        result = predictor.train_model(symbol, period, epochs=epochs)
        
        if result['status'] == 'success':
            return JsonResponse({
                'status': 'success',
                'data': result
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': result['message']
            }, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }, status=500)
