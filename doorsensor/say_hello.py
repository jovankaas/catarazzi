#!/usr/bin/env python3
# cc0 copyleft -- public domain
# example sending an email using SSL

import smtplib, ssl
import configparser


# read email addresses and passwords from config file
config = configparser.ConfigParser()
config.read('catarazzi_settings.ini')
sender_email = config['sender']['email'] # e.g. myemail@gmail.com
password = config['sender']['password'] # e.g. myemailpasswd
smtp_server = config['sender']['smtp'] # e.g. smtp.gmail.com
port = config['sender']['smtp_port'] # 465 for SSL
receiver_email = config['recipient']['email'] # e.g. youremail@gmail.com

message = """\
Subject: Hi there

This message is sent from catarazzi."""

context = ssl.create_default_context() # create SSL context
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

