import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import json
import random
import string
import math
from datetime import datetime, timezone
import re

# Load API keys from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Global variable for conversation memory
conversation_history = []

def add_to_history(user_msg, bot_reply):
    conversation_history.append({"user": user_msg, "bot": bot_reply})

# === EXISTING FEATURES ===
def get_bitcoin_price():
    """Get current Bitcoin price"""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return f"💰 Current Bitcoin price: ${data['bitcoin']['usd']:,}"
        else:
            return "❌ Couldn't fetch Bitcoin price: API unavailable."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_weather(city="Lucknow"):
    """Get current weather information for a city"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            desc = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            pressure = data['main']['pressure']
            visibility = data.get('visibility', 0) / 1000  # Convert to km
            
            # Calculate rain chance based on humidity and weather conditions
            rain_chance = calculate_rain_chance(humidity, desc, data['weather'][0]['main'])
            
            result = f"🌤️ Current Weather in {city}:\n"
            result += f"🌡️ Temperature: {temp}°C (feels like {feels_like}°C)\n"
            result += f"🌥️ Condition: {desc.title()}\n"
            result += f"💧 Humidity: {humidity}%\n"
            result += f"💨 Wind Speed: {wind_speed} m/s\n"
            result += f"🏔️ Pressure: {pressure} hPa\n"
            result += f"👁️ Visibility: {visibility:.1f} km\n"
            result += f"🌧️ Rain Chance: {rain_chance}%"
            
            return result
        else:
            return f"❌ Can't fetch weather data for {city}. Please check the city name."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_weather_forecast(city="Lucknow"):
    """Get 5-day weather forecast for a city"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            result = f"📅 5-Day Weather Forecast for {city}:\n\n"
            
            # Group forecasts by day
            daily_forecasts = {}
            for forecast in data['list']:
                date = datetime.fromtimestamp(forecast['dt']).strftime('%Y-%m-%d')
                time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')
                
                if date not in daily_forecasts:
                    daily_forecasts[date] = []
                daily_forecasts[date].append({
                    'time': time,
                    'temp': forecast['main']['temp'],
                    'desc': forecast['weather'][0]['description'],
                    'humidity': forecast['main']['humidity'],
                    'rain_prob': forecast.get('pop', 0) * 100  # Probability of precipitation
                })
            
            # Show next 5 days
            for i, (date, forecasts) in enumerate(list(daily_forecasts.items())[:5]):
                day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
                result += f"🗓️ {day_name} ({date}):\n"
                
                # Get day and night forecasts
                day_forecast = min(forecasts, key=lambda x: abs(int(x['time'].split(':')[0]) - 14))  # Closest to 2 PM
                night_forecast = min(forecasts, key=lambda x: abs(int(x['time'].split(':')[0]) - 20))  # Closest to 8 PM
                
                result += f"  ☀️ Day: {day_forecast['temp']:.1f}°C - {day_forecast['desc'].title()}\n"
                result += f"  🌙 Night: {night_forecast['temp']:.1f}°C - {night_forecast['desc'].title()}\n"
                result += f"  🌧️ Rain Chance: {max(f['rain_prob'] for f in forecasts):.0f}%\n"
                result += f"  💧 Humidity: {sum(f['humidity'] for f in forecasts) // len(forecasts)}%\n\n"
            
            return result.strip()
        else:
            return f"❌ Can't fetch weather forecast for {city}. Please check the city name."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def calculate_rain_chance(humidity, description, weather_main):
    """Calculate rain chance based on weather conditions"""
    base_chance = 0
    
    # Base chance from humidity
    if humidity > 80:
        base_chance = 70
    elif humidity > 60:
        base_chance = 40
    elif humidity > 40:
        base_chance = 20
    else:
        base_chance = 5
    
    # Adjust based on weather conditions
    rain_keywords = ['rain', 'drizzle', 'shower', 'thunderstorm']
    cloud_keywords = ['cloud', 'overcast', 'mist', 'fog']
    
    if any(keyword in description.lower() for keyword in rain_keywords):
        base_chance = min(95, base_chance + 50)
    elif any(keyword in description.lower() for keyword in cloud_keywords):
        base_chance = min(80, base_chance + 20)
    elif 'clear' in description.lower():
        base_chance = max(5, base_chance - 20)
    
    # Weather main adjustments
    if weather_main.lower() in ['rain', 'drizzle', 'thunderstorm']:
        base_chance = min(95, base_chance + 30)
    elif weather_main.lower() in ['clouds']:
        base_chance = min(70, base_chance + 15)
    elif weather_main.lower() == 'clear':
        base_chance = max(5, base_chance - 15)
    
    return min(95, max(5, base_chance))

