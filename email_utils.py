# email_utils.py
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("GMAIL_USER")
EMAIL_PASSWORD = os.getenv("GMAIL_PASS")

def send_violation_email(to_email, license_plate, violation_type, description):
    try:
        msg = EmailMessage()
        msg['Subject'] = f"Traffic Violation Notice for {license_plate}"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email

        msg.set_content(f"""
Dear Vehicle Owner,

Your vehicle with license plate {license_plate} was detected violating traffic rules.

Violation Type: {violation_type}
Details: {description}

This is an automated notice. Please ensure compliance with road safety regulations.

Regards,
Traffic Authority AI System
""")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"✅ Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        return False
