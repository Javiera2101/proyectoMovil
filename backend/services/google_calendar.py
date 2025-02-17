from google.oauth2 import service_account
from googleapiclient.discovery import build

from google.oauth2 import id_token
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'config/credenciales.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

def create_google_calendar_event(reminder):
    event = {
        'summary': reminder.title,
        'description': reminder.description,
        'start': {
            'dateTime': reminder.date.isoformat(),
            'timeZone': 'America/Santiago',
        },
        'end': {
            'dateTime': reminder.date.isoformat(),
            'timeZone': 'America/Santiago',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event

def verify_google_token(token: str) -> bool:
    try:
        # Aquí debes proporcionar la audiencia correcta para tu aplicación.
        audience = "863154778458-518rlvmkuakb7vu044dtshf7b99dava0.apps.googleusercontent.com"
        # Verificar el token ID de Google
        id_info = id_token.verify_oauth2_token(token, Request(), audience)

        # Si la verificación es exitosa, el token es válido
        return True
    except ValueError:
        # Si el token no es válido, lanzará un ValueError
        return False
    