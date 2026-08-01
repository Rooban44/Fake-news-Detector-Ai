"""
Utility functions for text preprocessing and analysis
"""
import re
import string
from collections import Counter


def clean_text(text):
    """Clean and normalize text for analysis"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    return text.strip()


def extract_keywords(text, top_n=10):
    """Extract most common keywords from text"""
    # Remove punctuation and convert to lowercase
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Split into words
    words = text.split()
    
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
    }
    
    words = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Count word frequency
    word_counts = Counter(words)
    
    return word_counts.most_common(top_n)


def calculate_text_stats(text):
    """Calculate basic statistics about the text"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    words = text.split()
    
    # Count capital letters (excessive caps can indicate sensationalism)
    caps_count = sum(1 for c in text if c.isupper())
    caps_ratio = caps_count / len(text) if len(text) > 0 else 0
    
    # Count exclamation marks (excessive use indicates sensationalism)
    exclamation_count = text.count('!')
    
    # Count question marks
    question_count = text.count('?')
    
    # Average sentence length
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    
    return {
        'word_count': len(words),
        'sentence_count': len(sentences),
        'avg_sentence_length': avg_sentence_length,
        'caps_ratio': caps_ratio,
        'exclamation_count': exclamation_count,
        'question_count': question_count
    }


def detect_clickbait_patterns(text):
    """Detect common clickbait patterns in text"""
    clickbait_phrases = [
        r'you won\'t believe',
        r'shocking',
        r'amazing',
        r'incredible',
        r'this one trick',
        r'doctors hate',
        r'what happened next',
        r'the truth about',
        r'they don\'t want you to know',
        r'secret',
        r'exposed',
        r'revealed',
        r'number \d+ will',
        r'\d+ reasons why',
        r'\d+ ways to',
        r'click here',
        r'must see',
        r'breaking:',
        r'urgent:',
        r'alert:'
    ]
    
    text_lower = text.lower()
    matches = []
    
    for pattern in clickbait_phrases:
        if re.search(pattern, text_lower):
            matches.append(pattern.replace(r'\d+', 'X').replace(r'\\', ''))
    
    return matches


def analyze_source_credibility_indicators(text):
    """Analyze text for credibility indicators"""
    credible_indicators = [
        r'according to',
        r'research shows',
        r'study found',
        r'experts say',
        r'data suggests',
        r'reported by',
        r'confirmed by',
        r'official statement',
        r'peer-reviewed',
        r'published in'
    ]
    
    questionable_indicators = [
        r'some say',
        r'people are saying',
        r'many believe',
        r'it is said',
        r'rumor has it',
        r'allegedly',
        r'supposedly',
        r'unconfirmed',
        r'anonymous source',
        r'insider claims'
    ]
    
    text_lower = text.lower()
    
    credible_count = sum(1 for pattern in credible_indicators if re.search(pattern, text_lower))
    questionable_count = sum(1 for pattern in questionable_indicators if re.search(pattern, text_lower))
    
    return {
        'credible_indicators': credible_count,
        'questionable_indicators': questionable_count
    }