def get_rain_prediction(city="Lucknow"):
    """Get specific rain prediction for a city"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            result = f"🌧️ Rain Prediction for {city}:\n\n"
            
            rain_forecasts = []
            for forecast in data['list'][:8]:  # Next 24 hours (8 x 3-hour intervals)
                time = datetime.fromtimestamp(forecast['dt']).strftime('%m-%d %H:%M')
                rain_prob = forecast.get('pop', 0) * 100
                desc = forecast['weather'][0]['description']
                
                if rain_prob > 20:  # Only show significant rain chances
                    rain_forecasts.append({
                        'time': time,
                        'prob': rain_prob,
                        'desc': desc
                    })
            
            if rain_forecasts:
                result += "⚠️ Expected rain periods:\n"
                for rf in rain_forecasts:
                    result += f"  • {rf['time']}: {rf['prob']:.0f}% chance - {rf['desc'].title()}\n"
            else:
                result += "☀️ No significant rain expected in the next 24 hours!\n"
            
            # Overall rain summary
            avg_rain_chance = sum(forecast.get('pop', 0) for forecast in data['list'][:8]) / 8 * 100
            result += f"\n📊 Average rain chance (next 24h): {avg_rain_chance:.0f}%"
            
            return result
        else:
            return f"❌ Can't fetch rain prediction for {city}. Please check the city name."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# === NEW FEATURES ===

def get_stock_price(symbol):
    """Get stock price using Alpha Vantage free API (demo data)"""
    # Using a free API endpoint for demonstration
    try:
        # For demo, we'll simulate stock data
        demo_stocks = {
            "AAPL": {"price": 150.25, "change": "+2.30"},
            "GOOGL": {"price": 2750.80, "change": "-15.20"},
            "TSLA": {"price": 245.67, "change": "+5.45"},
            "MSFT": {"price": 310.45, "change": "+1.80"},
            "AMZN": {"price": 3250.90, "change": "-8.30"}
        }
        
        symbol_upper = symbol.upper()
        if symbol_upper in demo_stocks:
            stock = demo_stocks[symbol_upper]
            return f"📈 {symbol_upper} Stock Price: ${stock['price']} ({stock['change']})"
        else:
            return f"❌ Stock symbol '{symbol}' not found in demo data. Try: AAPL, GOOGL, TSLA, MSFT, AMZN"
    except Exception as e:
        return f"❌ Error fetching stock data: {str(e)}"

def get_crypto_prices():
    """Get multiple cryptocurrency prices"""
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,cardano,solana,dogecoin,litecoin,polygon&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            result = "💰 Cryptocurrency Prices:\n"
            crypto_names = {
                "bitcoin": "Bitcoin (BTC)",
                "ethereum": "Ethereum (ETH)", 
                "cardano": "Cardano (ADA)",
                "solana": "Solana (SOL)",
                "dogecoin": "Dogecoin (DOGE)",
                "litecoin": "Litecoin (LTC)",
                "polygon": "Polygon (MATIC)"
            }
            for crypto_id, price_data in data.items():
                name = crypto_names.get(crypto_id, crypto_id.title())
                result += f"• {name}: ${price_data['usd']:,}\n"
            return result.strip()
        else:
            return "❌ Couldn't fetch cryptocurrency prices."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_news_headlines():
    """Get latest news headlines (demo data)"""
    # Demo news headlines - in real implementation, use NewsAPI
    demo_news = [
        "🌍 Global climate summit reaches breakthrough agreement",
        "💻 Tech giants announce new AI collaboration initiative", 
        "🏥 Major medical breakthrough in cancer research announced",
        "🚀 Space mission successfully launches to Mars",
        "📱 New smartphone technology revolutionizes mobile industry"
    ]
    
    result = "📰 Latest News Headlines:\n"
    for i, headline in enumerate(demo_news[:3], 1):
        result += f"{i}. {headline}\n"
    return result.strip()

def convert_units(value, from_unit, to_unit):
    """Convert between different units"""
    conversions = {
        # Length
        ("km", "miles"): lambda x: x * 0.621371,
        ("miles", "km"): lambda x: x * 1.60934,
        ("m", "ft"): lambda x: x * 3.28084,
        ("ft", "m"): lambda x: x * 0.3048,
        ("cm", "inches"): lambda x: x * 0.393701,
        ("inches", "cm"): lambda x: x * 2.54,
        
        # Temperature
        ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
        ("celsius", "kelvin"): lambda x: x + 273.15,
        ("kelvin", "celsius"): lambda x: x - 273.15,
        
        # Weight
        ("kg", "lbs"): lambda x: x * 2.20462,
        ("lbs", "kg"): lambda x: x * 0.453592,
        ("g", "oz"): lambda x: x * 0.035274,
        ("oz", "g"): lambda x: x * 28.3495,
        
        # Volume
        ("gallons", "liters"): lambda x: x * 3.78541,
        ("liters", "gallons"): lambda x: x * 0.264172,
        ("cups", "ml"): lambda x: x * 236.588,
        ("ml", "cups"): lambda x: x * 0.00422675,
        ("fl_oz", "ml"): lambda x: x * 29.5735,
        ("ml", "fl_oz"): lambda x: x * 0.033814,
        
        # Area
        ("acres", "hectares"): lambda x: x * 0.404686,
        ("hectares", "acres"): lambda x: x * 2.47105,
        ("sqft", "sqm"): lambda x: x * 0.092903,
        ("sqm", "sqft"): lambda x: x * 10.7639,
        
        # Speed
        ("mph", "kmh"): lambda x: x * 1.60934,
        ("kmh", "mph"): lambda x: x * 0.621371,
    }
    
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        result = conversions[key](value)
        return f"🔄 {value} {from_unit} = {result:.2f} {to_unit}"
    else:
        return f"🔧 Unit conversion from {from_unit} to {to_unit} will be added in future updates! Currently supported: km/miles, °C/°F, kg/lbs, gallons/liters, acres/hectares, mph/kmh, and more."

def generate_password(length=12):
    """Generate a secure password"""
    if length < 4:
        length = 4
    if length > 50:
        length = 50
        
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    return f"🔐 Generated password: {password}\n💡 Tip: Store this securely!"

def calculate_math(expression):
    """Safe mathematical calculation with advanced functions"""
    try:
        # Remove spaces and validate expression
        expression = expression.replace(" ", "")
        
        # Handle special functions
        if "sqrt(" in expression.lower():
            # Extract number from sqrt(x)
            match = re.search(r'sqrt\((\d+(?:\.\d+)?)\)', expression.lower())
            if match:
                number = float(match.group(1))
                result = math.sqrt(number)
                return f"🧮 √{number} = {result}"
        
        if "^" in expression:
            # Handle power operations (x^y -> x**y)
            expression = expression.replace("^", "**")
        
        # Allow only numbers, operators, and parentheses
        if re.match(r'^[0-9+\-**/().]+$', expression):
            result = eval(expression)
            return f"🧮 {expression} = {result}"
        else:
            return "🔧 Advanced math functions (trigonometry, logarithms, calculus) will be added in future updates! Currently supports: +, -, *, /, (), sqrt(), and ^ for powers."
    except Exception as e:
        return f"❌ Error in calculation: {str(e)}"

def get_time_info(timezone_name=None):
    """Get current time and date information"""
    try:
        current_time = datetime.now()
        if timezone_name:
            return f"🌍 Timezone conversions will be added in future updates!\n⏰ Current local time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}\n📅 Day: {current_time.strftime('%A')}"
        else:
            return f"⏰ Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}\n📅 Day: {current_time.strftime('%A')}\n🗓️ Date: {current_time.strftime('%B %d, %Y')}"
    except Exception as e:
        return f"❌ Error getting time: {str(e)}"

def get_random_joke():
    """Get a random joke"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything! 😄",
        "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
        "Why don't eggs tell jokes? They'd crack each other up! 🥚",
        "What do you call a fake noodle? An impasta! 🍝",
        "Why did the math book look so sad? Because it had too many problems! 📚",
        "What do you call a bear with no teeth? A gummy bear! 🐻",
        "Why don't skeletons fight each other? They don't have the guts! 💀",
    ]
    return f"😂 Here's a joke for you:\n{random.choice(jokes)}"

