import os
import re

def is_html(content):
    # Pattern to detect minimal HTML tags
    html_pattern = re.compile(r'<\s*([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>(.*?)<\s*/\1\s*>', re.IGNORECASE | re.DOTALL)
    # Search for the pattern in the content
    return bool(html_pattern.search(content))

def scan_directory_for_html(directory_path):
    # List all files in the given directory
    for filename in os.listdir(directory_path):
        # Construct full file path
        file_path = os.path.join(directory_path, filename)
        # Check if it's a file
        if os.path.isfile(file_path):
            # Open and read the file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            # Use the is_html function to check if the file contains HTML
            result = is_html(content)
            # Print the filename and whether it contains HTML
            print(f"{filename}: {'HTML' if result else 'Plain text'}")

# Example usage: adjust the path to the directory containing your message files
directory_path = 'gmail/samples'
scan_directory_for_html(directory_path)
