from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from textblob import TextBlob

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Replace with your YouTube Data API key
YOUTUBE_API_KEY = 'AIzaSyC1eppo6Ze-OCx0dcBS8qHqXhfvX6Pkpyk'

@app.route('/analyze', methods=['POST'])
def analyze_video():
    data = request.json
    video_url = data.get('video_url')

    # Extract video ID from URL
    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400

    # Fetch comments
    comments = fetch_comments(video_id)
    if not comments:
        return jsonify({'error': 'No comments found'}), 400

    # Perform sentiment analysis
    sentiment_results = analyze_sentiments(comments)

    # Summarize results
    summary = summarize_sentiments(sentiment_results)

    return jsonify(summary)

def extract_video_id(url):
    # Extract video ID from YouTube URL
    from urllib.parse import urlparse, parse_qs
    query = urlparse(url).query
    return parse_qs(query).get('v', [None])[0]

def fetch_comments(video_id):
    # Fetch comments using YouTube Data API
    url = f'https://www.googleapis.com/youtube/v3/commentThreads'
    params = {
        'part': 'snippet',
        'videoId': video_id,
        'key': YOUTUBE_API_KEY,
        'maxResults': 100  # Limit to 100 comments for simplicity
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []

    items = response.json().get('items', [])
    comments = [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in items]
    return comments

def analyze_sentiments(comments):
    # Analyze sentiment using TextBlob
    results = []
    for comment in comments:
        blob = TextBlob(comment)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiment = 'positive'
        elif polarity < 0:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        results.append(sentiment)
    return results

def summarize_sentiments(sentiments):
    # Calculate percentages
    total = len(sentiments)
    positive = sentiments.count('positive')
    negative = sentiments.count('negative')
    neutral = sentiments.count('neutral')

    # Determine recommendation
    recommendation = 'Recommended' if positive > negative else 'Not Recommended'

    return {
        'total_comments': total,
        'positive_percentage': round(positive / total * 100, 2),
        'negative_percentage': round(negative / total * 100, 2),
        'neutral_percentage': round(neutral / total * 100, 2),
        'recommendation': recommendation
    }

if __name__ == '__main__':
    app.run(debug=True)