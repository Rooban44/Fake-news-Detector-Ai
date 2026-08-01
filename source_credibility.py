"""
Source Credibility Database and Domain Verification
Checks news source domains for credibility ratings
"""
from urllib.parse import urlparse


class SourceCredibilityChecker:
    """Check credibility of news source domains"""
    
    def __init__(self):
        # Credible news sources (high trust)
        self.credible_sources = {
            # International
            'bbc.com', 'bbc.co.uk', 'reuters.com', 'apnews.com', 'npr.org',
            'theguardian.com', 'nytimes.com', 'washingtonpost.com', 'wsj.com',
            'economist.com', 'ft.com', 'bloomberg.com', 'cnbc.com',
            
            # Indian credible sources
            'thehindu.com', 'indianexpress.com', 'hindustantimes.com',
            'timesofindia.indiatimes.com', 'ndtv.com', 'thequint.com',
            'scroll.in', 'livemint.com', 'business-standard.com',
            'economictimes.indiatimes.com', 'moneycontrol.com',
            'theprint.in', 'thewire.in', 'news18.com', 'india.com',
            
            # Government/Official sources
            'pib.gov.in', 'mygov.in', 'india.gov.in', 'pmindia.gov.in',
            'who.int', 'un.org', 'gov.uk', 'gov.in',
            
            # Fact-checking sites
            'factcheck.org', 'snopes.com', 'politifact.com',
            'fullfact.org', 'boomlive.in', 'altnews.in', 'factchecker.in'
        }
        
        # Known fake news/unreliable sources
        self.unreliable_sources = {
            'fakingnews.com', 'worldnewsdailyreport.com', 'nationalreport.net',
            'empirenews.net', 'huzlers.com', 'thelastlineofdefense.org',
            'beforeitsnews.com', 'yournewswire.com', 'newspunch.com',
            'infowars.com', 'naturalnews.com', 'breitbart.com'
        }
        
        # Satire/parody sites (not fake news, but not real news)
        self.satire_sources = {
            'theonion.com', 'clickhole.com', 'babylonbee.com',
            'fakingnews.firstpost.com', 'theunrealtimes.com'
        }
    
    def check_domain(self, url):
        """
        Check the credibility of a news source domain
        
        Args:
            url: Full URL or domain name
            
        Returns:
            dict: Credibility assessment with score and category
        """
        if not url:
            return {
                'score': 50,
                'category': 'unknown',
                'message': 'No source URL provided'
            }
        
        # Extract domain from URL
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Remove www. prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            
        except Exception:
            return {
                'score': 50,
                'category': 'unknown',
                'message': 'Invalid URL format'
            }
        
        # Check against databases
        if domain in self.credible_sources:
            return {
                'score': 95,
                'category': 'credible',
                'message': f'{domain} is a known credible news source',
                'domain': domain
            }
        
        elif domain in self.unreliable_sources:
            return {
                'score': 10,
                'category': 'unreliable',
                'message': f'{domain} is flagged as an unreliable source',
                'domain': domain
            }
        
        elif domain in self.satire_sources:
            return {
                'score': 30,
                'category': 'satire',
                'message': f'{domain} is a satire/parody site - content is intentionally fake for humor',
                'domain': domain
            }
        
        else:
            # Unknown source - neutral score
            return {
                'score': 50,
                'category': 'unknown',
                'message': f'{domain} is not in our database - verify independently',
                'domain': domain
            }
    
    def get_source_recommendations(self, category):
        """Get recommendations based on source category"""
        recommendations = {
            'credible': [
                'Source appears credible, but always verify claims independently',
                'Check publication date and author credentials'
            ],
            'unreliable': [
                'This source has a history of publishing misinformation',
                'Do not share content from this source',
                'Verify any claims with credible news organizations',
                'Check fact-checking websites for debunking'
            ],
            'satire': [
                'This is a satire/parody website - content is intentionally fake',
                'Do not share as real news',
                'Content is meant for entertainment, not factual reporting'
            ],
            'unknown': [
                'Source credibility unknown - exercise caution',
                'Check if other credible sources report the same story',
                'Look for author credentials and publication standards',
                'Verify with fact-checking websites'
            ]
        }
        
        return recommendations.get(category, recommendations['unknown'])
