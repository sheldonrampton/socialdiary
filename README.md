# Social Diary
v0.0.0

This is a collection of code designed to collect, organize and search social media posts from Facebook and Twitter. Ideally it will become a tool, perhaps an app, that I can use to help draft book chapters and blog entries based on my posting history.

## Loading libraries
    source myenv2/bin/activate

## Source data

Facebook data is in a downloaded Facebook archive, in the following locations:
- *Posts* are at path your_facebook_activity/posts/your_posts__check_ins__photos_and_videos_1.json
- *Comments* are at path your_facebook_activity/comments_and_reactions/comments.json

Twitter data is in a downloaded Twitter archive, in the following locations:
- *Tweets* are at path data/tweets.js

The Twitter data fis a Javascript file (not JSON) and requires a little bit of fixing before it can be loaded as JSON.

Both Facebook and Twitter have additional data, including media files with images I've uploaded.

## Code

### Working code
* build_gmail_db.py: uses the Gmail API to build a SQLite database of my email sending history.
* breakout_months.py: generates a separate text file for each month of content in the databases.
* comments_to_csv.py: processes my Facebook comments into a CSV file.
* posts_to_csv.py: processes my Facebook posts into a CSV file
* search_everything: searches for all content that matches a keyword and outputs it all as a text file.
* tweets_to_csv.py: processes my Facebook tweets into a CSV file
* requirements.txt: Python module dependencies (not currently 100% accurate)

### Documentation
* README.md: You are here
* TODO.md: My roadmap of future enhancements and features

### Test code
* build_database.py: test script to load some content from a CSV of Facebook posts into a SQLite database.
* build_database_comments.py: loads content from a CSV of Facebook comments into the SQLite database.
* categorize_by_topic.py: an untested script (probably needs fixing) to filter content by matching category keywords and 
* categorize_posts.py: processes a posts.csv file and uses Latent Dirichlet Allocation (LDA) or Non-negative Matrix Factorization (NMF) to automatically identify topic categories. Not ready for prime time, but this might be a step in the direction of an AI tool for organizing content.
* cleanup_html.py: test script to clean up some sample HTML-based email messages.
* combine_databases.py: test script to combine the Gmail database and social media database into a single data collection.
* get_title.py: test script to look up a web page based on its URL and retrieve the title. It works pretty well. I'd like to have a script that can retrieve the full text of the content of a web page and then use AI (e.g., AWS Comprehend) to summarize it.
* html_detector.py: test script to determine whether or not a message is HTML-formatted.
* import_json.py: an early test script for importing Facebook posts from the .json archive
* import_json2.py: a fleshed-out version of the early test script
* parse_tweets.py: a test script to parse tweets from the Twitter tweets.js file
* retrieve_from_database.py: test script to retrieve some content from the SQLite database.
* retrieve_email_test: test script that retrieves a random email and then does some processing of it to determine what type of email it is (HTML/plain text; does it quote other emails?) annd also to clean it up for better text analysis.
* summarize_topic.py: summarizes text using an AI summarizer. Uses tensorflow. Big memory hog. Doesn't work well.
* summarize_url.py: test script to use the ChatGPT API to summarize the content of a web page. Doesn't work very well.
