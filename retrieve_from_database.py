import sqlite3
import datetime


# Connect to SQLite database
conn = sqlite3.connect('social_media.db')
c = conn.cursor()

text = input("Search string: ")

# SQL query to find posts containing the string
query = "SELECT * FROM SocialPosts WHERE content LIKE '%" + text + "%' ORDER BY timestamp ASC"

try:
    c.execute(query)
    results = c.fetchall()
    if results:
        for row in results:
            date = datetime.datetime.fromtimestamp(int(row[3]))
            formatted_date = date.strftime('%Y/%m/%d')
            # print("Unique ID:", row[0])
            print("Platform:", row[1])
            # print("Platform ID:", row[2])
            # print("Timestamp:", row[3])
            print("Date:", formatted_date)
            print("Content:", row[4])
            print("URL:", row[5])
            print("---------------")
    else:
        print("No posts mentioning 'Biden' were found.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()
