# Google Calendar AI Agent

An intelligent Python application that creates Google Calendar events from natural language requests using OpenAI's GPT-4 and the Google Calendar API.

## Features

- **Natural Language Processing**: Convert plain English requests into calendar events
- **Smart Date/Time Parsing**: Automatically interprets relative dates and times
- **Timezone Handling**: Respects your calendar's default timezone
- **Google Calendar Integration**: Direct integration with your Google Calendar
- **Flexible Event Creation**: Supports custom descriptions, durations, and scheduling

## Requirements

### Dependencies

```
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
openai
python-dateutil
pytz
```

### API Access

- **Google Calendar API**: Enabled in Google Cloud Console
- **OpenAI API**: Valid API key with GPT-4 access

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd google-calendar-ai-agent
   ```

2. **Install dependencies**
   ```bash
   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib openai python-dateutil pytz
   ```

3. **Set up Google Calendar API**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Calendar API
   - Create credentials (OAuth 2.0 Client IDs)
   - Download the credentials file and save as `credentials.json` in the project directory

4. **Set up OpenAI API**
   ```bash
   export OPENAI_API_KEY='your-openai-api-key-here'
   ```

## Configuration

Update the configuration variables in the script:

```python
GOOGLE_CREDENTIALS_FILE = 'credentials.json'
CALENDAR_ID = 'primary'  # or specific calendar ID
DEFAULT_TIMEZONE = 'America/Los_Angeles'  # Change to your timezone
```

## Usage

### Basic Usage

```python
from google_calendar_agent import GoogleCalendarAgent

# Initialize the agent
agent = GoogleCalendarAgent()

# Create events with natural language
event_link = agent.schedule_appointment("Schedule meeting with John tomorrow at 3pm for 1 hour about project Q")
print(f"Event created: {event_link}")
```

### Example Requests

The agent can handle various natural language formats:

```python
# Different ways to create events
requests = [
    "Schedule dentist appointment next Tuesday at 10am",
    "Book conference room for team standup every Monday at 9:30am for 30 minutes",
    "Add lunch with Sarah on Friday at noon",
    "Schedule code review session tomorrow from 2pm to 4pm",
    "Create all-hands meeting next week Wednesday at 3pm for 2 hours"
]

for request in requests:
    event_link = agent.schedule_appointment(request)
    print(f"Created: {event_link}")
```

### Command Line Usage

```bash
python google_calendar_agent.py
```

## How It Works

1. **Authentication**: The agent authenticates with Google Calendar using OAuth 2.0
2. **Natural Language Processing**: User input is sent to GPT-4 for structured extraction
3. **Event Parsing**: The AI converts natural language into JSON with event details
4. **Calendar Integration**: Events are created directly in your Google Calendar
5. **Response**: Returns a link to the created event

## API Response Format

The GPT-4 model extracts events in this JSON format:

```json
{
  "summary": "Meeting with John",
  "description": "Project Q discussion",
  "start": "2024-01-15T15:00:00-08:00",
  "end": "2024-01-15T16:00:00-08:00"
}
```

## Smart Defaults

- **Duration**: Defaults to 1 hour if not specified
- **Date**: Uses today if no date is mentioned
- **Timezone**: Applies your calendar's default timezone
- **Time Format**: Handles both 12-hour and 24-hour formats

## Error Handling

The application includes error handling for:
- Authentication failures
- Invalid date/time formats
- API quota limits
- Network connectivity issues

## File Structure

```
google-calendar-ai-agent/
├── google_calendar_agent.py    # Main application
├── credentials.json           # Google API credentials (you provide)
├── token.json                # OAuth token (auto-generated)
└── README.md                 # This file
```

## Security Notes

- Keep your `credentials.json` and `token.json` files secure
- Never commit API keys to version control
- Use environment variables for sensitive configuration
- The `token.json` file is automatically created during first authentication

## Troubleshooting

### Common Issues

**"Credentials not found"**
- Ensure `credentials.json` is in the project directory
- Verify the file was downloaded from Google Cloud Console

**"OpenAI API Error"**
- Check your API key is set correctly
- Verify you have GPT-4 access on your OpenAI account

**"Calendar API disabled"**
- Enable Google Calendar API in Google Cloud Console
- Ensure proper scopes are configured

**"Timezone issues"**
- Update `DEFAULT_TIMEZONE` to match your location
- Check your Google Calendar timezone settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT-4 natural language processing
- Google for the Calendar API
- Python dateutil library for robust date parsing
