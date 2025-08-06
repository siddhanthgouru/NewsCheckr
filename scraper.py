"""
NewsCheckr Web Scraper
Extracts article content from news URLs using newspaper3k
"""

import requests
from newspaper import Article, ArticleException
from urllib.parse import urlparse
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsArticleScraper:
    """Scrapes news articles from URLs and extracts relevant content."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_article(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape article content from the given URL.
        
        Args:
            url (str): The URL of the news article
            
        Returns:
            Dict containing article data or None if scraping fails
        """
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                logger.error(f"Invalid URL format: {url}")
                return None
            
            # Create and download article
            article = Article(url)
            article.download()
            article.parse()
            
            # Extract source domain
            source_domain = parsed_url.netloc.lower()
            if source_domain.startswith('www.'):
                source_domain = source_domain[4:]
            
            # Extract article data
            article_data = {
                'url': url,
                'title': article.title or 'No title available',
                'text': article.text or 'No content available',
                'source': source_domain,
                'authors': ', '.join(article.authors) if article.authors else 'Unknown',
                'publish_date': str(article.publish_date) if article.publish_date else 'Unknown',
                'top_image': article.top_image or '',
                'meta_description': article.meta_description or '',
                'meta_keywords': ', '.join(article.meta_keywords) if article.meta_keywords else ''
            }
            
            # Validate that we got meaningful content
            if len(article_data['text'].strip()) < 100:
                logger.warning(f"Article text too short (less than 100 chars): {url}")
                return None
            
            logger.info(f"Successfully scraped article from {source_domain}")
            return article_data
            
        except ArticleException as e:
            logger.error(f"Article parsing error for {url}: {str(e)}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error for {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {str(e)}")
            return None
    
    def validate_news_url(self, url: str) -> bool:
        """
        Basic validation to check if URL looks like a news article.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if URL appears to be a news article
        """
        try:
            parsed = urlparse(url)
            
            # Check if it's a valid HTTP(S) URL
            if parsed.scheme not in ['http', 'https']:
                return False
            
            # Common news domains and patterns
            news_indicators = [
                'news', 'article', 'story', 'post', 'blog',
                'cnn', 'bbc', 'reuters', 'ap', 'nytimes',
                'washingtonpost', 'guardian', 'forbes', 'time'
            ]
            
            url_lower = url.lower()
            return any(indicator in url_lower for indicator in news_indicators)
            
        except Exception:
            return False


def test_scraper():
    """Test the scraper with sample URLs."""
    scraper = NewsArticleScraper()
    
    # Test URLs (use actual news URLs for testing)
    test_urls = [
        "https://www.bbc.com/news/world-us-canada-67890123",  # Example URL
        "https://www.cnn.com/2023/12/01/politics/example-article/index.html"  # Example URL
    ]
    
    for url in test_urls:
        print(f"\nTesting URL: {url}")
        result = scraper.scrape_article(url)
        if result:
            print(f"Title: {result['title'][:100]}...")
            print(f"Source: {result['source']}")
            print(f"Text length: {len(result['text'])} characters")
            print(f"Authors: {result['authors']}")
        else:
            print("Failed to scrape article")


if __name__ == "__main__":
    test_scraper()