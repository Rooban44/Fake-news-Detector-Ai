"""
Fake News Detector - Flask Application
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from detector import FakeNewsDetector
from file_processor import FileProcessor
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Initialize detector and file processor
detector = FakeNewsDetector()
file_processor = FileProcessor()


@app.route('/')
def index():
    """Serve the main page"""
    return app.send_static_file('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_news():
    """
    Analyze news article for fake news detection
    
    Accepts either:
    - JSON with text and optional source_url
    - Form data with file upload
    """
    try:
        text = None
        source_url = None
        
        # Check if it's a file upload
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({
                    'error': 'No file selected'
                }), 400
            
            # Process the file
            file_data = file.read()
            result = file_processor.process_file(file_data, file.filename)
            
            if not result['success']:
                return jsonify({
                    'error': result['error'],
                    'help': result.get('help', '')
                }), 400
            
            text = result['text']
            source_url = request.form.get('source_url', '')
            
        else:
            # JSON request
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'error': 'No data provided'
                }), 400
            
            text = data.get('text', '').strip()
            source_url = data.get('source_url', '')
        
        if not text:
            return jsonify({
                'error': 'No text provided for analysis'
            }), 400
        
        # Perform analysis
        result = detector.analyze(text, source_url)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Analysis failed: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Fake News Detector API'
    }), 200


if __name__ == '__main__':
    print("=" * 60)
    print("Fake News Detector AI - Starting Server")
    print("=" * 60)
    print("Server running at: http://localhost:5000")
    print("Ready to analyze news articles!")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
