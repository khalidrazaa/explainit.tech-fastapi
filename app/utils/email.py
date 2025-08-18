import os
from email.message import EmailMessage
from aiosmtplib import send
from dotenv import load_dotenv

load_dotenv()

async def send_email_otp(to_email: str, otp: str):
    message = EmailMessage()
    from_email = os.getenv("EMAIL_USERNAME")
    
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = "Your OTP for ExplainIt.Tech"
    message.set_content(f"Your OTP is: {otp}\nIt will expire in 5 minutes.")

    await send(
        message,
        hostname=os.getenv("EMAIL_HOST"),
        port=int(os.getenv("EMAIL_PORT")),
        username=os.getenv("EMAIL_USERNAME"),
        password=os.getenv("EMAIL_PASSWORD"),
        start_tls=True,   # ✅ this enables STARTTLS for Outlook
    )