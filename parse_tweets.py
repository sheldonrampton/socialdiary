import json

def extract_tweets_from_json(file_path):
    # Load the JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Initialize a list to hold tweet information
    tweets_info = []
    
    # Extract the list of tweets
    tweets = data
    
    # Loop through each tweet and extract relevant information
    for tweet in tweets:
        tweet_data = tweet['tweet']
        tweet_id = tweet_data['id_str']  # Tweet ID
        tweet_text = tweet_data['full_text']  # Full text of the tweet
        tweet_date = tweet_data['created_at']  # Date the tweet was created
        
        # Store extracted information in a dictionary
        tweets_info.append({
            'id': tweet_id,
            'text': tweet_text,
            'created_at': tweet_date
        })
    
    return tweets_info

# Specify the path to your JSON file
file_path = 'tweet_sample.js'

# Extract tweets
tweets_info = extract_tweets_from_json(file_path)

# Print extracted information
for tweet in tweets_info:
    print(tweet)
