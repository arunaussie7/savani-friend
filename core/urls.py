from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('prediction/', views.prediction, name='prediction'),
    path('news-sentiment/', views.news_sentiment, name='news_sentiment'),
    path('about/', views.about, name='about'),
]
