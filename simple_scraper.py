"""
Simple web scraper using requests and BeautifulSoup as fallback
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
from typing import Dict, Optional
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleNewsArticleScraper:
    """Simple scraper using requests and BeautifulSoup."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_article(self, url: str) -> Optional[Dict[str, str]]:
        """Scrape article content using requests and BeautifulSoup."""
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                logger.error(f"Invalid URL format: {url}")
                return None
            
            # Get the page content
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract source domain
            source_domain = parsed_url.netloc.lower()
            if source_domain.startswith('www.'):
                source_domain = source_domain[4:]
            
            # Extract title
            title = ""
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text().strip()
            
            # Try to find article title from meta tags or h1
            if not title:
                meta_title = soup.find('meta', property='og:title')
                if meta_title:
                    title = meta_title.get('content', '').strip()
            
            if not title:
                h1_tag = soup.find('h1')
                if h1_tag:
                    title = h1_tag.get_text().strip()
            
            # Extract article text from common article containers
            article_text = ""
            
            # Try common article selectors
            article_selectors = [
                'article',
                '[role="main"]',
                '.article-content',
                '.post-content',
                '.entry-content',
                '.content',
                'main',
                '.article-body',
                '.story-body'
            ]
            
            for selector in article_selectors:
                article_elem = soup.select_one(selector)
                if article_elem:
                    # Get all paragraph text
                    paragraphs = article_elem.find_all(['p', 'div'], recursive=True)
                    text_parts = []
                    for p in paragraphs:
                        text = p.get_text().strip()
                        if len(text) > 20:  # Only include substantial text
                            text_parts.append(text)
                    
                    article_text = ' '.join(text_parts)
                    if len(article_text) > 200:  # If we found substantial content
                        break
            
            # Fallback: get all paragraph text
            if not article_text or len(article_text) < 200:
                paragraphs = soup.find_all('p')
                text_parts = []
                for p in paragraphs:
                    text = p.get_text().strip()
                    if len(text) > 20:
                        text_parts.append(text)
                article_text = ' '.join(text_parts)
            
            # Clean up the text
            article_text = re.sub(r'\s+', ' ', article_text).strip()
            
            # Validate that we got meaningful content
            if len(article_text) < 100:
                logger.warning(f"Article text too short: {url}")
                return None
            
            # Extract metadata
            author = "Unknown"
            meta_author = soup.find('meta', attrs={'name': 'author'})
            if not meta_author:
                meta_author = soup.find('meta', property='article:author')
            if meta_author:
                author = meta_author.get('content', 'Unknown').strip()
            
            publish_date = "Unknown"
            meta_date = soup.find('meta', property='article:published_time')
            if not meta_date:
                meta_date = soup.find('meta', attrs={'name': 'publish-date'})
            if meta_date:
                publish_date = meta_date.get('content', 'Unknown').strip()
            
            article_data = {
                'url': url,
                'title': title or 'No title available',
                'text': article_text,
                'source': source_domain,
                'authors': author,
                'publish_date': publish_date,
                'top_image': '',
                'meta_description': '',
                'meta_keywords': ''
            }
            
            logger.info(f"Successfully scraped article from {source_domain}")
            return article_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error for {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {str(e)}")
            return None


def test_simple_scraper():
    """Test the simple scraper."""
    scraper = SimpleNewsArticleScraper()
    
    # Test with a simple URL
    test_url = "https://example.com"  # Replace with actual news URL for testing
    
    print(f"Testing URL: {test_url}")
    result = scraper.scrape_article(test_url)
    if result:
        print(f"Title: {result['title'][:100]}...")
        print(f"Source: {result['source']}")
        print(f"Text length: {len(result['text'])} characters")
        print(f"Text preview: {result['text'][:200]}...")
    else:
        print("Failed to scrape article")


if __name__ == "__main__":
    test_simple_scraper()