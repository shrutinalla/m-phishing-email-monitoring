'''from email.mime.text import MIMEText
import smtplib
from config import SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD, BASE_URL
from email_log_models import EmailLog
from send_mail import send_phishing_email

def send_phishing_email(receiver_email, employee_id, campaign_id):

    tracking_link = f"{BASE_URL}/track/{employee_id}/{campaign_id}"
    body = f"""
    <html>
    <body>

    <h2>Account Verification Required</h2>

    <p>Your organization account requires verification.</p>

    <a href="{tracking_link}">
        Verify Account
    </a>

    </body>
    </html>
    """

    msg = MIMEText(body, "html")

    msg["Subject"] = "Security Alert"
    msg["From"] = SMTP_EMAIL
    msg["To"] = receiver_email
    server = None
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass


def send_campaign_emails(
    campaign,
    employees,
    db
):

    sent = 0
    failed = 0


    for employee in employees:


        log = EmailLog(

            employee_id=employee.id,

            campaign_id=campaign.id,

            email=employee.email,

            status="Pending"

        )


        db.add(log)

        db.commit()



        try:

            send_phishing_email(

                employee.email,

                campaign.email_subject,

                campaign.email_template,

                employee.id,

                campaign.id

            )


            log.status = "Sent"

            sent += 1



        except Exception as e:


            log.status = "Failed"

            log.error_message = str(e)

            failed += 1



        db.commit()



    return sent, failed'''

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
import os


load_dotenv()


SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")



async def send_phishing_email(
    recipient_email: str,
    subject: str,
    body: str
):

    message = MIMEMultipart()

    message["From"] = SMTP_EMAIL

    message["To"] = recipient_email

    message["Subject"] = subject


    message.attach(
        MIMEText(
            body,
            "html"
        )
    )


    server = smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    )


    server.starttls()


    server.login(
        SMTP_EMAIL,
        SMTP_PASSWORD
    )


    server.sendmail(

        SMTP_EMAIL,

        recipient_email,

        message.as_string()

    )


    server.quit()


    return True