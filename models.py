"""
NewsCheckr ML Models
Contains credibility and political bias classifiers
"""

import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import re
import logging
from typing import Dict, List, Tuple, Optional
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextPreprocessor:
    """Handles text preprocessing for ML models."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and preprocess text for analysis."""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        return text.strip()
    
    @staticmethod
    def extract_features(text: str) -> Dict[str, float]:
        """Extract additional features from text."""
        if not text:
            return {}
        
        words = text.split()
        sentences = text.split('.')
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_word_length': np.mean([len(word) for word in words]) if words else 0,
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'caps_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0
        }


class CredibilityClassifier:
    """Classifies news article credibility."""
    
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.is_trained = False
        self.preprocessor = TextPreprocessor()
    
    def _create_dummy_training_data(self) -> Tuple[List[str], List[str]]:
        """Create dummy training data for demonstration purposes."""
        
        # High credibility examples
        high_credibility = [
            "The Federal Reserve announced today a 0.25% interest rate increase following their monthly meeting. The decision was unanimous among board members and comes after careful analysis of current economic indicators.",
            "According to data released by the Department of Labor, unemployment rates decreased by 0.3% last month. The report cites increased hiring in manufacturing and service sectors.",
            "Scientists at MIT published research in the journal Nature showing promising results for renewable energy storage. The peer-reviewed study involved a three-year analysis of battery technology.",
            "The Supreme Court ruled 7-2 in favor of the plaintiff in today's landmark case. Chief Justice Roberts wrote the majority opinion, citing constitutional precedent from 1987.",
            "Quarterly earnings reports from Fortune 500 companies show mixed results, with technology sector outperforming expectations while retail struggled with supply chain issues.",
        ]
        
        # Medium credibility examples  
        medium_credibility = [
            "Sources close to the White House suggest that policy changes may be announced next week, though official confirmation has not been provided.",
            "Industry experts believe that market trends indicate potential volatility in the coming months, based on historical patterns and current indicators.",
            "Local officials reported increased activity in the downtown area, with businesses noting higher foot traffic compared to last year's figures.",
            "Anonymous sources within the organization claim that restructuring plans are being considered, though no official statement has been released.",
            "Preliminary data suggests that the new program has shown positive results, though comprehensive analysis is still pending.",
        ]
        
        # Low credibility examples
        low_credibility = [
            "SHOCKING!!! Government officials HATE this one simple trick that will change EVERYTHING! Click here to learn the secret they don't want you to know!!!",
            "Unconfirmed reports claim that celebrities are involved in secret meetings. Some people say this proves the conspiracy theories were right all along.",
            "Breaking: Massive scandal rocks the nation! Sources (who wish to remain anonymous) reveal explosive details that will shock you to your core!",
            "You won't believe what happened next! This incredible story will restore your faith in humanity and make you cry tears of joy!",
            "Insiders claim that everything you know is wrong. The truth has been hidden for years but now brave whistleblowers are speaking out!",
        ]
        
        texts = high_credibility + medium_credibility + low_credibility
        labels = ['high'] * len(high_credibility) + ['medium'] * len(medium_credibility) + ['low'] * len(low_credibility)
        
        return texts, labels
    
    def train_model(self, texts: Optional[List[str]] = None, labels: Optional[List[str]] = None):
        """Train the credibility classification model."""
        
        if texts is None or labels is None:
            logger.info("Using dummy training data for credibility classifier")
            texts, labels = self._create_dummy_training_data()
        
        # Preprocess texts
        processed_texts = [self.preprocessor.clean_text(text) for text in texts]
        
        # Create pipeline with TF-IDF and Random Forest
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        
        # Train model
        self.model.fit(processed_texts, labels)
        self.is_trained = True
        
        logger.info("Credibility classifier trained successfully")
    
    def predict_credibility(self, text: str) -> Dict[str, any]:
        """Predict credibility of given text."""
        
        if not self.is_trained:
            self.train_model()
        
        processed_text = self.preprocessor.clean_text(text)
        
        # Get prediction and probabilities
        prediction = self.model.predict([processed_text])[0]
        probabilities = self.model.predict_proba([processed_text])[0]
        
        # Convert to score (0-100)
        class_to_score = {'low': 25, 'medium': 60, 'high': 90}
        base_score = class_to_score[prediction]
        
        # Add some noise based on confidence
        max_prob = max(probabilities)
        confidence_adjustment = (max_prob - 0.5) * 20  # -10 to +10 adjustment
        final_score = max(0, min(100, base_score + confidence_adjustment))
        
        # Generate labels
        labels = []
        if final_score >= 80:
            labels = ["Highly Reliable", "Well-sourced"]
        elif final_score >= 60:
            labels = ["Generally Reliable", "Needs Verification"]
        else:
            labels = ["Low Reliability", "Likely Biased"]
        
        return {
            'credibility_score': round(final_score, 1),
            'prediction_class': prediction,
            'confidence': round(max_prob, 3),
            'labels': labels
        }


