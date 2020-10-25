#!/usr/bin/env python3
# cc0 copyleft -- public domain
# example sending an email using SSL
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import configparser


# read email addresses and passwords from config file
config = configparser.ConfigParser()
config.read('catarazzi_settings.ini')
sender_email = config['sender']['email'] # e.g. myemail@gmail.com
sender_password = config['sender']['password'] # e.g. myemailpasswd
smtp_server = config['sender']['smtp'] # e.g. smtp.gmail.com
port = config['sender']['smtp_port'] # 465 for SSL
receiver_email = config['recipient']['email'] # e.g. youremail@gmail.com
subject = "Catarazzi cat alert -- testing"



if __name__ == "__main__":
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails


    body = """\
    Subject: Hi there
    
    This message is sent from catarazzi."""


    # Add body to email
    message.attach(MIMEText(body, "plain"))
    print("made email message:\n")
    print(message)
    text = message.as_string()
    print("converted message to text\n")
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        print("logging into mail server " + smtp_server + "...")
        server.login(sender_email, sender_password)
        print("sending email from " + sender_email + " to " + receiver_email + "...")
        server.sendmail(sender_email, receiver_email, text)
        print("Sent email.")


# context = ssl.create_default_context() # create SSL context
# with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, message)

