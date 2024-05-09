# Preserves line breaks.

from bs4 import BeautifulSoup

def strip_html(html_content):
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Remove custom tags and their contents if needed
    for tag in soup.find_all(['x-stuff-for-pete', 'x-sigsep']):
        tag.decompose()
    
    # Extract text from the parsed HTML
    text = soup.get_text(separator='\n', strip=True)
    return text

# Load the HTML content from a file
# with open('gmail/samples/message_16880adbfd9978a8.txt', 'r') as file:
with open('gmail/samples/untitled 3.html', 'r') as file:
    html_content = file.read()

# Use the function to strip HTML and print the resulting plain text
plain_text = strip_html(html_content)
print(plain_text)