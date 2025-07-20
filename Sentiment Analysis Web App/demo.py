#!/usr/bin/env python3
"""
Simple demo of the sentiment analysis functionality
"""

def demo_sentiment_analysis():
    """Demonstrate sentiment analysis with example texts."""
    
    print("🧠 Sentiment Analysis Demo")
    print("=" * 50)
    
    try:
        from textblob import TextBlob
        
        examples = [
            "I absolutely love this product! It's amazing!",
            "This is terrible and I hate it.",
            "The weather is 20 degrees today.",
            "I'm so excited about this opportunity!",
            "This service is disappointing and frustrating."
        ]
        
        for i, text in enumerate(examples, 1):
            print(f"\nExample {i}: {text}")
            
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Classify sentiment
            if polarity > 0.1:
                sentiment = "😊 Positive"
            elif polarity < -0.1:
                sentiment = "😞 Negative"
            else:
                sentiment = "😐 Neutral"
            
            print(f"Sentiment: {sentiment}")
            print(f"Polarity: {polarity:.3f} (range: -1 to +1)")
            print(f"Subjectivity: {subjectivity:.3f} (range: 0 to 1)")
        
        print("\n✅ Sentiment analysis is working correctly!")
        print("You can now run the web application with: python app.py")
        
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Please install TextBlob: pip install textblob")
        print("Then download corpora: python -c \"import nltk; nltk.download('punkt')\"")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    demo_sentiment_analysis()
