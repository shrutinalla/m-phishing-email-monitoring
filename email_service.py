from email.mime.text import MIMEText
import smtplib
from config import SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD, BASE_URL

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
            