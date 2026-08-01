"""
Helper functions for user-friendly descriptions and summary generation
"""
from utils import detect_clickbait_patterns, analyze_source_credibility_indicators


def get_sentiment_description_simple(score):
    """Get user-friendly description for sentiment"""
    if score >= 70:
        return "Calm and balanced language ✓"
    elif score >= 50:
        return "Somewhat emotional language"
    else:
        return "Very emotional or one-sided language ⚠️"


def get_credibility_description_simple(score):
    """Get user-friendly description for credibility"""
    if score >= 70:
        return "Cites experts and reliable sources ✓"
    elif score >= 50:
        return "Has some sources mentioned"
    else:
        return "No credible sources or expert quotes ⚠️"


def get_linguistic_description_simple(score):
    """Get user-friendly description for linguistic patterns"""
    if score >= 70:
        return "Professional writing style ✓"
    elif score >= 50:
        return "Some sensational language"
    else:
        return "Lots of CAPS and exclamation marks!!! ⚠️"


def get_clickbait_description_simple(score):
    """Get user-friendly description for clickbait"""
    if score >= 80:
        return "No clickbait found ✓"
    elif score >= 50:
        return "Some attention-grabbing phrases"
    else:
        return "Full of clickbait like 'You won't believe...' ⚠️"


def generate_summary(score, verdict, risk_level, text, stats, source_domain_result):
    """Generate a brief, user-friendly summary of why the news is fake or credible"""
    summary_parts = []
    
    # Overall assessment
    if score >= 75:
        summary_parts.append("✅ This article appears to be CREDIBLE.")
    elif score >= 50:
        summary_parts.append("⚠️ This article is QUESTIONABLE and needs verification.")
    elif score >= 30:
        summary_parts.append("❌ This article is likely FAKE NEWS.")
    else:
        summary_parts.append("🚨 This article is HIGHLY LIKELY TO BE FAKE NEWS.")
    
    # Key reasons
    reasons = []
    
    # Check clickbait
    clickbait = detect_clickbait_patterns(text)
    if clickbait:
        reasons.append(f"uses clickbait phrases like '{clickbait[0]}'")
    
    # Check exclamation marks
    if stats['exclamation_count'] > 5:
        reasons.append(f"has {stats['exclamation_count']} exclamation marks (sign of sensationalism)")
    
    # Check source credibility
    indicators = analyze_source_credibility_indicators(text)
    if indicators['credible_indicators'] > 2:
        reasons.append("cites credible sources and experts")
    elif indicators['questionable_indicators'] > indicators['credible_indicators']:
        reasons.append("uses vague sources like 'anonymous' or 'people are saying'")
    
    # Check source domain
    if source_domain_result:
        if source_domain_result['category'] == 'credible':
            reasons.append(f"comes from a trusted news source ({source_domain_result.get('domain', 'verified source')})")
        elif source_domain_result['category'] == 'unreliable':
            reasons.append(f"comes from a known fake news website ({source_domain_result.get('domain', 'unreliable source')})")
        elif source_domain_result['category'] == 'satire':
            reasons.append(f"comes from a satire/parody website ({source_domain_result.get('domain', 'satire site')})")
    
    # Check capitalization
    if stats['caps_ratio'] > 0.10:
        reasons.append("uses excessive CAPITALIZATION")
    
    # Build summary
    if reasons:
        summary_parts.append(f"It {' and '.join(reasons[:3])}.")
    
    # Add recommendation
    if score < 50:
        summary_parts.append("⚠️ Do NOT share this without verifying from trusted sources first!")
    elif score < 75:
        summary_parts.append("💡 Check other reliable news sources before sharing.")
    
    return " ".join(summary_parts)
