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
comments_file = "comments.csv"
with open(comments_file, "r") as infile:
    comments = csv.reader(infile)
    next(comments, None)  # skip the headers
    unique_id = 1
    unique_url_id = 1
    try:
        for comment in comments:
            timestamp = comment[0]
            date = comment[1]
            url = comment[2]
            url_title = comment[3]
            url_error = comment[4]
            comment_text = comment[5]
            c.execute('''
            INSERT INTO SocialPosts (unique_id, platform, platform_id, timestamp, content, url)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (unique_id, 'Facebook comment', timestamp, timestamp, comment_text, url))
            unique_id += 1
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Attempted to insert a duplicate comment.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

print("Comments inserted successfully.")
