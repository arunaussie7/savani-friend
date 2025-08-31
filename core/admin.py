from django.contrib import admin
from .models import StockPrediction, SentimentAnalysis, StockData


@admin.register(StockPrediction)
class StockPredictionAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'prediction_date', 'actual_price', 'predicted_price', 'confidence_score', 'model_version', 'created_at')
    list_filter = ('symbol', 'model_version', 'prediction_date', 'created_at')
    search_fields = ('symbol',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Stock Information', {
            'fields': ('symbol', 'prediction_date')
        }),
        ('Prediction Results', {
            'fields': ('actual_price', 'predicted_price', 'confidence_score')
        }),
        ('Model Information', {
            'fields': ('model_version', 'created_at')
        }),
    )


@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('text', 'sentiment', 'confidence', 'source', 'created_at')
    list_filter = ('sentiment', 'source', 'created_at')
    search_fields = ('text',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Text Content', {
            'fields': ('text',)
        }),
        ('Analysis Results', {
            'fields': ('sentiment', 'confidence', 'source')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )


@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'created_at')
    list_filter = ('symbol', 'date', 'created_at')
    search_fields = ('symbol',)
    readonly_fields = ('created_at',)
    ordering = ('-date', '-created_at')
    
    fieldsets = (
        ('Stock Information', {
            'fields': ('symbol', 'date')
        }),
        ('Price Data', {
            'fields': ('open_price', 'high_price', 'low_price', 'close_price')
        }),
        ('Volume & Metadata', {
            'fields': ('volume', 'created_at')
        }),
    )
