# Preserves line breaks.


def clean_message(text):
    # Split the message into lines
    lines = text.split('\n')
    
    # Process each line to handle quotes and clean text
    cleaned_lines = []
    for line in lines:
        # Check if the line starts with '>' and handle accordingly
        if line.startswith('>'):
            # You can uncomment the next line if you want to skip quoted lines
            # continue
            # Or you can remove '>' to clean it but keep the text
            line = line.lstrip('> ').lstrip('> ')  # Remove leading '>' and extra spaces
        cleaned_lines.append(line)

    # Join the cleaned lines back into a single string
    cleaned_text = '\n'.join(cleaned_lines)
    return cleaned_text

# Load the message content from a file
with open('gmail/samples/sent_message_18d32127d9c0deec.txt', 'r', encoding='utf-8') as file:
    message_content = file.read()

# Clean the message content
cleaned_message = clean_message(message_content)
print(cleaned_message)


# def clean_message(text):
#     # Split the message into lines
#     lines = text.split('\n')
    
#     # Process each line
#     cleaned_lines = []
#     for line in lines:
#         if line.startswith('[') and 'image:' in line:
#             # Skip lines that are just image markers or similar non-text content
#             continue
#         # if 'https://' in line or 'http://' in line:
#         #     # Remove URLs or replace them with a placeholder or description
#         #     line = '(URL removed for privacy)'
#         cleaned_lines.append(line)

#     # Join the cleaned lines back into a single string
#     cleaned_text = '\n'.join(cleaned_lines)
#     return cleaned_text

# # Load the message content from a file
# with open('gmail/samples/sent_message_18e3553f7daee2b8.txt', 'r', encoding='utf-8') as file:
#     message_content = file.read()

# # Clean the message content
# cleaned_message = clean_message(message_content)
# print(cleaned_message)






# from bs4 import BeautifulSoup

# def strip_html(html_content):
#     # Use BeautifulSoup to parse the HTML content
#     soup = BeautifulSoup(html_content, 'lxml')
    
#     # Remove custom tags and their contents if needed
#     for tag in soup.find_all(['x-stuff-for-pete', 'x-sigsep']):
#         tag.decompose()
    
#     # Extract text from the parsed HTML
#     text = soup.get_text(separator='\n', strip=True)
#     return text

# # Load the HTML content from a file
# # with open('gmail/samples/message_16880adbfd9978a8.txt', 'r') as file:
# with open('gmail/samples/untitled 3.html', 'r') as file:
# with open('gmail/samples/sent_message_18e3553f7daee2b8.txt', 'r', encoding='utf-8') as file:
#     html_content = file.read()

# # Use the function to strip HTML and print the resulting plain text
# plain_text = strip_html(html_content)
# print(plain_text)