import os
import smtplib

from dotenv import load_dotenv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
print("SMTP_HOST =", SMTP_HOST)
print("SMTP_PORT =", SMTP_PORT)
print("SMTP_EMAIL =", SMTP_EMAIL)

async def send_phishing_email(
    recipient_email: str,
    subject: str,
    body: str
):
    print("=" * 60)
    print("Preparing Email")
    print("Recipient :", recipient_email)
    print("Subject   :", subject)
    print("=" * 60)

    message = MIMEMultipart()

    message["From"] = SMTP_EMAIL
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(
        MIMEText(body, "html")
    )

    try:
        print("Connecting to SMTP...")

        server = smtplib.SMTP_SSL(
            SMTP_HOST,
            SMTP_PORT
        )
        
        print("SMTP Object:", type(server))
        print("SSL Connection Established")

        print("Logging into Gmail...")
        server.login(
            SMTP_EMAIL,
            SMTP_PASSWORD
        )

        print("Sending Email...")

        server.sendmail(
            SMTP_EMAIL,
            recipient_email,
            message.as_string()
        )

        print("Email Successfully Sent!")

        server.quit()

        print("SMTP Connection Closed")

        return True
    except Exception as e:
        print("=" * 60)
        print("SMTP ERROR")
        print("TYPE :", type(e))
        print("ERROR:", repr(e))
        print("=" * 60)
        raise