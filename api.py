"""
NewsCheckr Flask API
Main API endpoint for news credibility and bias analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from typing import Dict, Optional
import traceback
import time

try:
    from scraper import NewsArticleScraper
except ImportError:
    # Fallback to simple scraper if newspaper4k has issues
    from simple_scraper import SimpleNewsArticleScraper as NewsArticleScraper
    print("Using simple scraper fallback")
from models import CredibilityClassifier, BiasClassifier, SourceCredibilityMap
from summarizer import TextSummarizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global model instances (initialized on first use for better startup time)
scraper = None
credibility_classifier = None
bias_classifier = None
summarizer = None
source_map = None


def initialize_models():
    """Initialize all models on first API call."""
    global scraper, credibility_classifier, bias_classifier, summarizer, source_map
    
    if scraper is None:
        logger.info("Initializing NewsCheckr models...")
        
        try:
            # Initialize scraper
            scraper = NewsArticleScraper()
            logger.info("✓ Scraper initialized")
            
            # Initialize classifiers
            credibility_classifier = CredibilityClassifier()
            bias_classifier = BiasClassifier()
            logger.info("✓ Classifiers initialized")
            
            # Pre-train models with dummy data
            credibility_classifier.train_model()
            bias_classifier.train_model()
            logger.info("✓ Models trained")
            
            # Initialize summarizer with error handling
            try:
                summarizer = TextSummarizer()
                logger.info("✓ Summarizer initialized")
            except Exception as e:
                logger.warning(f"Summarizer failed to initialize: {e}")
                summarizer = None
            
            # Initialize source map with error handling
            try:
                source_map = SourceCredibilityMap()
                logger.info("✓ Source map initialized")
            except Exception as e:
                logger.warning(f"Source map failed to initialize: {e}")
                source_map = None
                
            logger.info("Model initialization completed")
            
        except Exception as e:
            logger.error(f"Critical error initializing models: {str(e)}")
            # Ensure we have at least basic functionality
            if scraper is None:
                scraper = NewsArticleScraper()
            if credibility_classifier is None:
                credibility_classifier = CredibilityClassifier()
                credibility_classifier.train_model()
            if bias_classifier is None:
                bias_classifier = BiasClassifier()
                bias_classifier.train_model()


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'NewsCheckr API',
        'version': '1.0.0',
        'endpoints': ['/analyze'],
        'description': 'ML-based news credibility and bias analysis'
    })


@app.route('/analyze', methods=['POST'])
def analyze_news():
    """
    Main endpoint for analyzing news articles.
    
    Expected JSON input:
    {
        "url": "https://example.com/news-article"
    }
    
    Returns JSON with analysis results.
    """
    try:
        # Initialize models if not already done
        initialize_models()
        
        # Validate request
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL parameter is required'}), 400
        
        url = data['url'].strip()
        if not url:
            return jsonify({'error': 'URL cannot be empty'}), 400
        
        logger.info(f"Analyzing article from: {url}")
        start_time = time.time()
        
        # Step 1: Scrape the article
        article_data = scraper.scrape_article(url)
        if not article_data:
            return jsonify({'error': 'Failed to scrape article. URL may be invalid or inaccessible.'}), 400
        
        # Step 2: Check if we have source credibility info
        source_info = None
        if source_map:
            source_info = source_map.get_source_info(article_data['source'])
        
        # Step 3: Analyze credibility
        credibility_result = credibility_classifier.predict_credibility(article_data['text'])
        
        # If we have source info, blend it with text-based analysis
        if source_info:
            source_credibility = source_info['credibility']
            text_credibility = credibility_result['credibility_score']
            
            # Weighted average: 60% source reputation, 40% text analysis
            blended_credibility = (source_credibility * 0.6) + (text_credibility * 0.4)
            final_credibility = round(blended_credibility, 1)
            
            logger.info(f"Blended credibility: source={source_credibility}, text={text_credibility}, final={final_credibility}")
        else:
            final_credibility = credibility_result['credibility_score']
        
        # Step 4: Analyze bias
        if source_info and 'bias' in source_info:
            # Use known source bias
            predicted_bias = source_info['bias']
            logger.info(f"Using known source bias: {predicted_bias}")
        else:
            # Predict bias from text
            predicted_bias = bias_classifier.predict_bias(article_data['text'])
            logger.info(f"Predicted bias from text: {predicted_bias}")
        
        # Step 5: Generate summary
        if summarizer:
            summary = summarizer.generate_summary(article_data['text'], max_sentences=2)
        else:
            # Fallback: simple summary (first 2 sentences)
            sentences = article_data['text'].split('.')[:2]
            summary = '. '.join(s.strip() for s in sentences if s.strip()) + '.'
        
        # Step 6: Generate appropriate labels based on final credibility score
        if final_credibility >= 85:
            labels = ["Highly Reliable", "Well-sourced"]
        elif final_credibility >= 70:
            labels = ["Generally Reliable", "Fact-based"]
        elif final_credibility >= 55:
            labels = ["Mixed Reliability", "Needs Verification"]
        elif final_credibility >= 40:
            labels = ["Low Reliability", "Likely Biased"]
        else:
            labels = ["Very Low Reliability", "Likely Satire"]
        
        # Calculate processing time
        processing_time = round(time.time() - start_time, 2)
        
        # Build response
        response = {
            'source': article_data['source'],
            'credibility_score': final_credibility,
            'bias': predicted_bias,
            'summary': summary,
            'labels': labels,
            'metadata': {
                'title': article_data['title'],
                'authors': article_data['authors'],
                'publish_date': article_data['publish_date'],
                'processing_time_seconds': processing_time,
                'analysis_method': 'blended' if source_info else 'text_only'
            }
        }
        
        logger.info(f"Analysis completed in {processing_time}s - Score: {final_credibility}, Bias: {predicted_bias}")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error analyzing article: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.route('/sources', methods=['GET'])
def list_known_sources():
    """List all known news sources with their ratings."""
    initialize_models()
    
    if source_map:
        return jsonify({
            'known_sources': source_map.source_ratings,
            'total_sources': len(source_map.source_ratings)
        })
    else:
        return jsonify({
            'known_sources': {},
            'total_sources': 0,
            'error': 'Source map not available'
        })


@app.route('/debug', methods=['GET'])
def debug_models():
    """Debug endpoint to check model initialization."""
    try:
        initialize_models()
        return jsonify({
            'scraper': scraper is not None,
            'credibility_classifier': credibility_classifier is not None,
            'bias_classifier': bias_classifier is not None,
            'summarizer': summarizer is not None,
            'source_map': source_map is not None,
            'status': 'Models initialized successfully'
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'Model initialization failed'
        }), 500


@app.route('/test', methods=['POST'])
def test_with_text():
    """
    Test endpoint that accepts raw text instead of URL.
    Useful for testing the models without scraping.
    
    Expected JSON input:
    {
        "text": "Article text to analyze...",
        "source": "example.com" (optional)
    }
    """
    try:
        initialize_models()
        
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text parameter is required'}), 400
        
        text = data['text'].strip()
        source = data.get('source', 'unknown')
        
        if not text or len(text) < 50:
            return jsonify({'error': 'Text must be at least 50 characters long'}), 400
        
        # Analyze the text
        credibility_result = credibility_classifier.predict_credibility(text)
        bias_result = bias_classifier.predict_bias(text)
        summary = summarizer.generate_summary(text, max_sentences=2)
        
        response = {
            'source': source,
            'credibility_score': credibility_result['credibility_score'],
            'bias': bias_result,
            'summary': summary,
            'labels': credibility_result['labels'],
            'metadata': {
                'text_length': len(text),
                'analysis_method': 'text_only',
                'confidence': credibility_result['confidence']
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in test endpoint: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': ['/', '/analyze', '/sources', '/test']
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'message': 'Please check the logs for more details'
    }), 500


if __name__ == '__main__':
    print("""
    ====================================
    NewsCheckr API Starting...
    ====================================
    
    Available endpoints:
    - GET  /           : Health check
    - POST /analyze    : Analyze news article from URL
    - POST /test       : Test analysis with raw text
    - GET  /sources    : List known sources and ratings
    
    Example usage:
    curl -X POST http://localhost:5000/analyze \\
         -H "Content-Type: application/json" \\
         -d '{"url": "https://example.com/news-article"}'
    
    ====================================
    """)
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=False  # Set to True for development
    )