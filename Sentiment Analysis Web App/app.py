from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_sentiment(text):
    """
    Analyze sentiment of the given text using TextBlob
    Returns: dict with sentiment classification, polarity, and subjectivity
    """
    try:
        # Create TextBlob object
        blob = TextBlob(text)
        
        # Get polarity (-1 to 1) and subjectivity (0 to 1)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Classify sentiment based on polarity
        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        return {
            'text': text,
            'sentiment': sentiment,
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'polarity_percentage': round((polarity + 1) * 50, 1),  # Convert to 0-100 scale
            'subjectivity_percentage': round(subjectivity * 100, 1)  # Convert to 0-100 scale
        }
    
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        return {
            'error': f"Error analyzing sentiment: {str(e)}"
        }

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze sentiment for the submitted text"""
    try:
        # Get text from form or JSON
        if request.is_json:
            data = request.get_json()
            text = data.get('text', '').strip()
        else:
            text = request.form.get('text', '').strip()
        
        # Validate input
        if not text:
            return jsonify({'error': 'Please enter some text to analyze'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text is too long. Please limit to 5000 characters.'}), 400
        
        # Analyze sentiment
        result = analyze_sentiment(text)
        
        # Return JSON response for AJAX requests
        if request.is_json or request.headers.get('Content-Type') == 'application/json':
            return jsonify(result)
        
        # Render template with results for form submissions
        return render_template('index.html', result=result)
    
    except Exception as e:
        logger.error(f"Error in analyze route: {str(e)}")
        error_msg = f"An error occurred: {str(e)}"
        
        if request.is_json:
            return jsonify({'error': error_msg}), 500
        
        return render_template('index.html', error=error_msg)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for sentiment analysis"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Missing text field in request body'}), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text is too long. Please limit to 5000 characters.'}), 400
        
        result = analyze_sentiment(text)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in API analyze: {str(e)}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
