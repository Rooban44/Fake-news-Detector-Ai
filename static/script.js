// Fake News Detector - Frontend JavaScript
const API_URL = '/api/analyze';

// DOM Elements
const analyzerForm = document.getElementById('analyzerForm');
const newsText = document.getElementById('newsText');
const sourceUrl = document.getElementById('sourceUrl');
const charCount = document.getElementById('charCount');
const analyzeBtn = document.getElementById('analyzeBtn');
const btnText = document.getElementById('btnText');
const resultsContainer = document.getElementById('resultsContainer');
const resetBtn = document.getElementById('resetBtn');

// Character counter
newsText.addEventListener('input', () => {
    const count = newsText.value.length;
    charCount.textContent = `${count} character${count !== 1 ? 's' : ''}`;
});

// Form submission
analyzerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const text = newsText.value.trim();
    const source = sourceUrl.value.trim();

    // Check if file is selected (from file_upload.js)
    const fileInput = document.getElementById('fileInput');
    const hasFile = fileInput && fileInput.files && fileInput.files.length > 0;

    if (!hasFile && !text) {
        showError('Please enter some text or upload a file to analyze');
        return;
    }

    if (!hasFile && text.length < 20) {
        showError('Please provide at least 20 characters for accurate analysis');
        return;
    }

    // Show loading state
    setLoadingState(true);

    try {
        let response;

        if (hasFile) {
            // File upload
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            if (source) {
                formData.append('source_url', source);
            }

            response = await fetch(API_URL, {
                method: 'POST',
                body: formData
            });
        } else {
            // Text analysis
            response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    source_url: source
                })
            });
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }

        displayResults(data);

    } catch (error) {
        showError(error.message);
    } finally {
        setLoadingState(false);
    }
});

// Reset button
resetBtn.addEventListener('click', () => {
    analyzerForm.reset();
    resultsContainer.style.display = 'none';
    charCount.textContent = '0 characters';
    newsText.focus();

    // Smooth scroll to form
    analyzerForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
});

// Set loading state
function setLoadingState(isLoading) {
    if (isLoading) {
        analyzeBtn.classList.add('loading');
        btnText.textContent = 'Analyzing...';
        analyzeBtn.disabled = true;
    } else {
        analyzeBtn.classList.remove('loading');
        btnText.textContent = 'Analyze Article';
        analyzeBtn.disabled = false;
    }
}