class BiasClassifier:
    """Classifies political bias of news articles."""
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        self.preprocessor = TextPreprocessor()
    
    def _create_dummy_training_data(self) -> Tuple[List[str], List[str]]:
        """Create dummy training data for political bias classification."""
        
        # Left-leaning examples
        left_examples = [
            "The progressive coalition announced new initiatives to address climate change and social inequality through comprehensive policy reforms.",
            "Labor unions celebrated the victory as workers secure better wages and healthcare benefits through collective bargaining efforts.",
            "Environmental activists praised the renewable energy investment as a crucial step toward sustainable development and green job creation.",
            "Civil rights organizations call for expanded voting access and criminal justice reform to ensure equal representation for all communities.",
            "Healthcare advocates emphasize the need for universal coverage to protect vulnerable populations and reduce medical bankruptcy.",
        ]
        
        # Center examples
        center_examples = [
            "The bipartisan committee released a report analyzing both the benefits and drawbacks of the proposed legislation.",
            "Economists from various institutions offer mixed predictions about the policy's potential impact on economic growth and inflation.",
            "The survey results show diverse opinions among voters, with supporters and critics citing different priorities and concerns.",
            "Both parties acknowledge the complexity of the issue and emphasize the need for balanced solutions that address multiple stakeholder interests.",
            "The independent analysis presents data-driven findings while noting limitations and areas requiring further research.",
        ]
        
        # Right-leaning examples  
        right_examples = [
            "Conservative lawmakers emphasize the importance of fiscal responsibility and reducing government spending to protect taxpayers.",
            "Business leaders advocate for deregulation and tax cuts to stimulate economic growth and encourage entrepreneurship.",
            "Traditional values supporters highlight the need to preserve constitutional rights and individual freedoms from government overreach.",
            "Free market advocates argue that competition and private sector innovation deliver better outcomes than government programs.",
            "Security experts stress the importance of strong national defense and law enforcement to maintain public safety and order.",
        ]
        
        texts = left_examples + center_examples + right_examples
        labels = ['Left'] * len(left_examples) + ['Center'] * len(center_examples) + ['Right'] * len(right_examples)
        
        return texts, labels
    
    def train_model(self, texts: Optional[List[str]] = None, labels: Optional[List[str]] = None):
        """Train the bias classification model."""
        
        if texts is None or labels is None:
            logger.info("Using dummy training data for bias classifier")
            texts, labels = self._create_dummy_training_data()
        
        # Preprocess texts
        processed_texts = [self.preprocessor.clean_text(text) for text in texts]
        
        # Create pipeline with TF-IDF and Multinomial Naive Bayes
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=3000, stop_words='english', ngram_range=(1, 2))),
            ('classifier', MultinomialNB(alpha=0.1))
        ])
        
        # Train model
        self.model.fit(processed_texts, labels)
        self.is_trained = True
        
        logger.info("Bias classifier trained successfully")
    
    def predict_bias(self, text: str) -> str:
        """Predict political bias of given text."""
        
        if not self.is_trained:
            self.train_model()
        
        processed_text = self.preprocessor.clean_text(text)
        prediction = self.model.predict([processed_text])[0]
        
        return prediction


class SourceCredibilityMap:
    """Maps known news sources to credibility ratings."""
    
    def __init__(self):
        # Based on various media bias/credibility rating organizations
        self.source_ratings = {
            # High credibility sources
            'reuters.com': {'credibility': 95, 'bias': 'Center'},
            'ap.org': {'credibility': 94, 'bias': 'Center'},
            'bbc.com': {'credibility': 88, 'bias': 'Center'},
            'npr.org': {'credibility': 87, 'bias': 'Center'},
            'pbs.org': {'credibility': 86, 'bias': 'Center'},
            'wsj.com': {'credibility': 84, 'bias': 'Center'},
            
            # Left-leaning sources
            'nytimes.com': {'credibility': 82, 'bias': 'Left'},
            'washingtonpost.com': {'credibility': 81, 'bias': 'Left'},
            'theguardian.com': {'credibility': 79, 'bias': 'Left'},
            'cnn.com': {'credibility': 75, 'bias': 'Left'},
            'msnbc.com': {'credibility': 70, 'bias': 'Left'},
            
            # Right-leaning sources
            'foxnews.com': {'credibility': 68, 'bias': 'Right'},
            'nypost.com': {'credibility': 65, 'bias': 'Right'},
            'dailymail.co.uk': {'credibility': 60, 'bias': 'Right'},
            'breitbart.com': {'credibility': 45, 'bias': 'Right'},
            
            # Satire/Low credibility
            'theonion.com': {'credibility': 20, 'bias': 'Center'},
            'infowars.com': {'credibility': 15, 'bias': 'Right'},
        }
    
    def get_source_info(self, source_domain: str) -> Optional[Dict[str, any]]:
        """Get credibility and bias info for a known source."""
        return self.source_ratings.get(source_domain.lower())


def test_models():
    """Test the classification models."""
    
    # Test credibility classifier
    credibility_classifier = CredibilityClassifier()
    
    test_text_high = "The Federal Reserve announced today a 0.25% interest rate increase following their monthly meeting."
    result = credibility_classifier.predict_credibility(test_text_high)
    print(f"Credibility test - High quality text:")
    print(f"Score: {result['credibility_score']}, Labels: {result['labels']}")
    
    test_text_low = "SHOCKING!!! You won't believe this one simple trick!!!"
    result = credibility_classifier.predict_credibility(test_text_low)
    print(f"\nCredibility test - Low quality text:")
    print(f"Score: {result['credibility_score']}, Labels: {result['labels']}")
    
    # Test bias classifier
    bias_classifier = BiasClassifier()
    
    test_bias_left = "Progressive policies focus on expanding social programs and environmental protection."
    bias_result = bias_classifier.predict_bias(test_bias_left)
    print(f"\nBias test - Left-leaning text: {bias_result}")
    
    test_bias_right = "Conservative policies emphasize fiscal responsibility and individual freedoms."
    bias_result = bias_classifier.predict_bias(test_bias_right)
    print(f"Bias test - Right-leaning text: {bias_result}")
    
    # Test source mapping
    source_map = SourceCredibilityMap()
    source_info = source_map.get_source_info('reuters.com')
    print(f"\nSource test - Reuters: {source_info}")


if __name__ == "__main__":
    test_models()