def get_motivation_quote():
    """Get a motivational quote"""
    quotes = [
        "💪 'The only way to do great work is to love what you do.' - Steve Jobs",
        "🌟 'Innovation distinguishes between a leader and a follower.' - Steve Jobs", 
        "🚀 'The future belongs to those who believe in the beauty of their dreams.' - Eleanor Roosevelt",
        "⭐ 'It is during our darkest moments that we must focus to see the light.' - Aristotle",
        "🔥 'Success is not final, failure is not fatal: it is the courage to continue that counts.' - Winston Churchill",
        "💎 'The only impossible journey is the one you never begin.' - Tony Robbins",
    ]
    return f"✨ Daily Motivation:\n{random.choice(quotes)}"

def handle_future_feature(feature_type, user_input):
    """Handle requests for features that will be added in future updates"""
    feature_messages = {
        "translation": "🌍 Translation feature will be integrated in later upgrades! Soon you'll be able to translate between 100+ languages.",
        "timezone": "🌍 Timezone conversions will be added in future updates! You'll be able to check time in any city worldwide.",
        "reminders": "⏰ Scheduling and reminder system will be integrated in later upgrades! You'll be able to set reminders and manage your calendar.",
        "advanced_crypto": "💰 More cryptocurrencies will be added in future updates! We're expanding beyond the current 7 supported coins.",
        "advanced_stocks": "📈 Real-time stock API and more symbols will be integrated in later upgrades! Currently showing demo data for 5 major stocks.",
        "file_operations": "📁 File management features will be added in future updates! You'll be able to create, read, and organize files.",
        "email": "📧 Email integration will be added in later upgrades! You'll be able to compose and send emails directly.",
        "social_media": "📱 Social media integration will be added in future updates! Check trends, post updates, and more.",
        "advanced_math": "🧮 Advanced mathematical functions (trigonometry, calculus, statistics) will be integrated in later upgrades!",
        "weather_forecast": "🌤️ Weather forecasting is now available! Try asking for 'weather forecast [city]' or 'will it rain in [city]'.",
        "currency_exchange": "💱 Currency exchange rates will be integrated in later upgrades! Convert between USD, EUR, INR, and more.",
        "entertainment": "🎬 Entertainment database (movies, music, books) will be added in future updates!",
        "geography": "🌍 Geographical data (population, capitals, facts) will be integrated in later upgrades!",
        "qr_code": "📱 QR code generation will be added in future updates!",
        "web_status": "🌐 Website status checking will be integrated in later upgrades!"
    }
    
    return feature_messages.get(feature_type, 
        "🚀 This feature will be integrated in later upgrades! We're constantly expanding the AI assistant's capabilities.")

