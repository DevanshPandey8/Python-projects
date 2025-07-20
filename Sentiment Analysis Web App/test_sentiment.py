#!/usr/bin/env python3
"""
Test script for the Sentiment Analysis Web Application
This script tests the sentiment analysis functionality with various examples.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from textblob import TextBlob
    from app import analyze_sentiment
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please make sure you have installed the requirements:")
    print("pip install -r requirements.txt")
    sys.exit(1)

def test_sentiment_analysis():
    """Test the sentiment analysis function with various examples."""
    
    test_cases = [
        # Positive examples
        {
            'text': "I absolutely love this new product! It's amazing and works perfectly.",
            'expected_sentiment': 'Positive'
        },
        {
            'text': "What a beautiful day! I'm feeling great and excited about the future.",
            'expected_sentiment': 'Positive'
        },
        {
            'text': "This is the best thing that has ever happened to me!",
            'expected_sentiment': 'Positive'
        },
        
        # Negative examples
        {
            'text': "This is terrible! I hate how complicated everything is.",
            'expected_sentiment': 'Negative'
        },
        {
            'text': "I'm really disappointed and frustrated with this service.",
            'expected_sentiment': 'Negative'
        },
        {
            'text': "This product is awful and completely useless.",
            'expected_sentiment': 'Negative'
        },
        
        # Neutral examples
        {
            'text': "The meeting is scheduled for tomorrow at 3 PM.",
            'expected_sentiment': 'Neutral'
        },
        {
            'text': "Python is a programming language used for web development.",
            'expected_sentiment': 'Neutral'
        },
        {
            'text': "The weather report shows 20 degrees Celsius.",
            'expected_sentiment': 'Neutral'
        }
    ]
    
    print("=" * 60)
    print("SENTIMENT ANALYSIS TEST RESULTS")
    print("=" * 60)
    
    correct_predictions = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        text = test_case['text']
        expected = test_case['expected_sentiment']
        
        print(f"\nTest {i}:")
        print(f"Text: {text}")
        
        try:
            result = analyze_sentiment(text)
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                continue
                
            actual = result['sentiment']
            polarity = result['polarity']
            subjectivity = result['subjectivity']
            
            is_correct = actual == expected
            if is_correct:
                correct_predictions += 1
                status = "✅ CORRECT"
            else:
                status = "❌ INCORRECT"
            
            print(f"Expected: {expected}")
            print(f"Actual: {actual}")
            print(f"Polarity: {polarity}")
            print(f"Subjectivity: {subjectivity}")
            print(f"Status: {status}")
            
        except Exception as e:
            print(f"❌ Error analyzing text: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"SUMMARY: {correct_predictions}/{total_tests} correct predictions")
    print(f"Accuracy: {(correct_predictions/total_tests)*100:.1f}%")
    print("=" * 60)

def test_edge_cases():
    """Test edge cases and error handling."""
    
    print("\n" + "=" * 60)
    print("EDGE CASES AND ERROR HANDLING TESTS")
    print("=" * 60)
    
    edge_cases = [
        {
            'name': 'Empty string',
            'text': ''
        },
        {
            'name': 'Only spaces',
            'text': '   '
        },
        {
            'name': 'Single character',
            'text': 'a'
        },
        {
            'name': 'Numbers only',
            'text': '12345'
        },
        {
            'name': 'Special characters',
            'text': '!@#$%^&*()'
        },
        {
            'name': 'Very long text',
            'text': 'This is a test sentence. ' * 200  # 5000+ characters
        }
    ]
    
    for case in edge_cases:
        print(f"\nTesting: {case['name']}")
        print(f"Text length: {len(case['text'])} characters")
        
        try:
            result = analyze_sentiment(case['text'])
            
            if 'error' in result:
                print(f"✅ Handled gracefully: {result['error']}")
            else:
                print(f"✅ Analysis successful:")
                print(f"   Sentiment: {result['sentiment']}")
                print(f"   Polarity: {result['polarity']}")
                print(f"   Subjectivity: {result['subjectivity']}")
                
        except Exception as e:
            print(f"❌ Unhandled error: {str(e)}")

def test_textblob_installation():
    """Test if TextBlob is properly installed with required corpora."""
    
    print("\n" + "=" * 60)
    print("TEXTBLOB INSTALLATION TEST")
    print("=" * 60)
    
    try:
        # Test basic TextBlob functionality
        blob = TextBlob("This is a test sentence.")
        sentiment = blob.sentiment
        
        print("✅ TextBlob is working correctly")
        print(f"   Test sentiment: polarity={sentiment.polarity}, subjectivity={sentiment.subjectivity}")
        
        # Test tokenization (requires punkt)
        words = blob.words
        print(f"✅ Tokenization working: {len(words)} words detected")
        
        return True
        
    except Exception as e:
        print(f"❌ TextBlob error: {str(e)}")
        print("   You may need to download NLTK corpora:")
        print("   python -c \"import nltk; nltk.download('punkt'); nltk.download('brown')\"")
        return False

if __name__ == "__main__":
    print("Starting Sentiment Analysis Tests...")
    
    # Test TextBlob installation first
    if not test_textblob_installation():
        print("\n❌ TextBlob is not properly installed. Please fix the installation before running tests.")
        sys.exit(1)
    
    # Run sentiment analysis tests
    test_sentiment_analysis()
    
    # Test edge cases
    test_edge_cases()
    
    print("\n🎉 All tests completed!")
    print("\nTo run the web application:")
    print("   python app.py")
    print("\nThen open: http://localhost:5000")
