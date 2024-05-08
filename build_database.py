from datetime import datetime
import sqlite3
import csv


conn = sqlite3.connect('social_media.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS SocialPosts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT,
    platform_id TEXT,
    timestamp TEXT,
    content TEXT,
    url TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS Urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT
    title TEXT,
    error TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS TwitterUsers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    try:
        for post in posts:
            timestamp = post[0]
            date = post[1]
            url = post[2]
            url_title = post[3]
            url_error = post[4]
            post_text = post[5]
            c.execute('''
            INSERT INTO SocialPosts (platform, platform_id, timestamp, content, url)
            VALUES (?, ?, ?, ?, ?)
            ''', ('Facebook post', timestamp, timestamp, post_text, url))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Attempted to insert a duplicate post.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

print("Posts inserted successfully.")

conn = sqlite3.connect('social_media.db')
c = conn.cursor()
comments_file = "comments.csv"
with open(comments_file, "r") as infile:
    comments = csv.reader(infile)
    next(comments, None)  # skip the headers
    try:
        for comment in comments:
            timestamp = comment[0]
            date = comment[1]
            url = comment[2]
            url_title = comment[3]
            url_error = comment[4]
            comment_text = comment[5]
            c.execute('''
            INSERT INTO SocialPosts (platform, platform_id, timestamp, content, url)
            VALUES (?, ?, ?, ?, ?)
            ''', ('Facebook comment', timestamp, timestamp, comment_text, url))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Attempted to insert a duplicate comment.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
print("Comments inserted successfully.")

conn = sqlite3.connect('social_media.db')
c = conn.cursor()
tweets_file = "tweets.csv"
with open(tweets_file, "r") as infile:
    tweets = csv.reader(infile)
    next(tweets, None)  # skip the headers
    try:
        for tweet in tweets:
            tweet_id = tweet[0]
            timestamp = convert_date_to_timestamp(tweet[1])
            url = tweet[2]
            url_title = tweet[3]
            url_error = tweet[4]
            tweet_text = tweet[5]
            c.execute('''
            INSERT INTO SocialPosts (platform, platform_id, timestamp, content, url)
            VALUES (?, ?, ?, ?, ?)
            ''', ('Tweet', tweet_id, timestamp, tweet_text, url))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Attempted to insert a duplicate tweet.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

print("Tweets inserted successfully.")
