# 🤖 Enhanced AI Chatbot - Complete Assistant

A powerful Python chatbot application with modern GUI, powered by Google Gemini AI 2.0 Flash model, offering comprehensive features for weather, cryptocurrency, calculations, and intelligent conversations.

## 🌟 Key Features

### 🧠 **AI Capabilities**
- **Google Gemini 2.0 Flash** - Latest and most powerful AI model
- **Natural Language Processing** - Understands context and nuance
- **General Knowledge** - Answers questions on any topic
- **Creative Writing** - Poems, stories, explanations
- **Code Help** - Programming assistance and explanations

### 🌤️ **Weather & Forecasts**
- **Current Weather** - Real-time weather for any city
- **5-Day Forecasts** - Extended weather predictions
- **Rain Predictions** - Detailed precipitation forecasts
- **Weather Alerts** - Comprehensive weather information

### 💰 **Financial Data**
- **Cryptocurrency Prices** - Bitcoin, Ethereum, and more
- **Live Market Data** - Real-time price updates
- **Stock Information** - Demo stock prices for major companies

### 🧮 **Mathematical Operations**
- **Basic Calculations** - Addition, subtraction, multiplication, division
- **Advanced Math** - Square roots, powers, complex expressions
- **Safe Expression Evaluation** - Secure mathematical processing

### 🎨 **Modern Interface**
- **Dark Theme** - Professional, eye-friendly design
- **Responsive GUI** - Smooth animations and interactions
- **Auto-scroll** - Automatically follows conversation
- **Input Indicators** - Real-time feedback and character counting

## 🚀 Quick Start

### Method 1: One-Click Launch (Recommended)
```batch
run_chatbot.bat
```

### Method 2: Manual Launch
```bash
python chatbot.py
```

### Method 3: Desktop Shortcut
1. Run `create_desktop_shortcut.bat`
2. Double-click the desktop icon

## 📋 Requirements

- **Python 3.7+**
- **Internet Connection** (for AI and API features)
- **Required Packages:**
  - `google-generativeai` - Google Gemini AI integration
  - `requests` - HTTP requests for APIs
  - `python-dotenv` - Environment variable management
  - `tkinter` - GUI framework (usually included with Python)

## 🔧 Setup & Configuration

### 1. API Keys Setup
Create a `.env` file with your API keys:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

### 2. Get Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a free account
3. Generate an API key
4. Add it to your `.env` file

### 3. Get OpenWeatherMap API Key
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file

## 🎯 How to Use

### Chat Examples:

#### 🌟 **Greetings**
- "Hello" / "Hi" / "Good morning"
- "How are you?" / "What's up?"

#### 🌤️ **Weather Queries**
- "Weather in New York"
- "What's the weather like in London?"
- "Weather forecast for Tokyo"
- "Will it rain tomorrow in Mumbai?"

#### 💰 **Cryptocurrency**
- "Bitcoin price"
- "Ethereum price"
- "Current crypto prices"

#### 🧮 **Math Problems**
- "What is 15 * 25?"
- "Calculate 100 / 5"
- "Square root of 144"
- "What is 2^10?"

#### 🧠 **AI Questions**
- "What is the capital of France?"
- "Explain artificial intelligence"
- "Write a poem about coding"
- "How does machine learning work?"

#### 🎨 **Creative Requests**
- "Write a short story about robots"
- "Create a haiku about nature"
- "Explain quantum physics simply"

## 🏗️ Project Architecture

```
Enhanced AI Chatbot/
├── chatbot.py              # Main GUI application
├── ai_assistant.py         # Core AI logic and API integrations
├── .env                    # API keys (keep private!)
├── requirements.txt        # Python dependencies
├── run_chatbot.bat         # Windows launcher
├── create_desktop_shortcut.bat  # Desktop shortcut creator
├── fix_readonly.bat        # File permission utility
└── README.md              # This documentation
```

## � Technical Details

### AI Model
- **Google Gemini 2.0 Flash** - Latest multimodal AI model
- **Context Awareness** - Maintains conversation history
- **Fallback Handling** - Graceful error management

### APIs Used
- **Google Gemini API** - AI conversations and knowledge
- **OpenWeatherMap API** - Weather data and forecasts
- **CoinGecko API** - Cryptocurrency prices

### Security Features
- **Environment Variables** - API keys stored securely
- **Input Validation** - Safe expression evaluation
- **Error Handling** - Robust error management

## 🛠️ Troubleshooting

### Common Issues:

#### "API key expired" or "400 Error"
- Check your `.env` file for correct API keys
- Verify API keys are active and have quota remaining

#### "Input field not working"
- The application has been optimized for proper input handling
- Try restarting the application

#### "Module not found"
- Install dependencies: `pip install -r requirements.txt`
- Ensure Python is properly installed

#### "Permission denied"
- Run `fix_readonly.bat` to fix file permissions
- Ensure you have write permissions in the folder

### Performance Tips:
- Keep the application updated
- Ensure stable internet connection
- Close and restart if responses become slow

## 🎨 Features in Detail

### Greeting System
- Intelligent greeting detection
- Contextual responses
- Friendly conversation starters

### Weather System
- Real-time weather data
- 5-day forecasts
- Rain predictions
- Multiple city support
- Detailed meteorological information

### Math Engine
- Safe expression evaluation
- Support for basic and advanced operations
- Error handling for invalid expressions

### Cryptocurrency Tracker
- Real-time price data
- Multiple cryptocurrency support
- Market information

### AI Conversation
- Context-aware responses
- Creative writing capabilities
- Educational explanations
- Code assistance

## 📈 Recent Updates

### v2.0 - Major Enhancement
✅ **Fixed Greeting Detection** - Improved word matching  
✅ **Fixed Math Calculations** - Resolved scope issues  
✅ **Updated AI Model** - Gemini 2.0 Flash integration  
✅ **Enhanced Geography** - AI can answer location questions  
✅ **GUI Improvements** - Better input handling  
✅ **Bug Fixes** - All major issues resolved  

## 🎯 Tips for Best Experience

1. **Use Natural Language** - Speak to the AI like you would to a human
2. **Be Specific** - More detailed questions get better answers
3. **Try Different Phrasings** - If one approach doesn't work, try another
4. **Explore Features** - Try different types of queries to discover capabilities
5. **Keep It Updated** - Regularly update API keys and dependencies

## 🚀 Ready to Chat!

Your AI assistant is fully functional and ready to help with:
- ✅ Intelligent conversations
- ✅ Real-time weather data
- ✅ Mathematical calculations
- ✅ Cryptocurrency prices
- ✅ General knowledge questions
- ✅ Creative writing
- ✅ Code assistance

**Launch your chatbot now and start exploring its amazing capabilities!**

---

*Built with Python, Google Gemini AI, and modern GUI technologies. Designed for both casual users and developers.*
