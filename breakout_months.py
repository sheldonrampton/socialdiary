import sqlite3
import datetime
import re
from bs4 import BeautifulSoup
import os


sig_lines = ["""
--
Sheldon Rampton
"I think, therefore I procrastinate."
(608) 206-2745
"""]


def is_html(content):
    """
    Returns true of the content is HTML, false otherwise.
    """

    # Pattern to detect minimal HTML tags
    html_pattern = re.compile(r'<\s*([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>(.*?)<\s*/\1\s*>', re.IGNORECASE | re.DOTALL)
    # Search for the pattern in the content
    return bool(html_pattern.search(content))


def strip_html(html_content):
    """
    Converts HTML to plain text.
    """

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Remove custom tags and their contents if needed
    for tag in soup.find_all(['x-stuff-for-pete', 'x-sigsep']):
        tag.decompose()
    
    # Extract text from the parsed HTML
    text = soup.get_text(separator='\n', strip=True)
    return text


def clean_message(text):
    """
    Cleans some unwanted text out of email message bodies,
    including sig lines and > characters at the beginning of
    quoted text.
    """

    # Split the message into lines
    lines = text.split('\n')
    
    # Process each line to handle quotes and clean text
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # Check if the line starts with '>' and handle accordingly
        if line.startswith('>'):
            # You can uncomment the next line if you want to skip quoted lines
            # continue
            # Or you can remove '>' to clean it but keep the text
            line = line.lstrip('> ').lstrip('> ')  # Remove leading '>' and extra spaces
        elif line.startswith('[') and 'image:' in line:
            # Skip lines that are just image markers or similar non-text content
            continue
        if line.startswith('<') and line.endswith('>'):
            line = line[1:-1]
        cleaned_lines.append(line)

    # Join the cleaned lines back into a single string
    cleaned_text = '\n'.join(cleaned_lines)
    for sig_line in sig_lines:
        cleaned_text = cleaned_text.replace(sig_line, '')
    cleaned_text = cleaned_text.replace("\n\n\n\n\n", "\n\n").replace("\n\n\n\n", "\n\n")
    cleaned_text = cleaned_text.replace("\n\n\n", "\n\n")
    return cleaned_text


def fetch_data(keyword):
    """
    Retrieves the contents of the social_media and gmail databases
    and combines them into a single 
    """

    # Connect to the SQLite databases
    conn_social = sqlite3.connect('social_media.db')
    conn_gmail = sqlite3.connect('gmail.db')
    
    # Create cursors for each connection
    cursor_social = conn_social.cursor()
    cursor_gmail = conn_gmail.cursor()
    
    # SQL query for SocialPosts table
    query_social = """
    SELECT 'social' AS source, id, platform, platform_id,
    CAST(timestamp AS INTEGER) AS unix_timestamp, 
    content, url
    FROM SocialPosts 
    """
    # SQL query for GmailMessages table
    query_gmail = """
    SELECT 'gmail' AS source, id, 'Email' as platform, subject,
    timestamp AS unix_timestamp,
    message, from_email, to_emails 
    FROM GmailMessages 
    """
    
    # Execute the queries
    social_results = cursor_social.execute(query_social).fetchall()
    gmail_results = cursor_gmail.execute(query_gmail).fetchall()
    
    # Close the database connections
    conn_social.close()
    conn_gmail.close()
    
    # Combine results
    combined_results = social_results + gmail_results
    
    # Sort the combined results by timestamp (note the position of timestamp in each tuple)
    combined_sorted = sorted(combined_results, key=lambda x: x[4])
    
    return combined_sorted


"""
Main loop: Creates a "months" directory, retrieves all of the
content in the database, and writes out that content to a separate
file for each month for which content exists.
"""

# Create the "months" directory if it doesn't exist
if not os.path.exists('months'):
    os.makedirs('months')

# Dictionary to hold data grouped by month
data_by_month = {}
results = fetch_data('')

for row in results:
    # Parse the numerical timestamp
    timestamp = datetime.datetime.fromtimestamp(row[4])
    # Create a key for the month and year
    month_key = timestamp.strftime('%Y-%m')

    # Add the row to the corresponding month key
    if month_key not in data_by_month:
        data_by_month[month_key] = 1
        file_path = os.path.join('months', f'{month_key}.txt')
        file = open(file_path, 'w')

    date = datetime.datetime.fromtimestamp(int(row[4]))
    formatted_date = date.strftime('%Y/%m/%d')
    file.write("Platform: " + row[2] + '\n')
    file.write("Date: " + formatted_date + '\n')
    message = row[5]
    if row[2] == 'Email':
        email = ''
        if row[7] is not None:
            email = row[7]
        file.write('To: ' + email + '\n')
        result = is_html(message)
        if result:
            plain_text = strip_html(message)
            file.write(plain_text + '\n')
        else:
            cleaned_text = clean_message(message)
            file.write(cleaned_text + '\n')
    else:
        file.write("URL: " + row[6] + '\n')
        file.write(message + '\n')
    file.write("---------------\n")


print("Data has been successfully written to the 'months' directory.")
