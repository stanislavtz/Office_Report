import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("SMTP_HOST")
SENDER = os.getenv("REPORT_SENDER")
RECIPIENT = os.getenv("REPORT_RECIPIENT")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_report(pdf_path: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = "Revenue Report"
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg.set_content("""
    Good morning Mr. Smith.
    
    Please find the revenue report attached.
    It gives visual information about our revenue by regions and revenue by products.
    Also it contains a chart with revenue by regions.
    
    Best regards,
    John Doe
    """)

    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application",
                           subtype="pdf", filename="revenue_report.pdf")

    with smtplib.SMTP(HOST, 587) as smtp:
        smtp.starttls()
        smtp.login(user=SMTP_USER, password=SMTP_PASSWORD)
        smtp.send_message(msg)