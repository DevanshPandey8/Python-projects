# Sentiment Analysis Web Application

A beautiful and interactive web application built with Flask and TextBlob that performs sentiment analysis on user-entered text. The application classifies text as positive, negative, or neutral and displays polarity and subjectivity scores with visual indicators.

## Features

- **Real-time Sentiment Analysis**: Analyze text sentiment using TextBlob's natural language processing
- **Visual Results**: Beautiful charts and progress bars showing polarity and subjectivity scores
- **Interactive UI**: Modern, responsive design with Bootstrap 5
- **Multiple Input Methods**: Web form and REST API support
- **Error Handling**: Comprehensive error handling and validation
- **Character Counter**: Real-time character counting with limits
- **Example Texts**: Built-in examples for testing different sentiments

## Screenshots

The application features a modern, gradient-styled interface with:
- Clean input form with character counter
- Visual sentiment classification with icons
- Progress bars showing polarity (-1 to +1) and subjectivity (0 to 1) scores
- Responsive design that works on all devices

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd "Sentiment Analysis Web App"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv sentiment_env
   sentiment_env\Scripts\activate  # On Windows
   # source sentiment_env/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download TextBlob corpora** (required for first run)
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## Usage

### Web Interface

1. **Enter Text**: Type or paste your text in the textarea (max 5000 characters)
2. **Analyze**: Click the "Analyze Sentiment" button
3. **View Results**: See the sentiment classification and detailed scores

### API Usage

Send POST requests to `/api/analyze` with JSON payload:

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this amazing product!"}'
```

Response:
```json
{
  "text": "I love this amazing product!",
  "sentiment": "Positive",
  "polarity": 0.625,
  "subjectivity": 0.6,
  "polarity_percentage": 81.2,
  "subjectivity_percentage": 60.0
}
```

## Understanding the Scores

### Sentiment Classification
- **Positive**: Polarity > 0.1
- **Negative**: Polarity < -0.1
- **Neutral**: Polarity between -0.1 and 0.1

### Polarity Score
- **Range**: -1.0 to +1.0
- **-1.0**: Most negative sentiment
- **0.0**: Neutral sentiment
- **+1.0**: Most positive sentiment

### Subjectivity Score
- **Range**: 0.0 to 1.0
- **0.0**: Objective (factual)
- **1.0**: Subjective (opinionated)

## Project Structure

```
Sentiment Analysis Web App/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/            # HTML templates
    ├── index.html        # Main application page
    ├── 404.html         # 404 error page
    └── 500.html         # 500 error page
```

## API Endpoints

- `GET /` - Main application page
- `POST /analyze` - Web form sentiment analysis
- `POST /api/analyze` - REST API endpoint for sentiment analysis

## Dependencies

- **Flask 2.3.3**: Web framework
- **TextBlob 0.17.1**: Natural language processing
- **NLTK 3.8.1**: Natural language toolkit (dependency for TextBlob)
- **Bootstrap 5.1.3**: Frontend framework (CDN)
- **Font Awesome 6.0.0**: Icons (CDN)

## Technical Details

### Sentiment Analysis Logic
The application uses TextBlob's built-in sentiment analysis, which:
- Analyzes text polarity and subjectivity
- Uses a naive Bayes classifier trained on movie reviews
- Provides reliable results for general text analysis

### Error Handling
- Input validation (empty text, length limits)
- Exception handling for analysis errors
- Custom error pages (404, 500)
- Graceful error messages

### Performance Considerations
- Text length limited to 5000 characters
- Efficient TextBlob processing
- Responsive design for various devices

## Example Texts

Try these examples to see different sentiment classifications:

**Positive Examples:**
- "I absolutely love this new product! It's amazing and works perfectly."
- "What a beautiful day! I'm feeling great and excited about the future."

**Negative Examples:**
- "This is terrible! I hate how complicated everything is."
- "I'm really disappointed and frustrated with this service."

**Neutral Examples:**
- "The meeting is scheduled for tomorrow at 3 PM."
- "Python is a programming language used for web development."

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **NLTK data missing**: Download required corpora
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
   ```

3. **Port already in use**: Change port in app.py or stop other services using port 5000

### Development Mode

The application runs in debug mode by default for development. For production:
- Set `debug=False` in `app.py`
- Use a proper WSGI server like Gunicorn
- Configure environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Future Enhancements

- Support for multiple languages
- Batch text analysis
- Export results to CSV/JSON
- User authentication and history
- Advanced visualization charts
- Custom sentiment models
- Real-time analysis as you type

## Contact

For questions or support, please open an issue on the repository.
