"""
NewsCheckr Text Summarizer
Generates summaries of news articles using both extractive and abstractive methods
"""

import logging
from typing import List, Optional
import re
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextSummarizer:
    """Handles text summarization using multiple approaches."""
    
    def __init__(self):
        self.tokenizer = Tokenizer("english")
    
    def _clean_text_for_summary(self, text: str) -> str:
        """Clean and prepare text for summarization."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove very short sentences (likely incomplete)
        sentences = text.split('.')
        cleaned_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        return '. '.join(cleaned_sentences)
    
    def _extractive_summary_lsa(self, text: str, sentence_count: int = 2) -> str:
        """Generate extractive summary using LSA algorithm."""
        try:
            parser = PlaintextParser.from_string(text, self.tokenizer)
            summarizer = LsaSummarizer()
            summary_sentences = summarizer(parser.document, sentence_count)
            
            return ' '.join([str(sentence) for sentence in summary_sentences])
        except Exception as e:
            logger.error(f"LSA summarization failed: {str(e)}")
            return ""
    
    def _extractive_summary_textrank(self, text: str, sentence_count: int = 2) -> str:
        """Generate extractive summary using TextRank algorithm."""
        try:
            parser = PlaintextParser.from_string(text, self.tokenizer)
            summarizer = TextRankSummarizer()
            summary_sentences = summarizer(parser.document, sentence_count)
            
            return ' '.join([str(sentence) for sentence in summary_sentences])
        except Exception as e:
            logger.error(f"TextRank summarization failed: {str(e)}")
            return ""
    
    def _extractive_summary_lexrank(self, text: str, sentence_count: int = 2) -> str:
        """Generate extractive summary using LexRank algorithm."""
        try:
            parser = PlaintextParser.from_string(text, self.tokenizer)
            summarizer = LexRankSummarizer()
            summary_sentences = summarizer(parser.document, sentence_count)
            
            return ' '.join([str(sentence) for sentence in summary_sentences])
        except Exception as e:
            logger.error(f"LexRank summarization failed: {str(e)}")
            return ""
    
    def _simple_extractive_summary(self, text: str, sentence_count: int = 2) -> str:
        """Simple fallback extractive summarization based on sentence length and position."""
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
        
        if len(sentences) <= sentence_count:
            return '. '.join(sentences) + '.'
        
        # Score sentences based on length and position
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            # Position score (first sentences are more important)
            position_score = 1.0 - (i / len(sentences))
            
            # Length score (medium length sentences preferred)
            length_score = min(len(sentence) / 200, 1.0)
            
            # Combined score
            total_score = (position_score * 0.6) + (length_score * 0.4)
            scored_sentences.append((sentence, total_score))
        
        # Select top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        selected_sentences = [sentence for sentence, score in scored_sentences[:sentence_count]]
        
        return '. '.join(selected_sentences) + '.'
    
    def generate_summary(self, text: str, max_sentences: int = 2, method: str = "auto") -> str:
        """
        Generate a summary of the given text.
        
        Args:
            text (str): The text to summarize
            max_sentences (int): Maximum number of sentences in summary
            method (str): Summarization method ("lsa", "textrank", "lexrank", "simple", "auto")
            
        Returns:
            str: Generated summary
        """
        if not text or len(text.strip()) < 100:
            return "Article too short to summarize effectively."
        
        cleaned_text = self._clean_text_for_summary(text)
        
        if not cleaned_text:
            return "Unable to extract meaningful content for summarization."
        
        # Choose method
        if method == "auto":
            # Try methods in order of preference
            methods_to_try = ["lsa", "textrank", "lexrank", "simple"]
        else:
            methods_to_try = [method, "simple"]  # Fallback to simple if specified method fails
        
        summary = ""
        for method_name in methods_to_try:
            try:
                if method_name == "lsa":
                    summary = self._extractive_summary_lsa(cleaned_text, max_sentences)
                elif method_name == "textrank":
                    summary = self._extractive_summary_textrank(cleaned_text, max_sentences)
                elif method_name == "lexrank":
                    summary = self._extractive_summary_lexrank(cleaned_text, max_sentences)
                elif method_name == "simple":
                    summary = self._simple_extractive_summary(cleaned_text, max_sentences)
                
                if summary and len(summary.strip()) > 20:
                    logger.info(f"Successfully generated summary using {method_name} method")
                    break
                    
            except Exception as e:
                logger.error(f"Method {method_name} failed: {str(e)}")
                continue
        
        # Final cleanup
        if summary:
            # Ensure summary ends properly
            if not summary.endswith('.'):
                summary += '.'
            
            # Remove any remaining artifacts
            summary = re.sub(r'\s+', ' ', summary).strip()
            
            return summary
        else:
            return "Failed to generate summary with available methods."


class TransformerSummarizer:
    """Abstractive summarization using transformers (optional, requires more resources)."""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
    
    def load_model(self, model_name: str = "facebook/bart-large-cnn"):
        """Load transformer model for abstractive summarization."""
        try:
            from transformers import BartForConditionalGeneration, BartTokenizer
            
            self.tokenizer = BartTokenizer.from_pretrained(model_name)
            self.model = BartForConditionalGeneration.from_pretrained(model_name)
            self.model_loaded = True
            logger.info(f"Loaded transformer model: {model_name}")
            
        except ImportError:
            logger.warning("Transformers library not available. Using extractive summarization only.")
        except Exception as e:
            logger.error(f"Failed to load transformer model: {str(e)}")
    
    def generate_abstractive_summary(self, text: str, max_length: int = 150) -> str:
        """Generate abstractive summary using transformer model."""
        if not self.model_loaded:
            self.load_model()
        
        if not self.model_loaded:
            return "Abstractive summarization not available."
        
        try:
            # Tokenize input
            inputs = self.tokenizer.encode("summarize: " + text, 
                                         return_tensors="pt", 
                                         max_length=1024, 
                                         truncation=True)
            
            # Generate summary
            summary_ids = self.model.generate(inputs, 
                                            max_length=max_length,
                                            min_length=30,
                                            length_penalty=2.0,
                                            num_beams=4,
                                            early_stopping=True)
            
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary
            
        except Exception as e:
            logger.error(f"Abstractive summarization failed: {str(e)}")
            return "Failed to generate abstractive summary."


def test_summarizer():
    """Test the summarization functionality."""
    
    # Sample news article text
    sample_text = """
    The Federal Reserve announced today a significant policy shift regarding interest rates, marking the third adjustment this year. 
    The decision came after extensive deliberation among board members and careful analysis of current economic indicators. 
    Chairman Jerome Powell stated during the press conference that the move was necessary to address inflation concerns while maintaining economic stability. 
    The 0.25% increase brings the federal funds rate to its highest level since 2019, reflecting the central bank's commitment to price stability. 
    Market analysts had mixed reactions to the announcement, with some viewing it as a prudent measure while others expressed concerns about potential economic slowdown. 
    The banking sector showed immediate response with major institutions adjusting their lending rates accordingly. 
    Consumer groups voiced concerns about the impact on mortgage rates and credit card interest rates, which are expected to rise in the coming weeks. 
    Economic forecasters predict that the rate change will have broad implications for both domestic and international markets. 
    The Federal Reserve also updated its economic projections, suggesting a more cautious outlook for the remainder of the fiscal year. 
    International markets responded with volatility, as investors reassess their strategies in light of the new monetary policy direction.
    """
    
    # Test extractive summarization
    summarizer = TextSummarizer()
    
    print("Testing different summarization methods:")
    print("-" * 50)
    
    # Test each method
    methods = ["lsa", "textrank", "lexrank", "simple", "auto"]
    for method in methods:
        summary = summarizer.generate_summary(sample_text, max_sentences=2, method=method)
        print(f"\n{method.upper()} Method:")
        print(summary)
    
    # Test transformer summarization (if available)
    print("\n" + "="*50)
    print("Testing Transformer Summarization:")
    transformer_summarizer = TransformerSummarizer()
    
    # This will likely fail without proper setup, but shows the interface
    abstractive_summary = transformer_summarizer.generate_abstractive_summary(sample_text)
    print(abstractive_summary)


if __name__ == "__main__":
    test_summarizer()