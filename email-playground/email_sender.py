from dotenv import load_dotenv
from os import getenv
from email.message import EmailMessage
import ssl
import smtplib
from string import Template
from pathlib import Path

load_dotenv()

html = Template(Path("index.html").read_text())


email_sender = getenv("EMAIL_SENDER")
email_password = getenv("EMAIL_PASSWORD")

email_receiver = getenv("EMAIL_RECEIVER")
subject = "Check out my new video"
body = html.substitute({"name": "TinTin"})

email = EmailMessage()
email["from"] = email_sender
email["to"] = email_receiver
email["subject"] = subject

email.set_content(body)


context = ssl.create_default_context()

with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
    smtp.ehlo()
    smtp.starttls(context=context)
    smtp.login(email_sender, email_password)
    smtp.send_message(email)

    print("all works")
