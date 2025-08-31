import cohere
from typing import Dict, List, Optional
import os
from django.conf import settings
import random
import time


class SentimentAnalyzer:
    """Class for analyzing financial news sentiment using Cohere API"""
    
    def __init__(self):
        """Initialize the sentiment analyzer"""
        self.api_key = getattr(settings, 'COHERE_API_KEY', None)
        self.co = None
        
        if self.api_key:
            try:
                self.co = cohere.Client(self.api_key)
                print("Cohere API client initialized successfully")
            except Exception as e:
                print(f"Error initializing Cohere client: {str(e)}")
                self.co = None
        else:
            print("No Cohere API key found in settings")
    
    def analyze_text_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text using Cohere API
        
        Args:
            text (str): Text to analyze
        
        Returns:
            Dict: Sentiment analysis results
        """
        if not self.co:
            return self._get_dummy_sentiment(text)
        
        try:
            # Use Cohere's classify endpoint for sentiment analysis
            response = self.co.classify(
                texts=[text],
                model='large',
                examples=[
                    cohere.Example("Stock market reaches new all-time high", "bullish"),
                    cohere.Example("Company reports record-breaking quarterly earnings", "bullish"),
                    cohere.Example("Tech giant announces major breakthrough innovation", "bullish"),
                    cohere.Example("Market crashes due to economic uncertainty", "bearish"),
                    cohere.Example("Company files for bankruptcy", "bearish"),
                    cohere.Example("Federal Reserve raises interest rates", "bearish"),
                    cohere.Example("Company releases quarterly earnings report", "neutral"),
                    cohere.Example("Market shows mixed signals", "neutral"),
                    cohere.Example("Trading volume remains steady", "neutral")
                ]
            )
            
            # Extract results
            classification = response.classifications[0]
            predicted_label = classification.prediction
            confidence = classification.confidence
            
            return {
                'status': 'success',
                'text': text,
                'sentiment': predicted_label,
                'confidence': round(confidence, 3),
                'source': 'Cohere API'
            }
            
        except Exception as e:
            print(f"Error analyzing sentiment with Cohere: {str(e)}")
            return self._get_dummy_sentiment(text)
    
    def analyze_batch_sentiment(self, texts: List[str]) -> List[Dict]:
        """
        Analyze sentiment of multiple texts
        
        Args:
            texts (List[str]): List of texts to analyze
        
        Returns:
            List[Dict]: List of sentiment analysis results
        """
        results = []
        
        for text in texts:
            result = self.analyze_text_sentiment(text)
            results.append(result)
            
            # Add small delay to avoid rate limiting
            time.sleep(0.1)
        
        return results
    
    def analyze_financial_news(self, news_items: List[Dict]) -> Dict:
        """
        Analyze sentiment of financial news items
        
        Args:
            news_items (List[Dict]): List of news items with 'title' and 'content' keys
        
        Returns:
            Dict: Aggregated sentiment analysis results
        """
        if not news_items:
            return {
                'status': 'error',
                'message': 'No news items provided'
            }
        
        all_texts = []
        for item in news_items:
            # Combine title and content for analysis
            combined_text = f"{item.get('title', '')} {item.get('content', '')}"
            all_texts.append(combined_text.strip())
        
        # Analyze sentiment for all texts
        sentiment_results = self.analyze_batch_sentiment(all_texts)
        
        # Aggregate results
        sentiment_counts = {'bullish': 0, 'bearish': 0, 'neutral': 0}
        total_confidence = 0
        valid_results = 0
        
        for result in sentiment_results:
            if result['status'] == 'success':
                sentiment_counts[result['sentiment']] += 1
                total_confidence += result['confidence']
                valid_results += 1
        
        # Calculate overall sentiment
        if valid_results > 0:
            overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)
            avg_confidence = total_confidence / valid_results
        else:
            overall_sentiment = 'neutral'
            avg_confidence = 0.0
        
        return {
            'status': 'success',
            'overall_sentiment': overall_sentiment,
            'sentiment_distribution': sentiment_counts,
            'average_confidence': round(avg_confidence, 3),
            'total_news_items': len(news_items),
            'analyzed_items': valid_results,
            'detailed_results': sentiment_results
        }
    
    def get_sample_financial_news(self) -> List[Dict]:
        """
        Get sample financial news for testing/demo purposes
        
        Returns:
            List[Dict]: Sample news items
        """
        sample_news = [
            {
                'title': 'Tech Stocks Rally on Strong Earnings Reports',
                'content': 'Major technology companies reported better-than-expected quarterly earnings, driving the NASDAQ to new heights.',
                'expected_sentiment': 'bullish'
            },
            {
                'title': 'Federal Reserve Signals Potential Rate Hike',
                'content': 'The Federal Reserve indicated it may raise interest rates in the coming months to combat inflation.',
                'expected_sentiment': 'bearish'
            },
            {
                'title': 'Market Shows Mixed Signals Amid Economic Data',
                'content': 'Trading was volatile as investors weighed conflicting economic indicators and corporate earnings reports.',
                'expected_sentiment': 'neutral'
            },
            {
                'title': 'Oil Prices Surge on Supply Concerns',
                'content': 'Crude oil prices jumped to multi-month highs as geopolitical tensions raised concerns about supply disruptions.',
                'expected_sentiment': 'bullish'
            },
            {
                'title': 'Retail Sales Decline for Third Consecutive Month',
                'content': 'Consumer spending continued to weaken, raising concerns about economic growth and consumer confidence.',
                'expected_sentiment': 'bearish'
            },
            {
                'title': 'Housing Market Remains Stable',
                'content': 'Home prices and sales volumes showed little change from the previous month, indicating market stability.',
                'expected_sentiment': 'neutral'
            }
        ]
        
        return sample_news
    
    def _get_dummy_sentiment(self, text: str) -> Dict:
        """
        Generate dummy sentiment analysis when API is not available
        
        Args:
            text (str): Text to analyze
        
        Returns:
            Dict: Dummy sentiment analysis results
        """
        # Simple keyword-based sentiment analysis
        text_lower = text.lower()
        
        bullish_keywords = ['bullish', 'rally', 'surge', 'jump', 'gain', 'rise', 'high', 'record', 'breakthrough', 'innovation']
        bearish_keywords = ['bearish', 'crash', 'decline', 'drop', 'fall', 'low', 'bankruptcy', 'uncertainty', 'concern', 'weak']
        
        bullish_score = sum(1 for keyword in bullish_keywords if keyword in text_lower)
        bearish_score = sum(1 for keyword in bearish_keywords if keyword in text_lower)
        
        if bullish_score > bearish_score:
            sentiment = 'bullish'
            confidence = min(0.8, 0.5 + (bullish_score * 0.1))
        elif bearish_score > bullish_score:
            sentiment = 'bearish'
            confidence = min(0.8, 0.5 + (bearish_score * 0.1))
        else:
            sentiment = 'neutral'
            confidence = 0.6
        
        return {
            'status': 'success',
            'text': text,
            'sentiment': sentiment,
            'confidence': round(confidence, 3),
            'source': 'Dummy Analysis (API not available)'
        }
    
    def get_sentiment_summary(self, sentiment_results: List[Dict]) -> Dict:
        """
        Generate a summary of sentiment analysis results
        
        Args:
            sentiment_results (List[Dict]): List of sentiment analysis results
        
        Returns:
            Dict: Summary statistics
        """
        if not sentiment_results:
            return {
                'status': 'error',
                'message': 'No sentiment results to summarize'
            }
        
        sentiment_counts = {'bullish': 0, 'bearish': 0, 'neutral': 0}
        total_confidence = 0
        valid_results = 0
        
        for result in sentiment_results:
            if result['status'] == 'success':
                sentiment_counts[result['sentiment']] += 1
                total_confidence += result['confidence']
                valid_results += 1
        
        if valid_results == 0:
            return {
                'status': 'error',
                'message': 'No valid sentiment results found'
            }
        
        # Calculate percentages
        total = valid_results
        sentiment_percentages = {
            sentiment: round((count / total) * 100, 1)
            for sentiment, count in sentiment_counts.items()
        }
        
        # Determine dominant sentiment
        dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
        dominant_percentage = sentiment_percentages[dominant_sentiment]
        
        return {
            'status': 'success',
            'total_analyzed': valid_results,
            'sentiment_distribution': sentiment_counts,
            'sentiment_percentages': sentiment_percentages,
            'dominant_sentiment': dominant_sentiment,
            'dominant_percentage': dominant_percentage,
            'average_confidence': round(total_confidence / valid_results, 3),
            'market_outlook': self._get_market_outlook(dominant_sentiment, dominant_percentage)
        }
    
    def _get_market_outlook(self, dominant_sentiment: str, percentage: float) -> str:
        """
        Generate market outlook based on sentiment analysis
        
        Args:
            dominant_sentiment (str): Dominant sentiment
            percentage (float): Percentage of dominant sentiment
        
        Returns:
            str: Market outlook description
        """
        if percentage >= 70:
            if dominant_sentiment == 'bullish':
                return 'Strongly Bullish - Market sentiment is very positive'
            elif dominant_sentiment == 'bearish':
                return 'Strongly Bearish - Market sentiment is very negative'
            else:
                return 'Neutral - Market shows balanced sentiment'
        elif percentage >= 50:
            if dominant_sentiment == 'bullish':
                return 'Moderately Bullish - Market sentiment is positive'
            elif dominant_sentiment == 'bearish':
                return 'Moderately Bearish - Market sentiment is negative'
            else:
                return 'Neutral - Market shows mixed sentiment'
        else:
            return 'Mixed - No clear sentiment direction'
