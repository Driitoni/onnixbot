"""
Market News Module for Pocket Option Trading Bot
Fetches and processes real-time market news and economic events
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class MarketNews:
    """Market news fetcher and processor"""
    
    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY', 'demo')
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
        self.finnhub_key = os.getenv('FINNHUB_API_KEY', 'demo')
        
    def get_latest_news(self) -> Dict:
        """Get latest market news from multiple sources"""
        try:
            # Try multiple news sources
            news_data = self._get_news_from_newsapi()
            if not news_data:
                news_data = self._get_news_from_finnhub()
            if not news_data:
                news_data = self._get_fallback_news()
            
            return news_data
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return self._get_fallback_news()
    
    def _get_news_from_newsapi(self) -> Optional[Dict]:
        """Fetch news from NewsAPI (requires API key)"""
        if self.news_api_key == 'demo':
            return None
            
        try:
            url = f"https://newsapi.org/v2/everything"
            params = {
                'apiKey': self.news_api_key,
                'q': 'forex OR "currency trading" OR "financial markets" OR stocks OR cryptocurrency',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"NewsAPI error: {e}")
            return None
    
    def _get_news_from_finnhub(self) -> Optional[Dict]:
        """Fetch news from Finnhub (requires API key)"""
        if self.finnhub_key == 'demo':
            return None
            
        try:
            url = f"https://finnhub.io/api/v1/news"
            params = {
                'token': self.finnhub_key,
                'category': 'forex',
                'minId': 0
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Convert to standard format
            articles = []
            for article in data[:5]:
                articles.append({
                    'title': article.get('headline', 'No title'),
                    'description': article.get('summary', ''),
                    'url': article.get('url', '#'),
                    'publishedAt': datetime.fromtimestamp(article.get('datetime', 0)).isoformat(),
                    'source': 'Finnhub'
                })
            
            return {'articles': articles}
        except Exception as e:
            logger.error(f"Finnhub error: {e}")
            return None
    
    def _get_fallback_news(self) -> Dict:
        """Get fallback market news when APIs are not available"""
        current_time = datetime.now()
        
        # Sample market news (in real implementation, this would be from actual sources)
        fallback_articles = [
            {
                'title': 'EUR/USD Steady as Markets Await Central Bank Decisions',
                'description': 'The euro remains stable against the dollar as investors monitor upcoming central bank policy meetings and economic data releases.',
                'url': 'https://example.com/eur-usd-analysis',
                'publishedAt': (current_time - timedelta(hours=1)).isoformat(),
                'source': 'Market Analysis'
            },
            {
                'title': 'Gold Prices Edge Higher on Safe-Haven Demand',
                'description': 'Gold futures advance as geopolitical tensions and economic uncertainty drive investors toward safe-haven assets.',
                'url': 'https://example.com/gold-outlook',
                'publishedAt': (current_time - timedelta(hours=2)).isoformat(),
                'source': 'Commodities Report'
            },
            {
                'title': 'Bitcoin Maintains Support Above $40,000',
                'description': 'Cryptocurrency markets show resilience as Bitcoin holds key support levels amid ongoing institutional adoption.',
                'url': 'https://example.com/crypto-update',
                'publishedAt': (current_time - timedelta(hours=3)).isoformat(),
                'source': 'Crypto Daily'
            },
            {
                'title': 'Oil Prices Fluctuate on Supply and Demand Concerns',
                'description': 'Crude oil futures trade mixed as market participants balance supply constraints against global demand uncertainties.',
                'url': 'https://example.com/oil-market',
                'publishedAt': (current_time - timedelta(hours=4)).isoformat(),
                'source': 'Energy Markets'
            },
            {
                'title': 'Stock Markets Show Cautious Optimism',
                'description': 'Major indices advance modestly as corporate earnings season progresses and economic indicators show mixed signals.',
                'url': 'https://example.com/stock-outlook',
                'publishedAt': (current_time - timedelta(hours=5)).isoformat(),
                'source': 'Equity Markets'
            }
        ]
        
        return {'articles': fallback_articles}
    
    def get_economic_calendar(self) -> List[Dict]:
        """Get economic events calendar (placeholder)"""
        # In a real implementation, this would fetch from economic calendar APIs
        events = [
            {
                'time': '08:30',
                'event': 'US Non-Farm Payrolls',
                'currency': 'USD',
                'impact': 'HIGH',
                'forecast': '200K',
                'previous': '180K'
            },
            {
                'time': '10:00',
                'event': 'EUR Interest Rate Decision',
                'currency': 'EUR',
                'impact': 'HIGH',
                'forecast': '0.50%',
                'previous': '0.25%'
            },
            {
                'time': '14:30',
                'event': 'Crude Oil Inventories',
                'currency': 'USD',
                'impact': 'MEDIUM',
                'forecast': '-2.5M',
                'previous': '-3.2M'
            }
        ]
        return events
    
    def get_market_sentiment(self) -> Dict:
        """Get current market sentiment indicators"""
        # Placeholder - in real implementation, this would analyze various sentiment indicators
        sentiment = {
            'overall': 'NEUTRAL',
            'risk_appetite': 'MODERATE',
            'vix_level': 18.5,
            'dollar_strength': 102.3,
            'gold_trend': 'BULLISH',
            'crypto_sentiment': 'BULLISH',
            'forex_volatility': 'MODERATE'
        }
        return sentiment
    
    def get_forex_news(self, pair: str = None) -> Dict:
        """Get currency pair specific news"""
        # This would fetch pair-specific news in a real implementation
        pair_news = {
            'EURUSD': [
                {
                    'title': 'ECB Officials Signal Potential Rate Hike Pause',
                    'impact': 'BEARISH_EUR',
                    'time': datetime.now().isoformat()
                },
                {
                    'title': 'US Dollar Strengthens on Fed Hawkish Comments',
                    'impact': 'BEARISH_EUR',
                    'time': (datetime.now() - timedelta(hours=2)).isoformat()
                }
            ],
            'GBPUSD': [
                {
                    'title': 'BoE Governor Discusses Inflation Control Measures',
                    'impact': 'BULLISH_GBP',
                    'time': (datetime.now() - timedelta(hours=1)).isoformat()
                }
            ],
            'USDJPY': [
                {
                    'title': 'BoJ Maintains Ultra-Loose Policy Stance',
                    'impact': 'BULLISH_JPY',
                    'time': (datetime.now() - timedelta(hours=3)).isoformat()
                }
            ]
        }
        
        if pair:
            return {'articles': pair_news.get(pair, [])}
        return pair_news
    
    def get_breaking_news_alerts(self) -> List[Dict]:
        """Get breaking news that could impact markets"""
        # This would monitor news feeds for breaking news
        breaking_news = [
            {
                'headline': 'Major Economic Data Release Scheduled for Next Hour',
                'impact': 'HIGH',
                'assets_affected': ['EURUSD', 'GBPUSD', 'USDJPY'],
                'alert_time': datetime.now().isoformat()
            }
        ]
        return breaking_news

class NewsSentimentAnalyzer:
    """Analyzes news sentiment for market insights"""
    
    def __init__(self):
        self.sentiment_weights = {
            'POSITIVE': 1.0,
            'NEUTRAL': 0.0,
            'NEGATIVE': -1.0
        }
    
    def analyze_news_sentiment(self, news_articles: List[Dict]) -> Dict:
        """Analyze sentiment of news articles"""
        if not news_articles:
            return {'sentiment': 'NEUTRAL', 'score': 0, 'confidence': 0}
        
        total_sentiment = 0
        processed_count = 0
        
        # Keywords for sentiment analysis
        positive_keywords = ['growth', 'increase', 'rise', 'gain', 'bull', 'positive', 'strong', 'boost', 'rally']
        negative_keywords = ['decline', 'decrease', 'fall', 'loss', 'bear', 'negative', 'weak', 'drop', 'crash', 'recession']
        
        for article in news_articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            text = f"{title} {description}"
            
            positive_count = sum(1 for word in positive_keywords if word in text)
            negative_count = sum(1 for word in negative_keywords if word in text)
            
            if positive_count > negative_count:
                total_sentiment += 1
            elif negative_count > positive_count:
                total_sentiment -= 1
            
            processed_count += 1
        
        if processed_count == 0:
            return {'sentiment': 'NEUTRAL', 'score': 0, 'confidence': 0}
        
        # Calculate final sentiment
        sentiment_score = total_sentiment / processed_count
        confidence = min(abs(sentiment_score) * 100, 100)
        
        if sentiment_score > 0.3:
            sentiment = 'BULLISH'
        elif sentiment_score < -0.3:
            sentiment = 'BEARISH'
        else:
            sentiment = 'NEUTRAL'
        
        return {
            'sentiment': sentiment,
            'score': round(sentiment_score, 2),
            'confidence': round(confidence, 1),
            'articles_analyzed': processed_count
        }
    
    def get_asset_impact_assessment(self, news_articles: List[Dict], asset: str) -> Dict:
        """Assess how news might impact a specific asset"""
        impact_score = 0
        reasons = []
        
        for article in news_articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            text = f"{title} {description}"
            
            # Asset-specific impact analysis
            if asset == 'EURUSD':
                if any(word in text for word in ['ecb', 'european central bank', 'euro', 'europe']):
                    if any(word in text for word in ['hawkish', 'increase', 'raise', 'tightening']):
                        impact_score += 1
                        reasons.append('ECB hawkish stance')
                    elif any(word in text for word in ['dovish', 'decrease', 'cut', 'easing']):
                        impact_score -= 1
                        reasons.append('ECB dovish stance')
                
                if any(word in text for word in ['fed', 'federal reserve', 'dollar', 'us']):
                    if any(word in text for word in ['hawkish', 'increase', 'raise']):
                        impact_score -= 1
                        reasons.append('Fed hawkish stance (USD strength)')
                    elif any(word in text for word in ['dovish', 'decrease', 'cut']):
                        impact_score += 1
                        reasons.append('Fed dovish stance (USD weakness)')
            
            elif asset == 'XAUUSD':  # Gold
                if any(word in text for word in ['inflation', 'uncertaint', 'crisis', 'safe-haven']):
                    impact_score += 1
                    reasons.append('Safe-haven demand')
                elif any(word in text for word in ['strong dollar', 'fed hawkish', 'rate increase']):
                    impact_score -= 1
                    reasons.append('Dollar strength pressure')
            
            elif asset in ['BTCUSD', 'ETHUSD']:  # Crypto
                if any(word in text for word in ['bitcoin', 'crypto', 'institutional']):
                    if any(word in text for word in ['adoption', 'etf', 'bullish']):
                        impact_score += 1
                        reasons.append('Crypto adoption news')
                    elif any(word in text for word in ['regulation', 'ban', 'negative']):
                        impact_score -= 1
                        reasons.append('Crypto regulatory concerns')
        
        return {
            'impact_score': impact_score,
            'impact_direction': 'BULLISH' if impact_score > 0 else 'BEARISH' if impact_score < 0 else 'NEUTRAL',
            'reasons': reasons,
            'confidence': min(abs(impact_score) * 25, 100)
        }