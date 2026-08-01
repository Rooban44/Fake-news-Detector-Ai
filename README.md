# Fake News Detector AI

A professional AI-powered news verification system that analyzes articles for credibility using 6 comprehensive analysis factors including sentiment analysis, source verification, linguistic patterns, clickbait detection, domain reputation checking, and web-based fact verification.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🎯 Features

- **6-Factor AI Analysis**: Multi-dimensional credibility scoring
- **File Upload Support**: Analyze text from images (OCR), PDFs, and text files
- **Source Domain Verification**: Database of 50+ credible and unreliable news sources
- **Web-Based Fact Checking**: Automated claim extraction and verification
- **User-Friendly Interface**: Professional, clean design with simple language
- **Real-Time Analysis**: Results in under 1 second
- **Privacy-Focused**: No data storage, all processing done locally

## 📊 Analysis Factors

1. **Tone & Emotion** (15% weight) - Detects emotional manipulation and bias
2. **Sources & Experts** (25% weight) - Checks for credible citations and expert quotes
3. **Writing Quality** (20% weight) - Analyzes professionalism and linguistic patterns
4. **Clickbait Check** (20% weight) - Identifies sensational phrases and tactics
5. **Website Reputation** (10% weight) - Verifies source domain credibility
6. **Fact Check** (10% weight) - Cross-references claims for verification

## 🏗️ Project Architecture

```
fake-news-detector/
├── app.py                      # Flask web application
├── detector.py                 # Main detection engine
├── detector_helpers.py         # User-friendly descriptions
├── utils.py                    # Text analysis utilities
├── source_credibility.py       # Domain reputation checker
├── web_verifier.py            # Claim verification module
├── file_processor.py          # File upload handler (images/PDFs/text)
├── requirements.txt           # Python dependencies
├── static/                    # Frontend assets
│   ├── index.html            # Main webpage
│   ├── style.css             # Base styles
│   ├── enhancements.css      # Feature enhancements
│   ├── professional-theme.css # Professional UI theme
│   ├── button-fix.css        # Button styling fixes
│   ├── divider-fix.css       # Form divider fixes
│   ├── script.js             # Main JavaScript
│   └── file_upload.js        # File upload handling
└── test_files/               # Sample test files
    ├── test_fake_news.txt
    ├── test_credible_news.txt
    ├── test_fake_news.pdf
    └── test_fake_news.png
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) Tesseract OCR for image text extraction

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- Flask 3.0.0 - Web framework
- Flask-CORS 4.0.0 - Cross-origin resource sharing
- nltk 3.8.1 - Natural language processing
- textblob 0.17.1 - Text analysis
- numpy 1.24.3 - Numerical computing
- requests 2.31.0 - HTTP library
- Pillow 10.1.0 - Image processing
- PyPDF2 3.0.1 - PDF text extraction
- pytesseract 0.3.10 - OCR support

### Step 2: Download NLTK Data (First Time Only)

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Step 3: Run the Application

```bash
python app.py
```

The server will start at `http://localhost:5000`

## � How to Use

### Option 1: Text Analysis

1. Open `http://localhost:5000` in your browser
2. Paste news article text into the text area
3. (Optional) Add the source URL
4. Click "Analyze Article"
5. View detailed results with credibility score, summary, and factor breakdown

### Option 2: File Upload

1. Click the file upload area or drag & drop a file
2. Supported formats: JPG, PNG, PDF, TXT
3. (Optional) Add the source URL
4. Click "Analyze Article"
5. The system will extract text and analyze it

## 🧪 Testing

### Test Files Included

The project includes 4 test files in the root directory:

1. **test_fake_news.txt** - Text file with obvious fake news indicators
2. **test_credible_news.txt** - Text file with credible news content
3. **test_fake_news.pdf** - PDF document with fake news
4. **test_fake_news.png** - Image with clickbait text

### Running Tests

**Test 1: Fake News Detection**
```bash
# Upload test_fake_news.txt or test_fake_news.pdf
# Expected: Score 20-35/100, "LIKELY FAKE" badge
# Summary will explain why (clickbait, no sources, emotional language)
```

**Test 2: Credible News Detection**
```bash
# Upload test_credible_news.txt
# Expected: Score 85-95/100, "CREDIBLE" badge
# Summary will highlight expert citations and professional writing
```

**Test 3: API Testing**
```bash
python test_uploads.py
# Tests all file upload types (TXT, PDF, PNG)
# Verifies API responses and data structure
```