// Display results
function displayResults(data) {
    // Show results container
    resultsContainer.style.display = 'block';

    // Display overall score with badge
    displayOverallScore(data);

    // Display summary
    if (data.summary) {
        displaySummary(data.summary);
    }

    // Display factor analysis
    displayFactors(data.factors);

    // Display warnings
    displayWarnings(data.warnings);

    // Display recommendations
    displayRecommendations(data.recommendations);

    // Display statistics
    displayStatistics(data.statistics);

    // Smooth scroll to results
    setTimeout(() => {
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// Display overall score with visual badge
function displayOverallScore(data) {
    const scoreCard = document.getElementById('overallScore');
    const riskClass = `risk-${data.risk_level}`;

    // Determine badge
    let badge = '';
    if (data.overall_score >= 75) {
        badge = '<div class="verdict-badge verdict-credible">✓ CREDIBLE</div>';
    } else if (data.overall_score >= 50) {
        badge = '<div class="verdict-badge verdict-questionable">? QUESTIONABLE</div>';
    } else if (data.overall_score >= 30) {
        badge = '<div class="verdict-badge verdict-fake">✗ LIKELY FAKE</div>';
    } else {
        badge = '<div class="verdict-badge verdict-fake-critical">⚠ FAKE NEWS</div>';
    }

    scoreCard.innerHTML = `
        ${badge}
        <div class="score-value ${riskClass}">${data.overall_score}<span style="font-size: 2rem;">/100</span></div>
        <div class="score-label">Credibility Score</div>
        <div class="score-verdict ${riskClass}">${data.verdict}</div>
        <div class="score-confidence">Confidence: ${data.confidence}</div>
    `;
}

// Display summary
function displaySummary(summary) {
    const summaryContainer = document.getElementById('summaryContainer');

    if (!summary) {
        summaryContainer.style.display = 'none';
        return;
    }

    summaryContainer.style.display = 'block';
    summaryContainer.innerHTML = `
        <div class="summary-title">📋 Quick Summary</div>
        <div class="summary-text">${summary}</div>
    `;
}

// Display factors
function displayFactors(factors) {
    const factorsGrid = document.getElementById('factorsGrid');

    const factorNames = {
        'sentiment_analysis': 'Tone & Emotion',
        'credibility_indicators': 'Sources & Experts',
        'linguistic_patterns': 'Writing Quality',
        'clickbait_detection': 'Clickbait Check',
        'source_domain_check': 'Website Reputation',
        'web_verification': 'Fact Check'
    };

    factorsGrid.innerHTML = Object.entries(factors).map(([key, factor]) => {
        const scoreClass = getScoreClass(factor.score);

        return `
            <div class="factor-card">
                <div class="factor-header">
                    <div class="factor-name">${factorNames[key] || key}</div>
                    <div class="factor-score ${scoreClass}">${factor.score}</div>
                </div>
                <div class="factor-description">${factor.description}</div>
            </div>
        `;
    }).join('');
}

// Display warnings
function displayWarnings(warnings) {
    const warningsContainer = document.getElementById('warningsContainer');

    if (!warnings || warnings.length === 0) {
        warningsContainer.style.display = 'none';
        return;
    }

    warningsContainer.style.display = 'block';
    warningsContainer.innerHTML = `
        <div class="warnings-title">⚠️ Warnings Detected</div>
        ${warnings.map(warning => `
            <div class="warning-item">${warning}</div>
        `).join('')}
    `;
}

// Display recommendations
function displayRecommendations(recommendations) {
    const recommendationsContainer = document.getElementById('recommendationsContainer');

    if (!recommendations || recommendations.length === 0) {
        recommendationsContainer.style.display = 'none';
        return;
    }

    recommendationsContainer.style.display = 'block';
    recommendationsContainer.innerHTML = `
        <div class="recommendations-title">💡 Recommendations</div>
        ${recommendations.map(rec => `
            <div class="recommendation-item">${rec}</div>
        `).join('')}
    `;
}

// Display statistics
function displayStatistics(stats) {
    const statisticsContainer = document.getElementById('statisticsContainer');

    statisticsContainer.innerHTML = `
        <div class="statistics-title">📊 Text Statistics</div>
        <div class="statistics-grid">
            <div class="stat-item">
                <div class="stat-item-value">${stats.word_count}</div>
                <div class="stat-item-label">Words</div>
            </div>
            <div class="stat-item">
                <div class="stat-item-value">${stats.sentence_count}</div>
                <div class="stat-item-label">Sentences</div>
            </div>
            <div class="stat-item">
                <div class="stat-item-value">${Math.round(stats.avg_sentence_length)}</div>
                <div class="stat-item-label">Avg Sentence Length</div>
            </div>
            <div class="stat-item">
                <div class="stat-item-value">${stats.exclamation_count}</div>
                <div class="stat-item-label">Exclamation Marks</div>
            </div>
            <div class="stat-item">
                <div class="stat-item-value">${(stats.caps_ratio * 100).toFixed(1)}%</div>
                <div class="stat-item-label">Capitalization</div>
            </div>
            <div class="stat-item">
                <div class="stat-item-value">${stats.question_count}</div>
                <div class="stat-item-label">Question Marks</div>
            </div>
        </div>
    `;
}

// Get score class based on value
function getScoreClass(score) {
    if (score >= 75) return 'risk-low';
    if (score >= 50) return 'risk-medium';
    if (score >= 30) return 'risk-high';
    return 'risk-critical';
}

// Show error message
function showError(message) {
    // Create error toast
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: linear-gradient(135deg, #e11d48 0%, #be123c 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        z-index: 10000;
        animation: slideInRight 0.3s ease-out;
        max-width: 400px;
    `;
    toast.textContent = `❌ ${message}`;

    document.body.appendChild(toast);

    // Remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
