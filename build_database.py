from datetime import datetime
import sqlite3
import csv


conn = sqlite3.connect('social_media.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS SocialPosts (
    unique_id TEXT PRIMARY KEY,
    platform TEXT,
    platform_id TEXT,
    timestamp TEXT,
    content TEXT,
    url TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Urls (
    unique_id TEXT PRIMARY KEY,
    url TEXT
    title TEXT,
    error TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS TwitterUsers (
    unique_id TEXT PRIMARY KEY,
    handle TEXT
    name TEXT
)
''')

conn.commit()
conn.close()


def convert_date_to_timestamp(date_str):
    # Define the date format
    date_format = '%a %b %d %H:%M:%S %z %Y'
    
    # Parse the date string into a datetime object
    date_object = datetime.strptime(date_str, date_format)
    
    # Convert the datetime object to a UNIX timestamp (seconds since Jan 01 1970. (UTC))
    timestamp = int(date_object.timestamp())
    
    return timestamp


conn = sqlite3.connect('social_media.db')
c = conn.cursor()
posts_file = "posts.csv"
with open(posts_file, "r") as infile:
    posts = csv.reader(infile)
    next(posts, None)  # skip the headers
    unique_id = 1
    unique_url_id = 1
    try:
        for post in posts:

            timestamp = post[0]
            date = post[1]
            url = post[2]
            url_title = post[3]
            url_error = post[4]
            post_text = post[5]
            c.execute('''
            INSERT INTO SocialPosts (unique_id, platform, platform_id, timestamp, content, url)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (unique_id, 'Facebook post', timestamp, timestamp, post_text, url))
            unique_id += 1
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Attempted to insert a duplicate post.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

print("Posts inserted successfully.")


# Example usage
date_str = "Fri Apr 19 02:11:34 +0000 2024"
timestamp = convert_date_to_timestamp(date_str)
print("Timestamp:", timestamp)
