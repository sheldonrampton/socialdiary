import json

# Load the JSON file
def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

# Extract posts
def extract_posts(data):
    posts = []
    for item in data['posts']:
        try:
            content = item['data'][0]['post']
            timestamp = item['timestamp']
            posts.append({'content': content, 'timestamp': timestamp})
        except KeyError:
            continue  # Some posts might not have the 'post' key
    return posts

# Main function to run the script
def main():
    filepath = 'your_facebook_data/posts/your_posts.json'
    data = load_json_file(filepath)
    posts = extract_posts(data)
    for post in posts:
        print(post)

if __name__ == '__main__':
    main()
