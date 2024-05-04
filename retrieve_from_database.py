import sqlite3


# Connect to SQLite database
conn = sqlite3.connect('social_media.db')
c = conn.cursor()

# SQL query to find posts containing the word 'Biden'
query = "SELECT * FROM SocialPosts WHERE content LIKE '%Biden%'"

try:
    c.execute(query)
    results = c.fetchall()
    if results:
        for row in results:
            print("Unique ID:", row[0])
            print("Platform:", row[1])
            print("Platform ID:", row[2])
            print("Timestamp:", row[3])
            print("Content:", row[4])
            print("URL:", row[5])
            print("---------------")
    else:
        print("No posts mentioning 'Biden' were found.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()