def detect_future_feature_request(user_input):
    """Detect if user is asking for a feature that will be added later"""
    user_input_lower = user_input.lower()
    
    # Translation requests
    if any(word in user_input_lower for word in ["translate", "translation", "spanish", "french", "german", "hindi"]):
        return "translation"
    
    # Timezone requests
    if any(phrase in user_input_lower for phrase in ["time in tokyo", "time in london", "time in new york", "timezone"]):
        return "timezone"
    
    # Reminder/scheduling requests
    if any(word in user_input_lower for word in ["reminder", "remind me", "schedule", "calendar", "alarm"]):
        return "reminders"
    
    # Advanced crypto requests (specific coins not supported)
    if any(word in user_input_lower for word in ["shiba", "xrp", "ripple", "chainlink", "avalanche"]):
        return "advanced_crypto"
    
    # Email requests
    if any(word in user_input_lower for word in ["email", "send mail", "compose email"]):
        return "email"
    
    # File operation requests
    if any(phrase in user_input_lower for phrase in ["create file", "read file", "delete file", "file management"]):
        return "file_operations"
    
    # Currency exchange requests
    if any(phrase in user_input_lower for phrase in ["usd to eur", "currency exchange", "exchange rate", "dollar to euro"]):
        return "currency_exchange"
    
    # Entertainment requests
    if any(phrase in user_input_lower for phrase in ["oscar winner", "movie", "netflix", "music", "song"]):
        return "entertainment"
    
    # Geography requests - Remove capital questions since AI can handle them
    if any(phrase in user_input_lower for phrase in ["population of", "demographics"]):
        return "geography"
    
    # QR code requests
    if any(phrase in user_input_lower for phrase in ["qr code", "generate qr", "create qr"]):
        return "qr_code"
    
    # Website status requests
    if any(phrase in user_input_lower for phrase in ["is google down", "website status", "server down"]):
        return "web_status"
    
    return None

