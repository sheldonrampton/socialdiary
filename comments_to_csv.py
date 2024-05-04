import json
import requests
from bs4 import BeautifulSoup
import csv
from requests.exceptions import Timeout
import datetime

# Load the JSON file
def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


# Extract entries
def extract_entries(data):
    entries = []
    for item in data["comments_v2"]:
        entry = {
            'timestamp': item.get('timestamp'),
        }

        # Attempt to find URL in attachments if available
        url = ''
        comment = ''
        if 'attachments' in item:
            for attachment in item['attachments']:
                for att_data in attachment.get('data', []):
                    external_context = att_data.get('external_context', {})
                    if 'url' in external_context:
                        url = external_context['url']
        if 'data' in item:
            for data in item['data']:
                if 'comment' in data:
                    comment = data['comment']['comment']
        if comment != '' or url != '':
            entry['comment'] = comment
            entry['url'] = url
            entries.append(entry)
    return entries


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


# Main function to run the script
def main():
    filepath = '/Users/sheldonmrampton/Documents/@Reference/Social media/Facebook/facebook-sheldonrampton-2024-04-27-pvGjU2dZ/your_facebook_activity/comments_and_reactions/comments.json'  # Update this path to where your JSON file is stored
    data = load_json_file(filepath)
    entries = extract_entries(data)

    csvfile = open('comments.csv', 'w', newline='')
    csvwriter = csv.writer(
        csvfile, delimiter=',',
        quotechar='"', quoting=csv.QUOTE_MINIMAL
    )
    csvwriter.writerow([
        'Timestamp', 'Date', 'Url', 'URL title', 'URL error', 'Comment'
    ])

    # using list slicing
    # Get first N elements from list
    # N = 100
    # entries = entries[:N]

    for entry in entries:
        print(f"Timestamp: {entry['timestamp']}, URL: {entry['url']}, Post: {entry['comment']}")
        # print(f"{entry['url']}")
        title = ''
        error = ''
        date = datetime.datetime.fromtimestamp(entry['timestamp'])
        # Format the date as YYYY/MM/DD
        formatted_date = date.strftime('%Y/%m/%d')
        if entry['url'] != '':
            [title, error] = get_webpage_title(entry['url'])
            print(f"Title: {title}")
        csvwriter.writerow([entry['timestamp'], formatted_date, entry['url'],
            title, error, entry['comment']])

if __name__ == '__main__':
    main()