## 🔧 How It Works

### 1. Text Processing Pipeline

```
Input (Text/File) → Text Extraction → Cleaning → Analysis → Scoring → Results
```

### 2. Analysis Process

**Step 1: Text Extraction**
- Direct text input: Used as-is
- PDF files: PyPDF2 extracts text from pages
- Images: Tesseract OCR extracts text (if available)
- Text files: Read with UTF-8 encoding

**Step 2: Multi-Factor Analysis**

Each factor runs independently:

- **Sentiment Analysis**: Uses TextBlob to measure polarity and subjectivity
- **Credibility Indicators**: Regex patterns detect citations, research, experts
- **Linguistic Patterns**: Analyzes capitalization, punctuation, sentence structure
- **Clickbait Detection**: Pattern matching for sensational phrases
- **Source Domain**: URL parsing and database lookup (50+ domains)
- **Web Verification**: Claim extraction and credibility indicator detection

**Step 3: Weighted Scoring**

```python
overall_score = (
    sentiment_score * 0.15 +
    credibility_score * 0.25 +
    linguistic_score * 0.20 +
    clickbait_score * 0.20 +
    source_domain_score * 0.10 +
    web_verification_score * 0.10
)
```

**Step 4: Verdict Generation**

- Score ≥ 75: "Likely Credible" (Green badge)
- Score 50-74: "Questionable" (Yellow badge)
- Score 30-49: "Likely Fake News" (Orange badge)
- Score < 30: "Fake News" (Red badge)

**Step 5: Summary Generation**

AI generates a plain-English summary explaining:
- Overall assessment
- Key red flags found (clickbait, no sources, etc.)
- Specific recommendations

### 3. Source Domain Database

**Credible Sources (Score: 95/100)**
- International: BBC, Reuters, AP News, The Guardian, NPR
- Indian: The Hindu, Indian Express, NDTV, The Quint
- Government: PIB, WHO, UN
- Fact-Checking: FactCheck.org, Snopes, AltNews

**Unreliable Sources (Score: 10/100)**
- Known fake news sites
- Clickbait content farms

**Satire Sites (Score: 30/100)**
- The Onion, Babylon Bee, Faking News

## 📈 API Endpoints

### POST /api/analyze

**Request (JSON):**
```json
{
  "text": "News article text...",
  "source_url": "https://example.com/article"
}
```

**Request (Form Data - File Upload):**
```
file: <binary file data>
source_url: https://example.com/article (optional)
```

**Response:**
```json
{
  "overall_score": 31.6,
  "verdict": "Likely Fake News",
  "risk_level": "high",
  "confidence": "Medium",
  "summary": "❌ This article is likely FAKE NEWS. It uses clickbait phrases...",
  "factors": {
    "sentiment_analysis": {
      "score": 63.7,
      "weight": 15.0,
      "description": "Somewhat emotional language"
    }
  },
  "warnings": ["Clickbait patterns detected"],
  "recommendations": ["Verify with multiple sources"],
  "statistics": {
    "word_count": 85,
    "sentence_count": 11,
    "exclamation_count": 10
  }
}
```

## 🎨 UI Features

- **Professional Design**: Clean, corporate-style interface
- **Visual Verdict Badges**: Large, color-coded credibility indicators
- **Plain English**: No technical jargon, user-friendly descriptions
- **Responsive Layout**: Works on desktop and mobile
- **File Upload**: Drag-and-drop support
- **Real-Time Feedback**: Loading states and error handling

## 🔒 Privacy & Security

- **No Data Storage**: Articles are not saved or logged
- **Local Processing**: All analysis done on your server
- **No External APIs**: Self-contained system (except optional OCR)
- **Open Source**: Full transparency of analysis methods

## �️ Troubleshooting

**Issue: Image upload not working**
- Solution: Install Tesseract OCR for image text extraction
- Alternative: Use PDF or text files instead

**Issue: Server won't start**
- Check if port 5000 is available
- Verify all dependencies are installed: `pip install -r requirements.txt`

**Issue: Low accuracy**
- Ensure text has at least 20 characters
- Provide source URL for better domain verification
- Check that text is in English

## 📝 License

MIT License - Feel free to use and modify for your projects.

## 👥 Contributing

Contributions welcome! Areas for improvement:
- Additional language support
- More source domains in database
- Enhanced ML models
- Mobile app version

## 📧 Support

For issues or questions, please check the troubleshooting section or review the code comments for detailed explanations.

---

**Built with ❤️ for a more informed world**
