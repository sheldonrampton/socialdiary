import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime
import sqlite3
from dateutil import parser

conn = sqlite3.connect('gmail.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS GmailMessages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    timestamp INTEGER,
    from_email TEXT,
    to_emails TEXT,
    message TEXT
)
''')
conn.commit()
conn.close()

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_header(headers, name):
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return None

def convert_date_to_timestamp(date_str):
    # Try to parse the date string with dateutil.parser which handles more cases
    date_object = parser.parse(date_str)
    
    # Convert the datetime object to a UNIX timestamp
    timestamp = int(date_object.timestamp())
    
    return timestamp


def retrieve_emails(c, service, request):
    while request is not None:
        results = request.execute()
        messages = results.get('messages', [])
        nextPageToken = results.get('nextPageToken')

        if not messages:
            print('No messages found.')
        else:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                headers = msg['payload']['headers']
                subject = get_header(headers, 'Subject')
                date = get_header(headers, 'Date')
                timestamp = convert_date_to_timestamp(date)
                date_object = datetime.fromtimestamp(timestamp)
                formatted_date = date_object.strftime('%Y/%m/%d')
                from_email = get_header(headers, 'From')
                to_emails = get_header(headers, 'To')

                # Extract email body
                msg_str = ''
                if 'data' in msg['payload']['body']:
                    msg_str = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
                else:
                    parts = msg['payload'].get('parts', [])
                    for part in parts:
                        if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                            msg_str = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            break
                        else:
                            continue  # Skip if no text/plain part found

                # Save email with metadata
                file_name = f'gmail/message_{message["id"]}.txt'
                with open(file_name, 'w') as file:
                    file.write(f"Subject: {subject}\n")
                    file.write(f"Date: {date}\n")
                    file.write(f"From: {from_email}\n")
                    file.write(f"To: {to_emails}\n")
                    file.write("\n")
                    file.write(msg_str)
                    c.execute('''
                    INSERT INTO GmailMessages (subject, timestamp, from_email, to_emails, message)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (subject, timestamp, from_email, to_emails, msg_str))
                print(f'Saved {file_name} from {formatted_date}')

        # Prepare the next request
        request = service.users().messages().list_next(previous_request=request, previous_response=results)


def main():
    conn = sqlite3.connect('gmail.db')
    c = conn.cursor()
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    print(">>>>>> QUERY:", "SENT")
    request = service.users().messages().list(userId='me', labelIds=['SENT'])
    retrieve_emails(c, service, request)

    # Query for messages from a email addresses
    query = 'from:sheldon2000@tds.net'
    print(">>>>>> QUERY:", query)
    request = service.users().messages().list(userId='me', q=query)
    retrieve_emails(c, service, request)

    query = 'from:sheldon@prwatch.org'
    print(">>>>>> QUERY:", query)
    request = service.users().messages().list(userId='me', q=query)
    retrieve_emails(c, service, request)

    query = 'from:sheldon@sheldonrampton.com'
    print(">>>>>> QUERY:", query)
    request = service.users().messages().list(userId='me', q=query)
    retrieve_emails(c, service, request)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
