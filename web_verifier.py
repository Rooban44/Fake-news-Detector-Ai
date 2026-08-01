"""
Web-based Fact Verification Module
Performs online verification of claims using web search and fact-checking APIs
"""
import re
import requests
from urllib.parse import quote_plus


class WebVerifier:
    """Verify news claims using web search and fact-checking"""
    
    def __init__(self):
        self.timeout = 5  # seconds
        self.enabled = True
    
    def extract_key_claims(self, text):
        """Extract key factual claims from text"""
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Filter for sentences that look like factual claims
        claims = []
        
        # Look for sentences with specific indicators
        claim_indicators = [
            r'\d+\s*(percent|%)',  # Statistics
            r'according to',
            r'research shows',
            r'study found',
            r'data (shows|suggests|indicates)',
            r'experts? (say|claim|state)',
            r'report(s|ed)',
            r'announced',
            r'confirmed',
            r'revealed'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:  # Too short
                continue
            
            # Check if sentence contains claim indicators
            for indicator in claim_indicators:
                if re.search(indicator, sentence, re.IGNORECASE):
                    claims.append(sentence)
                    break
        
        return claims[:3]  # Return top 3 claims
    
    def search_claim_verification(self, claim):
        """
        Search for claim verification (simulated - would use real API in production)
        
        In production, this would:
        1. Use Google Fact Check Tools API
        2. Search fact-checking databases
        3. Query news aggregators
        
        For now, returns a simulated response based on keywords
        """
        # Simulate fact-checking logic
        # In production, replace with actual API calls
        
        claim_lower = claim.lower()
        
        # Check for common fake news indicators
        fake_indicators = [
            'anonymous source', 'allegedly', 'supposedly', 'rumor',
            'unconfirmed', 'many believe', 'people are saying'
        ]
        
        credible_indicators = [
            'according to', 'research', 'study', 'data', 'expert',
            'published', 'peer-reviewed', 'official', 'confirmed'
        ]
        
        fake_count = sum(1 for indicator in fake_indicators if indicator in claim_lower)
        credible_count = sum(1 for indicator in credible_indicators if indicator in claim_lower)
        
        if credible_count > fake_count:
            return {
                'claim': claim,
                'verification_status': 'likely_true',
                'confidence': 'medium',
                'note': 'Claim contains credible source indicators'
            }
        elif fake_count > credible_count:
            return {
                'claim': claim,
                'verification_status': 'questionable',
                'confidence': 'medium',
                'note': 'Claim lacks credible source citations'
            }
        else:
            return {
                'claim': claim,
                'verification_status': 'unverified',
                'confidence': 'low',
                'note': 'Unable to verify - check multiple sources'
            }
    
    def verify_article(self, text, source_url=None):
        """
        Perform web-based verification of article
        
        Args:
            text: Article text
            source_url: Optional source URL
            
        Returns:
            dict: Verification results
        """
        if not self.enabled:
            return {
                'enabled': False,
                'message': 'Web verification disabled'
            }
        
        # Extract key claims
        claims = self.extract_key_claims(text)
        
        if not claims:
            return {
                'enabled': True,
                'claims_found': 0,
                'message': 'No specific factual claims detected for verification'
            }
        
        # Verify each claim
        verifications = []
        for claim in claims:
            verification = self.search_claim_verification(claim)
            verifications.append(verification)
        
        # Calculate overall verification score
        status_scores = {
            'likely_true': 80,
            'unverified': 50,
            'questionable': 30,
            'likely_false': 10
        }
        
        avg_score = sum(status_scores.get(v['verification_status'], 50) 
                       for v in verifications) / len(verifications)
        
        return {
            'enabled': True,
            'claims_found': len(claims),
            'verifications': verifications,
            'overall_verification_score': round(avg_score, 1),
            'recommendation': self._get_verification_recommendation(avg_score)
        }
    
    def _get_verification_recommendation(self, score):
        """Get recommendation based on verification score"""
        if score >= 70:
            return 'Claims appear verifiable with credible indicators'
        elif score >= 50:
            return 'Mixed verification - some claims need independent confirmation'
        else:
            return 'Multiple claims lack credible verification - exercise caution'


# Google Fact Check Tools API integration (optional - requires API key)
class FactCheckAPI:
    """Integration with Google Fact Check Tools API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = 'https://factchecktools.googleapis.com/v1alpha1/claims:search'
    
    def search_claim(self, query):
        """
        Search for fact-checks of a claim
        
        Requires Google Fact Check Tools API key
        Get free key at: https://developers.google.com/fact-check/tools/api
        """
        if not self.api_key:
            return {
                'error': 'API key not configured',
                'message': 'To enable fact-checking API, add your Google Fact Check Tools API key'
            }
        
        try:
            params = {
                'query': query,
                'key': self.api_key,
                'languageCode': 'en'
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_fact_check_response(data)
            else:
                return {
                    'error': 'API request failed',
                    'status_code': response.status_code
                }
                
        except Exception as e:
            return {
                'error': 'API request failed',
                'message': str(e)
            }
    
    def _parse_fact_check_response(self, data):
        """Parse Google Fact Check API response"""
        if 'claims' not in data or not data['claims']:
            return {
                'found': False,
                'message': 'No fact-checks found for this claim'
            }
        
        fact_checks = []
        for claim in data['claims']:
            for review in claim.get('claimReview', []):
                fact_checks.append({
                    'claim_text': claim.get('text', ''),
                    'rating': review.get('textualRating', 'Unknown'),
                    'publisher': review.get('publisher', {}).get('name', 'Unknown'),
                    'url': review.get('url', '')
                })
        
        return {
            'found': True,
            'fact_checks': fact_checks,
            'count': len(fact_checks)
        }
