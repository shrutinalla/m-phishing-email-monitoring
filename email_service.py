import os
import smtplib
import mimetypes

from dotenv import load_dotenv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

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
    body: str,
    attachment_path: str = None,
    attachment_name: str = None
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

    # ------------------------------------
    # Attach Campaign File (Optional)
    # ------------------------------------

    if attachment_path and os.path.exists(attachment_path):

        content_type, _ = mimetypes.guess_type(
            attachment_path
        )

        if content_type is None:
            content_type = "application/octet-stream"

        maintype, subtype = content_type.split("/", 1)

        with open(
            attachment_path,
            "rb"
        ) as file:

            attachment = MIMEBase(
                maintype,
                subtype
            )

            attachment.set_payload(
                file.read()
            )

        encoders.encode_base64(
            attachment
        )

        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=attachment_name
            if attachment_name
            else os.path.basename(
                attachment_path
            )
        )

        message.attach(
            attachment
        )

        print("Attachment Added :", attachment_path)

    try:

        print("Connecting to SMTP...")

        server = smtplib.SMTP_SSL(
            SMTP_HOST,
            SMTP_PORT
        )

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