# === SMART INPUT PROCESSING ===

def extract_city_from_input(user_input):
    """Extract city name from user input with various patterns"""
    user_input_lower = user_input.lower()
    
    if " in " in user_input_lower:
        parts = user_input_lower.split(" in ", 1)
        if len(parts) > 1:
            city = parts[1].strip()
            city = city.replace(" weather", "").replace(" today", "").replace(" now", "")
            return city.title()
    
    if " for " in user_input_lower:
        parts = user_input_lower.split(" for ", 1)
        if len(parts) > 1:
            city = parts[1].strip()
            city = city.replace(" weather", "").replace(" today", "").replace(" now", "")
            return city.title()
    
    if user_input_lower.endswith(" weather"):
        city = user_input_lower.replace(" weather", "").strip()
        if len(city) > 0 and city not in ["what's the", "how's the"]:
            return city.title()
    
    return "Lucknow"

def extract_stock_symbol(user_input):
    """Extract stock symbol from user input"""
    user_input_upper = user_input.upper()
    # Look for common patterns
    symbols = ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN", "APPLE", "GOOGLE", "TESLA", "MICROSOFT", "AMAZON"]
    for symbol in symbols:
        if symbol in user_input_upper:
            # Map company names to symbols
            symbol_map = {"APPLE": "AAPL", "GOOGLE": "GOOGL", "TESLA": "TSLA", "MICROSOFT": "MSFT", "AMAZON": "AMZN"}
            return symbol_map.get(symbol, symbol)
    return "AAPL"  # default

def extract_conversion_params(user_input):
    """Extract conversion parameters from user input"""
    user_input_lower = user_input.lower()
    
    # Pattern: "convert X unit1 to unit2"
    convert_pattern = r"convert\s+(\d+(?:\.\d+)?)\s+(\w+)\s+to\s+(\w+)"
    match = re.search(convert_pattern, user_input_lower)
    if match:
        value, from_unit, to_unit = match.groups()
        return float(value), from_unit, to_unit
    
    # Pattern: "X unit1 to unit2"
    direct_pattern = r"(\d+(?:\.\d+)?)\s+(\w+)\s+to\s+(\w+)"
    match = re.search(direct_pattern, user_input_lower)
    if match:
        value, from_unit, to_unit = match.groups()
        return float(value), from_unit, to_unit
    
    return None, None, None

def extract_math_expression(user_input):
    """Extract mathematical expression from user input"""
    # Look for calculate/math keywords followed by expression
    patterns = [
        r"calculate\s+(.+)",
        r"math\s+(.+)",
        r"solve\s+(.+)",
        r"compute\s+(.+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, user_input.lower())
        if match:
            return match.group(1).strip()
    
    # Handle "what is" only for mathematical expressions
    if user_input.lower().startswith("what is"):
        # Extract the part after "what is"
        expression = user_input[7:].strip()
        # Check if it looks like a math expression (contains numbers and operators)
        if re.match(r'^[0-9+\-*/().\s]+$', expression):
            return expression
    
    # If input looks like a math expression directly
    if re.match(r'^[0-9+\-*/().\s]+$', user_input.strip()):
        return user_input.strip()
    
    return None

def generate_gemini_reply(user_input):
    """Generate reply using Gemini AI"""
    try:
        prompt = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in conversation_history])
        prompt += f"\nUser: {user_input}\nBot:"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🤖 I'm having trouble connecting to my AI brain right now. Error: {str(e)}"

