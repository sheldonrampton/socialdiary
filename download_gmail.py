import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_header(headers, name):
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return None


def main():
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

    request = service.users().messages().list(userId='me', labelIds=['SENT'])
    while request is not None:
        results = request.execute()
        messages = results.get('messages', [])
        nextPageToken = results.get('nextPageToken')

        if not messages:
            print('No sent messages found.')
        else:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                headers = msg['payload']['headers']
                subject = get_header(headers, 'Subject')
                date = get_header(headers, 'Date')
                from_email = get_header(headers, 'From')
                to_emails = get_header(headers, 'To')

                # Extract email body
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
                file_name = f'gmail/sent_message_{message["id"]}.txt'
                with open(file_name, 'w') as file:
                    file.write(f"Subject: {subject}\n")
                    file.write(f"Date: {date}\n")
                    file.write(f"From: {from_email}\n")
                    file.write(f"To: {to_emails}\n")
                    file.write("\n")
                    file.write(msg_str)
                print(f'Saved {file_name}')

        # Prepare the next request
        request = service.users().messages().list_next(previous_request=request, previous_response=results)

if __name__ == '__main__':
    main()
