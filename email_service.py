from email.mime.text import MIMEText
import smtplib


def send_phishing_email(receiver_email, employee_id, campaign_id):

    tracking_link = f"http://127.0.0.1:8000/track/{employee_id}/{campaign_id}"

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
    msg["From"] = "kusumabhavani.a@gmail.com"
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()

    server.login(
        "kusumabhavani.a@gmail.com",
        "bcolhzrlmhhbywpn"
    )

    server.sendmail(
        "kusumabhavani.a@gmail.com",
        receiver_email,
        msg.as_string()
    )

    server.quit()