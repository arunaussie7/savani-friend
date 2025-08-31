from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    path('predict/', api_views.predict_stock, name='predict_stock'),
    path('stock-info/<str:symbol>/', api_views.get_stock_info, name='get_stock_info'),
    path('train-model/', api_views.train_model, name='train_model'),
]
