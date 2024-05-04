import json
import requests
from bs4 import BeautifulSoup
import csv
from requests.exceptions import Timeout
import datetime
import re

def extract_tweets_from_json(file_path):
    # Load the JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    start_idx = content.find('[')  # Assuming the JSON data starts with '['
    if start_idx == -1:
        return "No JSON data found."

    # Extract the JSON string
    json_str = content[start_idx:]

    # Convert the JSON string to a Python dictionary
    tweets = json.loads(json_str)

    # Initialize a list to hold tweet information
    tweets_info = []
    
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


def get_webpage_title(url):
    max_retries = 2  # Maximum number of retries
    backoff_factor = 1  # Time in seconds to wait between retries
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    error = ''
    for attempt in range(max_retries):
        try:
            # Sending a HTTP request to the URL
            response = requests.get(url, headers=headers, timeout=10)
            # Raise an exception if the request was unsuccessful
            response.raise_for_status()

            # Parsing the HTML content of the webpage
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extracting the title tag
            title_tag = soup.find('title')

            # Returning the text part of the title tag
            return [title_tag.text.strip(), ''] if title_tag else ['', '']
        except Timeout:
            print("The request timed out")
        except requests.RequestException as e:
            error = e
            print(f"Error accessing the URL: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
            error = e
    return ['', error]


def remove_twitter_handles_improved(text):
    # Extend the pattern to optionally include surrounding whitespace or a colon (commonly following handles)
    pattern = r'\s?@\w+\b:?'
    
    clean_text = re.sub(pattern, '', text)
    return clean_text.strip()


def find_and_remove_urls(text):
    # Regular expression pattern to match URLs
    url_pattern = r'https?://\S+|www\.\S+'
    
    # Find all occurrences of the pattern
    urls = re.findall(url_pattern, text)
    
    # Replace all occurrences of URLs with an empty string
    text_without_urls = re.sub(url_pattern, '', text)
    
    return text_without_urls, urls


# Main function to run the script
def main():
    file_path = '/Users/sheldonmrampton/Documents/@Reference/Social media/Twitter/twitter-2024-04-19-b507256fb4366adab232fc5f6832bbb1ee993c7c2a4164a7f254c494620e1251/data/tweets.js'

    # Extract tweets
    tweets_info = extract_tweets_from_json(file_path)

    csvfile = open('tweets.csv', 'w', newline='')
    csvwriter = csv.writer(
        csvfile, delimiter=',',
        quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    csvwriter.writerow([
        'ID', 'Created_at', 'URL', 'URL title', 'URL error', 'Text'
    ])

    # using list slicing
    # Get first N elements from list
    # N = 100
    # tweets_info = tweets_info[:N]

    for entry in tweets_info:
        print(f"ID: {entry['id']}, Created: {entry['created_at']}, Text: {entry['text']}")
        # date = datetime.datetime.fromtimestamp(entry['timestamp'])
        # # Format the date as YYYY/MM/DD
        # formatted_date = date.strftime('%Y/%m/%d')
        cleaned_text = remove_twitter_handles_improved(entry['text'])
        text, urls = find_and_remove_urls(cleaned_text)
        url = ''
        title = ''
        error = ''
        if len(urls) > 0:
            url = urls[0]
            [title, error] = get_webpage_title(url)
            if title.startswith('http'):
                url = title
                [title, error] = get_webpage_title(url)
            print(f"Title: {title}")
        csvwriter.writerow([entry['id'], entry['created_at'], url, title, error, text])

if __name__ == '__main__':
    main()