def process_user_input(user_input):
    """Main function to process user input and determine response"""
    user_input_lower = user_input.lower()
    
    # Handle greetings - improved to match whole words only
    greeting_words = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings", "howdy"]
    words_in_input = user_input_lower.split()
    if any(word in words_in_input for word in greeting_words):
        return get_user_greeting_response()
    
    # Handle "how are you" type questions
    if any(phrase in user_input_lower for phrase in ["how are you", "how's it going", "how are things", "what's up"]):
        return "😊 I'm doing great, thank you for asking! I'm here and ready to help you with anything you need. How can I assist you today?"
    
    # Handle "thank you" responses
    if any(word in user_input_lower for word in ["thank you", "thanks", "thank"]):
        return "🙏 You're very welcome! I'm happy to help! Is there anything else you'd like me to assist you with?"
    
    # Handle "good" or "nice" responses
    if any(word in user_input_lower for word in ["good", "nice", "great", "awesome", "cool", "excellent"]) and len(user_input.split()) <= 3:
        return "😊 Glad to hear that! What else can I help you with today?"
    
    # Bitcoin price
    if any(word in user_input_lower for word in ["bitcoin", "btc"]) and "price" in user_input_lower:
        return get_bitcoin_price()
    
    # Multiple crypto prices
    if any(word in user_input_lower for word in ["crypto", "cryptocurrency"]) and "price" in user_input_lower:
        return get_crypto_prices()
    
    # Stock prices
    if any(word in user_input_lower for word in ["stock", "share"]) and "price" in user_input_lower:
        symbol = extract_stock_symbol(user_input)
        return get_stock_price(symbol)
    
    # Weather - Enhanced with forecasts and rain predictions
    if "weather" in user_input_lower:
        city = extract_city_from_input(user_input)
        
        # Check for forecast requests
        if any(word in user_input_lower for word in ["forecast", "tomorrow", "next", "future", "week", "days"]):
            return get_weather_forecast(city)
        # Check for rain-specific requests
        elif any(word in user_input_lower for word in ["rain", "precipitation", "shower", "drizzle"]):
            return get_rain_prediction(city)
        else:
            return get_weather(city)
    
    # Rain prediction requests
    if any(phrase in user_input_lower for phrase in ["will it rain", "rain today", "rain tomorrow", "chance of rain", "rain prediction"]):
        city = extract_city_from_input(user_input)
        return get_rain_prediction(city)
    
    # Weather forecast requests
    if any(phrase in user_input_lower for phrase in ["weather forecast", "forecast", "weather tomorrow", "weather next week"]):
        city = extract_city_from_input(user_input)
        return get_weather_forecast(city)
    
    # News
    if any(word in user_input_lower for word in ["news", "headlines", "latest news"]):
        return get_news_headlines()
    
    # Unit conversion
    if any(word in user_input_lower for word in ["convert", "conversion"]) or " to " in user_input_lower:
        value, from_unit, to_unit = extract_conversion_params(user_input)
        if value is not None:
            return convert_units(value, from_unit, to_unit)
    
    # Password generation
    if any(word in user_input_lower for word in ["password", "generate password"]):
        # Extract length if specified
        length_match = re.search(r"(\d+)", user_input)
        length = int(length_match.group(1)) if length_match else 12
        return generate_password(length)
    
    # Mathematical calculations
    math_expr = extract_math_expression(user_input)
    if math_expr:
        return calculate_math(math_expr)
    
    # Time and date
    if any(word in user_input_lower for word in ["time", "date", "what time", "current time"]):
        return get_time_info()
    
    # Jokes
    if any(word in user_input_lower for word in ["joke", "funny", "make me laugh"]):
        return get_random_joke()
    
    # Motivation
    if any(word in user_input_lower for word in ["motivation", "motivate", "inspire", "quote"]):
        return get_motivation_quote()
    
    # Help command
    if user_input_lower in ["help", "what can you do", "features", "commands"]:
        return get_help_message()
    
    # Check for future feature requests
    future_feature = detect_future_feature_request(user_input)
    if future_feature:
        return handle_future_feature(future_feature, user_input)
    
    # If it's a short unclear input, give a helpful response
    if len(user_input.split()) <= 2 and not any(char.isdigit() for char in user_input):
        return get_confused_response()
    
    # Default to Gemini AI for complex queries
    return generate_gemini_reply(user_input)

