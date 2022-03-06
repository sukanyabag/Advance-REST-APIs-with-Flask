#the methods in this library is intented to send any arbitrary email to the users
from requests import Response, post
from typing import List
import os

FAILED_LOAD_API_KEY = "Failed to load Mailgun API key! Make sure you have set it."
FAILED_LOAD_DOMAIN = "Failed to load Mailgun Domain. Make sure you have set it."
ERROR_SENDING_EMAIL = "Error in sending activation email. User registeration failed!"

class MailgunException(Exception):
    #init constructor calls super class Exception to print exceptions into our custom
    # error handling class "MailgunException"
    def __init__(self, message:str):
        super().__init__(message)

class Mailgun:
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN') #if not set defaults to None
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')  #if not set defaults to None
    FROM_TITLE = "E-Commerce Store API"
    FROM_EMAIL = "postmaster@sandboxacc0df4769db4923b75ca265e64386b5.mailgun.org"

    @classmethod
    def send_email(cls, email: List[str], subject: str, text:str, html:str) -> Response:
        #check and handle errors if any
        if cls.MAILGUN_API_KEY is None:
            raise MailgunException(FAILED_LOAD_API_KEY)

        if cls.MAILGUN_DOMAIN is None:
            raise MailgunException(FAILED_LOAD_DOMAIN)
        
        #send a request to the mailgun api for sending the activation email to users
        response = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )

        if response.status_code != 200:
            raise MailgunException(ERROR_SENDING_EMAIL)

        return response
