import time
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os


# Configure the OpenAI key from an environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


def summarize_text(text):
    """Use OpenAI's API to summarize the provided text."""
    try:
        # response = client.completions.create.create(
        #     engine="text-davinci-002",  # Make sure this is the correct model name
        #     prompt="Summarize this text:\n\n" + text,
        #     max_tokens=150,
        #     temperature=0.5  # Optional: adjust for creativity of the response
        # )
        response = client.completions.create(model="davinci-002",
        prompt="Summarize this text:\n\n" + text,
        max_tokens=500,
        temperature=0.5)
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Failed to generate a summary: {e}")
        return None


def fetch_webpage_content(url):
    """Fetch the content of a webpage by URL and return the main text using BeautifulSoup, with retries and backoff."""
    max_retries = 5  # Maximum number of retries
    backoff_factor = 1  # Time in seconds to wait between retries

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            soup = BeautifulSoup(response.content, 'html.parser')
            text = ' '.join(p.text for p in soup.find_all('p'))
            print(text)
            return text
        except requests.exceptions.HTTPError as e:
            print(429)
            if e.response.status_code == 429:
                time.sleep(backoff_factor * (2 ** attempt))  # Exponential backoff
            else:
                raise
        except requests.RequestException as e:
            print(f"Failed to fetch the webpage: {e}")
            return None

    return None  # Return None if all retries fail


def main():
    # url = "https://myfox8.com/news/florida-man-shoots-son-to-death-after-argument-over-beer/"  # Replace with the URL you want to summarize
    url = 'http://www.nytimes.com/2016/06/28/upshot/exit-polls-and-why-the-primary-was-not-stolen-from-bernie-sanders.html?smid=fb-share'
    text = fetch_webpage_content(url)
    print(text)
    if text:
        summary = summarize_text(text)
        if summary:
            print("Summary:")
            print(summary)
        else:
            print("No summary could be generated.")
    else:
        print("No text could be extracted from the webpage.")

if __name__ == "__main__":
    main()