def get_help_message():
    """Display help message with available features"""
    return """🤖 Aiden - Your AI Assistant Features:

💬 **Chat & Greetings:**
• "Hello", "Hi", "Hey" - I'll greet you back!
• "How are you?" - I'll let you know how I'm doing
• "Thank you" - I appreciate your gratitude!

💰 **Financial:**
• "Bitcoin price" - Get current BTC price
• "Crypto prices" - 7 major cryptocurrency prices  
• "Apple stock price" or "AAPL stock" - Stock prices (demo data)

🌤️ **Weather & Forecasts:**
• "Weather in Delhi" - Current weather with rain chances
• "Weather forecast Mumbai" - 5-day weather forecast
• "Will it rain in London" - Rain prediction for next 24 hours
• "Rain chances Tokyo" - Detailed rain probability analysis

🔧 **Tools:**
• "Convert 100 km to miles" - Unit conversions (length, weight, temp, volume, area, speed)
• "Generate password" - Secure password (specify length: "Generate 16 password")
• "Calculate 15 * 25" or "sqrt(144)" - Math calculations with basic functions

📰 **Information:**
• "Latest news" - Current headlines (demo data)
• "Time" or "Current time" - Date and time info

🎯 **Fun:**
• "Tell me a joke" - Random jokes
• "Motivate me" - Inspirational quotes

💬 **General:** Ask me anything else and I'll use my AI to help!

🚀 **Coming Soon:** Translation, timezone conversions, reminders, more crypto/stocks, 
   advanced math, email integration, and much more in future upgrades!

Type 'exit' to quit the chat."""

def display_welcome_message():
    """Display a friendly welcome message"""
    print("=" * 60)
    print("🎉 WELCOME TO AIDEN - YOUR AI ASSISTANT! 🎉")
    print("=" * 60)
    print("👋 Hello there! I'm Aiden, your friendly AI assistant, powered by Google Gemini.")
    print("🌟 I'm here to help you with various tasks and answer your questions!")
    print()
    print("🔥 What can I do for you today?")
    print("• 💬 Have a conversation with me")
    print("• 🌤️ Get current weather with rain chances")
    print("• 📅 Get 5-day weather forecasts")
    print("• 🌧️ Check rain predictions")
    print("• 💰 Check Bitcoin prices")
    print("• 📈 Get stock prices (demo)")
    print("• 🧮 Solve math problems")
    print("• 🔐 Generate secure passwords")
    print("• 📰 Get latest news")
    print("• 😂 Tell you jokes")
    print("• 💪 Share motivational quotes")
    print("• ⏰ Show current time and date")
    print("• ❓ Answer any questions you have")
    print()
    print("✨ Just type what you want, and I'll help you out!")
    print("💡 Try saying: 'Hello', 'Weather forecast Delhi', 'Will it rain?', 'Tell me a joke'")
    print("🚪 Type 'exit' when you're done chatting")
    print("-" * 60)

def get_user_greeting_response():
    """Return a friendly greeting response"""
    greetings = [
        "👋 Hello! I'm Aiden, great to meet you! How can I assist you today?",
        "🌟 Hi there! I'm Aiden, excited to help you! What would you like to do?",
        "😊 Hey! Welcome! I'm Aiden, here to make your day easier. What can I help with?",
        "🎉 Greetings! I'm Aiden, your AI assistant, ready to help! What's on your mind?",
        "✨ Hello! I'm Aiden, here and ready to assist you with anything you need!",
        "🚀 Hi! I'm Aiden, let's get started! What would you like to explore today?",
    ]
    return random.choice(greetings)

def get_confused_response():
    """Return a helpful response when user input is unclear"""
    responses = [
        "🤔 I'm not quite sure what you mean. Could you please rephrase that?",
        "💭 Hmm, I didn't catch that. Could you try asking in a different way?",
        "🔍 I want to help, but I need a bit more clarity. Can you be more specific?",
        "😅 I'm a bit confused. Could you give me more details about what you need?",
        "🤖 I'm still learning! Could you try explaining that differently?",
        "💡 I'm here to help! Try typing 'help' to see what I can do, or just ask me anything!",
    ]
    return random.choice(responses)

def chat():
    """Main chat function with enhanced user interaction"""
    display_welcome_message()
    
    # Ask user what they want to do
    print("🎯 What would you like to do first?")
    print("(You can type anything or say 'help' for a full list of features)")
    print()
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                print("🤖 Bot: 😊 I'm here when you're ready! Just type something and I'll help you.")
                continue
                
            if user_input.lower() == "exit":
                print("\n🎉 Thank you for chatting with me today!")
                print("👋 Goodbye! I hope I was helpful. See you next time!")
                break
            
            reply = process_user_input(user_input)
            print(f"🤖 Aiden: {reply}")
            add_to_history(user_input, reply)
            
        except KeyboardInterrupt:
            print("\n\n🎉 Thank you for using Aiden!")
            print("👋 Goodbye! Have a wonderful day!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")
            print("🔧 Don't worry, I'm still here to help! Please try again.")

if __name__ == "__main__":
    chat()
