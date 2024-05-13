import sqlite3
import datetime
import re
from bs4 import BeautifulSoup


def is_html(content):
    # Pattern to detect minimal HTML tags
    html_pattern = re.compile(r'<\s*([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>(.*?)<\s*/\1\s*>', re.IGNORECASE | re.DOTALL)
    # Search for the pattern in the content
    return bool(html_pattern.search(content))


def perform_action():
    # Example of an action: print a message
    print("Action performed.")


def strip_html(html_content):
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Remove custom tags and their contents if needed
    for tag in soup.find_all(['x-stuff-for-pete', 'x-sigsep']):
        tag.decompose()
    
    # Extract text from the parsed HTML
    text = soup.get_text(separator='\n', strip=True)
    return text


sig_lines = ["""--
Sheldon Rampton
"I think, therefore I procrastinate."
(608) 206-2745""",
"--Sheldon Rampton\n"]


def clean_message(text):
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


def has_nested_quotes(email_text):
    # Split the email into lines
    lines = email_text.split('\n')
    
    # Process each line to handle quotes and clean text
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line not in ['','>','>>','>>>','>>>>','>>>s>>']:
            cleaned_lines.append(line)

    # Join the cleaned lines back into a single string
    email_text = '\n'.join(cleaned_lines)
    for sig_line in sig_lines:
        email_text = email_text.replace(sig_line, '')
    email_text = email_text.strip()

    print("==============")
    print(email_text)
    print("==============")
    lines = email_text.strip().split('\n')
    
    # Variable to keep track of the expected number of '>' for the current line
    expected_quote_level = 0
    
    # Iterate through each line in the email
    for line in lines:
        # Strip leading whitespace for accurate '>' counting
        stripped_line = line.lstrip()
        # Count '>' at the beginning of the line
        count = 0
        for char in stripped_line:
            if char == '>':
                count += 1
            else:
                break
        
        # Check if the count of '>' matches the expected quote level
        if count != expected_quote_level:
            # If the line starts with text or has fewer '>' than expected, return False
            if count < expected_quote_level:
                return False
            # Update the expected_quote_level to the new level found
            expected_quote_level = count
        
    # If all lines have appropriate quoting levels, return True
    if expected_quote_level > 0:
        return True
    else:
        return False


conn = sqlite3.connect('gmail.db')
c = conn.cursor()
query = "SELECT * FROM GmailMessages ORDER BY RANDOM() LIMIT 1"

while True:
    # Perform the action
    try:
        c.execute(query)
        results = c.fetchall()
        if results:
            for row in results:
                mail_id = row[0]
                subject = row[1]
                timestamp = row[2]
                from_email = row[3]
                to_emails = row[4]
                message = row[5]
                print("ID:", mail_id)
                print("Subject:", subject)
                print("Timestamp:", timestamp)
                print("From:", from_email)
                print("To:", to_emails)
                print("Message:", message)
                print("--------------------")
                result = is_html(message)
                print(f"{'HTML' if result else 'Plain text'}")
                if result:
                    print("--------------------")
                    plain_text = strip_html(message)
                    print("PLAIN TEXT VERSION:")
                    print(plain_text)
                else:
                    if has_nested_quotes(message):
                        print("HAS NESTED QUOTES")
                    else:
                        print("DOES NOT HAVE NESTED QUOTES")
                    cleaned_text = clean_message(message)
                    print("CLEANED TEXT:")
                    print(cleaned_text)
                print("--------------------")
        else:
            print("No emails found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Ask the user if they want to continue
    user_input = input("Do you want to try another? (y/n): ")

    # Check if the user wants to exit the loop
    if user_input.lower() == 'n':
        print("Exiting the program.")
        break

conn.close()
