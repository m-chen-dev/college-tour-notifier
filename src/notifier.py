from win11toast import notify
from custom_logging import log
from twilio.rest import Client
from os import getenv
from dotenv import load_dotenv

load_dotenv(".env")

PERSONAL_PHONE_NUMBER = getenv("PERSONAL_PHONE_NUMBER")
TWILIO_PHONE_NUMBER = getenv("TWILIO_PHONE_NUMBER")
TWILIO_ACCOUNT_SID = getenv("TWILIO_ACCOUNT_SID")
TWILIO_API_KEY_SID = getenv("TWILIO_API_KEY_SID")
TWILIO_API_KEY_SECRET = getenv("TWILIO_API_KEY_SECRET")
ENABLE_SMS = False

TWILIO_CLIENT = Client(TWILIO_API_KEY_SID, TWILIO_API_KEY_SECRET, TWILIO_ACCOUNT_SID) if ENABLE_SMS else None

def send_message(message : str, title: str, url : str):    
    log(message)
    notify(
        title=title,
        body=message,
        on_click=url
    )
    
    if TWILIO_CLIENT is None: return
    message_instance = TWILIO_CLIENT.messages.create(
        body="sms_event_notifications",
        from_=TWILIO_PHONE_NUMBER,
        to=PERSONAL_PHONE_NUMBER
    )
    log(f"Successfully sent message! (Message SID: [{message_instance.sid}])")
