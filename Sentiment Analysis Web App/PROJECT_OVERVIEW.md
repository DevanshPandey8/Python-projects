# Sentiment Analysis Web Application - Project Overview

## 🎯 Project Description

A complete web application built with Flask that performs sentiment analysis on user-entered text using TextBlob. The application provides a beautiful, responsive interface and classifies text as positive, negative, or neutral while displaying detailed polarity and subjectivity scores.

## 🚀 Quick Start

### Option 1: Using the Batch File (Windows)
1. Double-click `run_app.bat`
2. The script will automatically set up everything and start the server
3. Open http://localhost:5000 in your browser

### Option 2: Manual Setup
1. Install Python 3.7+ if not already installed
2. Open Command Prompt/PowerShell in this directory
3. Create virtual environment: `python -m venv venv`
4. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (macOS/Linux)
5. Install dependencies: `pip install -r requirements.txt`
6. Download NLTK data: `python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"`
7. Run the app: `python app.py`
8. Open http://localhost:5000 in your browser

### Option 3: Using Start Script
1. Run: `python start_app.py`
2. This script includes automatic setup and error checking

## 📁 Project Structure

```
Sentiment Analysis Web App/
├── 📄 app.py                    # Main Flask application with all routes and logic
├── 📄 start_app.py              # Alternative startup script with error handling
├── 📄 demo.py                   # Simple demonstration of sentiment analysis
├── 📄 test_sentiment.py         # Comprehensive test suite
├── 📄 requirements.txt          # Python package dependencies
├── 📄 run_app.bat              # Windows batch file for easy startup
├── 📄 README.md                # Detailed documentation
├── 📄 PROJECT_OVERVIEW.md      # This file
└── 📁 templates/               # HTML templates
    ├── 📄 index.html           # Main application interface
    ├── 📄 404.html             # 404 error page
    └── 📄 500.html             # 500 error page
```

## 🔧 Key Features

### Web Interface
- **Modern Design**: Beautiful gradient UI with Bootstrap 5
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Real-time Features**: Character counter, loading states
- **Interactive Elements**: Example texts, progress bars
- **Error Handling**: Graceful error messages and validation

### Sentiment Analysis
- **TextBlob Integration**: Professional NLP library
- **Three Classifications**: Positive, Negative, Neutral
- **Detailed Scores**: Polarity (-1 to +1) and Subjectivity (0 to 1)
- **Visual Indicators**: Progress bars and color-coded results
- **Score Explanations**: User-friendly explanations of metrics

### Technical Features
- **REST API**: JSON endpoint at `/api/analyze`
- **Input Validation**: Length limits, empty text checks
- **Error Pages**: Custom 404 and 500 error handling
- **Logging**: Comprehensive error logging
- **Security**: Input sanitization and validation

## 🎨 User Interface

### Main Page Elements
1. **Header Section**: Attractive gradient header with title and description
2. **Input Area**: Large textarea with character counter (max 5000 chars)
3. **Analysis Button**: Prominent call-to-action button
4. **Results Section**: Visual display of sentiment classification and scores
5. **Progress Bars**: Visual representation of polarity and subjectivity
6. **Examples Modal**: Pre-built example texts for testing

### Visual Design
- **Color Scheme**: Purple gradient theme with professional appearance
- **Icons**: Font Awesome icons throughout the interface
- **Typography**: Clean, readable fonts with proper hierarchy
- **Animations**: Smooth transitions and hover effects
- **Loading States**: Visual feedback during analysis

## 🔧 Technical Implementation

### Backend (Flask)
- **Routes**: Main page, form handler, API endpoint
- **Analysis Function**: Core sentiment analysis using TextBlob
- **Error Handling**: Try-catch blocks with user-friendly messages
- **Validation**: Input length and content validation
- **Logging**: Error logging for debugging

### Frontend (HTML/CSS/JS)
- **Bootstrap 5**: Responsive grid system and components
- **Custom CSS**: Gradient themes and visual enhancements
- **JavaScript**: Character counting, form handling, examples
- **Progressive Enhancement**: Works without JavaScript

### Libraries & Dependencies
- **Flask 2.3.3**: Web framework
- **TextBlob 0.17.1**: Natural language processing
- **NLTK 3.8.1**: Language toolkit (TextBlob dependency)
- **Bootstrap 5.1.3**: Frontend framework
- **Font Awesome 6.0.0**: Icon library

## 📊 Sentiment Analysis Details

### How It Works
1. User enters text in the web form
2. Text is sent to Flask backend
3. TextBlob analyzes the text sentiment
4. Results are processed and formatted
5. Visual results are displayed to user

### Score Interpretation
- **Polarity Score**: Emotional attitude measurement
  - +1.0: Very positive
  - 0.0: Neutral
  - -1.0: Very negative

- **Subjectivity Score**: Opinion vs. fact measurement
  - 1.0: Very subjective (opinion-based)
  - 0.0: Very objective (fact-based)

### Classification Logic
- **Positive**: Polarity > 0.1
- **Negative**: Polarity < -0.1  
- **Neutral**: Polarity between -0.1 and 0.1

## 🧪 Testing

### Test Files Included
1. **demo.py**: Simple demonstration with examples
2. **test_sentiment.py**: Comprehensive test suite with:
   - Positive, negative, neutral examples
   - Edge cases (empty text, long text, special chars)
   - Error handling validation
   - TextBlob installation verification

### Running Tests
```bash
python demo.py          # Quick demonstration
python test_sentiment.py   # Full test suite
```

## 🌐 API Usage

### Endpoint: POST /api/analyze
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here"}'
```

### Response Format
```json
{
  "text": "Your text here",
  "sentiment": "Positive",
  "polarity": 0.8,
  "subjectivity": 0.6,
  "polarity_percentage": 90.0,
  "subjectivity_percentage": 60.0
}
```

## 🚦 Development Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Internet connection (for CDN resources)

### Development Mode
- The app runs in debug mode by default
- Auto-reloads on code changes
- Detailed error messages in browser

### Production Deployment
- Set `debug=False` in app.py
- Use proper WSGI server (Gunicorn, uWSGI)
- Configure environment variables
- Serve static files with web server

## 🔧 Troubleshooting

### Common Issues
1. **Port 5000 in use**: Change port in app.py or stop conflicting service
2. **Import errors**: Run `pip install -r requirements.txt`
3. **NLTK data missing**: Run NLTK download commands
4. **Permission errors**: Run as administrator or check file permissions

### Error Messages
- Clear error messages for common issues
- Validation feedback for user input
- Detailed logging for development

## 🎯 Example Use Cases

### Content Analysis
- Social media posts sentiment
- Product review classification
- Customer feedback analysis
- Email tone detection

### Educational
- Learning about NLP and sentiment analysis
- Understanding machine learning basics
- Web development with Flask
- API development concepts

## 🚀 Future Enhancements

### Potential Features
- Multiple language support
- Batch text analysis
- Historical analysis tracking
- Advanced visualization charts
- Custom sentiment models
- Real-time analysis
- Export functionality
- User authentication

### Technical Improvements
- Database integration
- Caching for better performance
- Rate limiting
- Advanced error handling
- Unit test coverage
- CI/CD pipeline

## 📝 Notes

- This is a complete, production-ready web application
- All code is well-commented and documented
- Follows Flask best practices
- Responsive design works on all devices
- Includes comprehensive error handling
- Ready for deployment or further development

## 🎉 Getting Started

1. Choose your preferred startup method above
2. Open the application in your browser
3. Try the example texts or enter your own
4. Explore the API endpoints
5. Read the detailed README.md for more information

Happy analyzing! 🎯
