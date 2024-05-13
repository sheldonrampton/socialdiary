import sqlite3

def fetch_data(keyword):
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
    WHERE content LIKE ?
    """
    # SQL query for GmailMessages table
    query_gmail = """
    SELECT 'gmail' AS source, id, 'Email' as platform, subject,
    timestamp AS unix_timestamp,
    message, from_email, to_emails 
    FROM GmailMessages 
    WHERE message LIKE ?
    """
    
    # Execute the queries
    social_results = cursor_social.execute(query_social, ('%' + keyword + '%',)).fetchall()
    gmail_results = cursor_gmail.execute(query_gmail, ('%' + keyword + '%',)).fetchall()
    
    # Close the database connections
    conn_social.close()
    conn_gmail.close()
    
    # Combine results
    combined_results = social_results + gmail_results
    
    # Sort the combined results by timestamp (note the position of timestamp in each tuple)
    combined_sorted = sorted(combined_results, key=lambda x: x[4])
    
    return combined_sorted

# Usage
keyword = "cognitive"
results = fetch_data(keyword)
for result in results:
    print(result)
