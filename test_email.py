import asyncio
from email_sender import send_phishing_email


async def test():
    await send_phishing_email(
        "your_test_email@gmail.com",
        "MIDHANI Test Email",
        """
        <h2>SMTP Test Successful</h2>
        <p>Email sending works.</p>
        """
    )


asyncio.run(test())