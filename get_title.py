import requests
from bs4 import BeautifulSoup
from requests.exceptions import Timeout


def get_webpage_title(url):
    max_retries = 2  # Maximum number of retries
    backoff_factor = 1  # Time in seconds to wait between retries
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
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
            return title_tag.text if title_tag else ''
        except Timeout:
            print("The request timed out")
        except requests.RequestException as e:
            print(f"Error accessing the URL: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    return ''

# Example usage:
url = 'http://www.nationalmemo.com/judge-attacked-trump-long-history-serving-country/'

# http://www.usnews.com/opinion/articles/2016-06-01/bernie-sanders-path-to-victory-is-implausible-to-deceptive-part-infinity'
print(get_webpage_title(url))
