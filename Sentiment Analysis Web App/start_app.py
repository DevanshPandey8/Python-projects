import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("Starting Sentiment Analysis Web Application...")
print("Current directory:", current_dir)

try:
    # Test imports
    from flask import Flask
    from textblob import TextBlob
    print("✅ Required packages imported successfully")
    
    # Test TextBlob
    blob = TextBlob("This is a test.")
    print(f"✅ TextBlob test: {blob.sentiment}")
    
    # Import and run the app
    from app import app
    print("✅ Flask app imported successfully")
    print("\n🚀 Starting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages:")
    print("pip install flask textblob")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
