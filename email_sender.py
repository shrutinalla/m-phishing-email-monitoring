import os
import certifi
import ssl

ssl_context = ssl.create_default_context(
    cafile=certifi.where()
)
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

load_dotenv()


conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("SMTP_EMAIL"),
    MAIL_PASSWORD=os.getenv("SMTP_PASSWORD"),
    MAIL_FROM=os.getenv("SMTP_EMAIL"),

    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,

    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,

    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_phishing_email(
    recipient_email: str,
    subject: str,
    body: str
):

    message = MessageSchema(
        subject=subject,
        recipients=[recipient_email],
        body=body,
        subtype="html"
    )

    fast_mail = FastMail(conf)

    await fast_mail.send_message(message)