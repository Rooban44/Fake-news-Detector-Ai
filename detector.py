"""
Fake News Detection Engine
Multi-factor analysis combining credibility scoring, sentiment analysis, and linguistic patterns
"""
from textblob import TextBlob
from utils import (
    clean_text,
    extract_keywords,
    calculate_text_stats,
    detect_clickbait_patterns,
    analyze_source_credibility_indicators
)
from source_credibility import SourceCredibilityChecker
from web_verifier import WebVerifier
from detector_helpers import (
    get_sentiment_description_simple,
    get_credibility_description_simple,
    get_linguistic_description_simple,
    get_clickbait_description_simple,
    generate_summary
)


class FakeNewsDetector:
    """Main fake news detection engine"""
    
    def __init__(self):
        self.weights = {
            'sentiment': 0.15,
            'credibility': 0.25,
            'linguistic': 0.20,
            'clickbait': 0.20,
            'source_domain': 0.10,
            'web_verification': 0.10
        }
        
        # Initialize new checkers
        self.source_checker = SourceCredibilityChecker()
        self.web_verifier = WebVerifier()
    
    def analyze(self, text, source_url=None):
        """
        Perform comprehensive fake news analysis
        
        Args:
            text: News article text to analyze
            source_url: Optional URL of the news source
            
        Returns:
            dict: Analysis results with scores and recommendations
        """
        if not text or len(text.strip()) < 20:
            return {
                'error': 'Text too short for analysis. Please provide at least 20 characters.'
            }
        
        # Clean the text
        cleaned_text = clean_text(text)
        
        # Perform multi-factor analysis
        sentiment_score = self._analyze_sentiment(cleaned_text)
        credibility_score = self._analyze_credibility(cleaned_text)
        linguistic_score = self._analyze_linguistic_patterns(cleaned_text)
        clickbait_score = self._analyze_clickbait(cleaned_text)
        
        # NEW: Source domain credibility check
        source_domain_result = self.source_checker.check_domain(source_url) if source_url else None
        source_domain_score = source_domain_result['score'] if source_domain_result else 50
        
        # NEW: Web verification (optional, can be disabled)
        web_verification_result = self.web_verifier.verify_article(cleaned_text, source_url)
        web_verification_score = web_verification_result.get('overall_verification_score', 50) if web_verification_result.get('enabled') else 50
        
        # Calculate weighted overall score (0-100, higher = more credible)
        overall_score = (
            sentiment_score * self.weights['sentiment'] +
            credibility_score * self.weights['credibility'] +
            linguistic_score * self.weights['linguistic'] +
            clickbait_score * self.weights['clickbait'] +
            source_domain_score * self.weights['source_domain'] +
            web_verification_score * self.weights['web_verification']
        )
        
        # Get text statistics
        stats = calculate_text_stats(text)
        
        # Determine verdict and confidence
        verdict, risk_level = self._determine_verdict(overall_score)
        
        # Generate detailed analysis
        analysis = {
            'overall_score': round(overall_score, 1),
            'verdict': verdict,
            'risk_level': risk_level,
            'confidence': self._calculate_confidence(stats['word_count']),
            'factors': {
                'sentiment_analysis': {
                    'score': round(sentiment_score, 1),
                    'weight': self.weights['sentiment'] * 100,
                    'description': self._get_sentiment_description_simple(sentiment_score),
                    'technical': self._get_sentiment_description(sentiment_score)
                },
                'credibility_indicators': {
                    'score': round(credibility_score, 1),
                    'weight': self.weights['credibility'] * 100,
                    'description': self._get_credibility_description_simple(credibility_score),
                    'technical': self._get_credibility_description(credibility_score)
                },
                'linguistic_patterns': {
                    'score': round(linguistic_score, 1),
                    'weight': self.weights['linguistic'] * 100,
                    'description': self._get_linguistic_description_simple(linguistic_score),
                    'technical': self._get_linguistic_description(linguistic_score)
                },
                'clickbait_detection': {
                    'score': round(clickbait_score, 1),
                    'weight': self.weights['clickbait'] * 100,
                    'description': self._get_clickbait_description_simple(clickbait_score),
                    'technical': self._get_clickbait_description(clickbait_score)
                },
                'source_domain_check': {
                    'score': round(source_domain_score, 1),
                    'weight': self.weights['source_domain'] * 100,
                    'description': source_domain_result['message'] if source_domain_result else 'No source URL provided',
                    'category': source_domain_result['category'] if source_domain_result else 'unknown'
                },
                'web_verification': {
                    'score': round(web_verification_score, 1),
                    'weight': self.weights['web_verification'] * 100,
                    'description': web_verification_result.get('recommendation', 'Web verification not available') if web_verification_result.get('enabled') else 'Web verification disabled',
                    'claims_verified': web_verification_result.get('claims_found', 0) if web_verification_result.get('enabled') else 0
                }
            },
            'statistics': stats,
            'summary': self._generate_summary(overall_score, verdict, risk_level, text, stats, source_domain_result),
            'warnings': self._generate_warnings(text, stats, source_domain_result),
            'recommendations': self._generate_recommendations(overall_score, source_domain_result)
        }
        
        return analysis
    
    def _analyze_sentiment(self, text):
        """Analyze sentiment for emotional manipulation detection"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Extreme polarity or high subjectivity can indicate bias
            # Convert to 0-100 scale where higher = more credible
            polarity_score = (1 - abs(polarity)) * 100
            subjectivity_score = (1 - subjectivity) * 100
            
            # Average the two
            sentiment_score = (polarity_score + subjectivity_score) / 2
            
            return sentiment_score
        except:
            return 50.0  # Neutral if analysis fails
    
    def _analyze_credibility(self, text):
        """Analyze credibility indicators in the text"""
        indicators = analyze_source_credibility_indicators(text)
        
        credible = indicators['credible_indicators']
        questionable = indicators['questionable_indicators']
        
        # Calculate score based on ratio of credible to questionable indicators
        if credible + questionable == 0:
            return 50.0  # Neutral if no indicators found
        
        ratio = credible / (credible + questionable)
        credibility_score = ratio * 100
        
        return credibility_score
    
    def _analyze_linguistic_patterns(self, text):
        """Analyze linguistic patterns for professionalism"""
        stats = calculate_text_stats(text)
        
        score = 100.0
        
        # Penalize excessive capitalization (shouting)
        if stats['caps_ratio'] > 0.15:
            score -= 30
        elif stats['caps_ratio'] > 0.10:
            score -= 15
        
        # Penalize excessive exclamation marks
        if stats['exclamation_count'] > 5:
            score -= 25
        elif stats['exclamation_count'] > 2:
            score -= 10
        
        # Penalize very short or very long sentences (lack of balance)
        if stats['avg_sentence_length'] < 8 or stats['avg_sentence_length'] > 35:
            score -= 15
        
        return max(0, score)
    
    def _analyze_clickbait(self, text):
        """Detect clickbait patterns"""
        clickbait_matches = detect_clickbait_patterns(text)
        
        # Each clickbait pattern reduces the score
        penalty = len(clickbait_matches) * 20
        score = max(0, 100 - penalty)
        
        return score
    
    def _determine_verdict(self, score):
        """Determine verdict based on overall score"""
        if score >= 75:
            return "Likely Credible", "low"
        elif score >= 50:
            return "Questionable - Verify Sources", "medium"
        elif score >= 30:
            return "Likely Fake News", "high"
        else:
            return "High Risk - Probable Fake News", "critical"
    
    def _calculate_confidence(self, word_count):
        """Calculate confidence based on text length"""
        if word_count < 50:
            return "Low (insufficient text)"
        elif word_count < 150:
            return "Medium"
        else:
            return "High"
    
    def _get_sentiment_description(self, score):
        """Get description for sentiment score"""
        if score >= 70:
            return "Balanced and objective tone"
        elif score >= 50:
            return "Moderately emotional language"
        else:
            return "Highly emotional or biased language detected"
    
    def _get_credibility_description(self, score):
        """Get description for credibility score"""
        if score >= 70:
            return "Strong credible source indicators"
        elif score >= 50:
            return "Mixed credibility indicators"
        else:
            return "Lacks credible source citations"
    
    def _get_linguistic_description(self, score):
        """Get description for linguistic score"""
        if score >= 70:
            return "Professional writing style"
        elif score >= 50:
            return "Somewhat sensationalized language"
        else:
            return "Highly sensationalized or unprofessional"
    
    def _get_clickbait_description(self, score):
        """Get description for clickbait score"""
        if score >= 80:
            return "No clickbait patterns detected"
        elif score >= 50:
            return "Some clickbait elements present"
        else:
            return "Heavy use of clickbait tactics"
    
    # NEW: Simplified user-friendly methods
    def _get_sentiment_description_simple(self, score):
        return get_sentiment_description_simple(score)
    
    def _get_credibility_description_simple(self, score):
        return get_credibility_description_simple(score)
    
    def _get_linguistic_description_simple(self, score):
        return get_linguistic_description_simple(score)
    
    def _get_clickbait_description_simple(self, score):
        return get_clickbait_description_simple(score)
    
    def _generate_summary(self, score, verdict, risk_level, text, stats, source_domain_result):
        return generate_summary(score, verdict, risk_level, text, stats, source_domain_result)
    
    def _generate_warnings(self, text, stats, source_domain_result=None):
        """Generate specific warnings based on analysis"""
        warnings = []
        
        clickbait = detect_clickbait_patterns(text)
        if clickbait:
            warnings.append(f"Clickbait patterns detected: {', '.join(clickbait[:3])}")
        
        if stats['exclamation_count'] > 3:
            warnings.append(f"Excessive exclamation marks ({stats['exclamation_count']}) may indicate sensationalism")
        
        if stats['caps_ratio'] > 0.10:
            warnings.append("Excessive capitalization detected")
        
        indicators = analyze_source_credibility_indicators(text)
        if indicators['questionable_indicators'] > indicators['credible_indicators']:
            warnings.append("More questionable than credible source indicators")
        
        if stats['word_count'] < 50:
            warnings.append("Text may be too short for accurate analysis")
        
        # NEW: Source domain warnings
        if source_domain_result:
            if source_domain_result['category'] == 'unreliable':
                warnings.append(f"WARNING: {source_domain_result['message']}")
            elif source_domain_result['category'] == 'satire':
                warnings.append(f"NOTE: {source_domain_result['message']}")
        
        return warnings
    
    def _generate_recommendations(self, score, source_domain_result=None):
        """Generate recommendations based on score"""
        recommendations = []
        
        if score < 75:
            recommendations.append("Verify information with multiple credible sources")
        
        if score < 50:
            recommendations.append("Check the original source and publication date")
            recommendations.append("Look for expert opinions and fact-checking websites")
        
        if score < 30:
            recommendations.append("Exercise extreme caution - high likelihood of misinformation")
            recommendations.append("Do not share until verified by trusted sources")
        
        # NEW: Source-specific recommendations
        if source_domain_result:
            source_recs = self.source_checker.get_source_recommendations(source_domain_result['category'])
            recommendations.extend(source_recs)
        
        recommendations.append("Always practice critical thinking when consuming news")
        
        return recommendations
