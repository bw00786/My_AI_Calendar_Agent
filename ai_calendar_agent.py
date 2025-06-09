import os
import datetime
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import openai
from dateutil import parser
import pytz

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GOOGLE_CREDENTIALS_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'primary'
DEFAULT_TIMEZONE = 'America/Los_Angeles'  # Change to your timezone

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

class GoogleCalendarAgent:
    def __init__(self):
        self.service = self._authenticate_google()
        self.timezone = self._get_calendar_timezone()
    
    def _authenticate_google(self):
        """Authenticate with Google Calendar API"""
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GOOGLE_CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return build('calendar', 'v3', credentials=creds)
    
    def _get_calendar_timezone(self):
        """Get calendar's default timezone"""
        calendar = self.service.calendars().get(calendarId=CALENDAR_ID).execute()
        return calendar.get('timeZone', DEFAULT_TIMEZONE)
    
    def _parse_datetime(self, dt_str):
        """Parse datetime string with calendar's timezone"""
        dt = parser.parse(dt_str)
        if not dt.tzinfo:
            dt = pytz.timezone(self.timezone).localize(dt)
        return dt.isoformat()
    
    def create_event(self, event_details):
        """Create calendar event from structured data"""
        event = {
            'summary': event_details['summary'],
            'description': event_details.get('description', ''),
            'start': {'dateTime': self._parse_datetime(event_details['start'])},
            'end': {'dateTime': self._parse_datetime(event_details['end'])},
        }
        
        created_event = self.service.events().insert(
            calendarId=CALENDAR_ID,
            body=event
        ).execute()
        
        return created_event.get('htmlLink')
    
    def process_natural_language(self, user_input):
        """Use GPT-4o to convert natural language to structured event data"""
        system_prompt = f"""
        You are an AI scheduling assistant that creates Google Calendar events. 
        Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        Calendar timezone: {self.timezone}
        
        Extract event details in JSON format with these keys:
        - summary (string): Event title
        - description (string): Optional description
        - start (string): Start time in ISO 8601 format
        - end (string): End time in ISO 8601 format
        
        Follow these rules:
        1. If no duration specified, default to 1 hour
        2. If no date specified, use today
        3. Always include timezone offset if not provided
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        return json.loads(response.choices[0].message['content'])
    
    def schedule_appointment(self, user_request):
        """Full workflow: NLP processing + event creation"""
        event_data = self.process_natural_language(user_request)
        event_link = self.create_event(event_data)
        return event_link

# Example Usage
if __name__ == "__main__":
    # Initialize agent
    agent = GoogleCalendarAgent()
    
    # User request in natural language
    user_request = "Schedule meeting with John tomorrow at 3pm for 1 hour about project Q"
    
    # Process request and create event
    try:
        event_link = agent.schedule_appointment(user_request)
        print(f"Event created: {event_link}")
    except Exception as e:
        print(f"Error: {str(e)}")