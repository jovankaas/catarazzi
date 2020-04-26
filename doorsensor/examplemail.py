#!/usr/bin/env python3
# cc0 copyleft -- public domain
# example sending an email using SSL

import smtplib
import socket
import configparser

if __name__ == "__main__":



    config = configparser.ConfigParser()
    config.read('catarazzi_settings.ini')
    sender = config['sender']['email']
    sender_pw = config['sender']['password']
    sender_smtp = config['sender']['smtp']
    sender_smtp_port = config['sender']['smtp_port']
    recipient = config['recipient']['email']
    smtpconn = smtplib.SMTP_SSL(sender_smtp, sender_smtp_port)
    smtpconn.login(sender, sender_pw)
    hostname = socket.gethostname()
    afzender = sender
    subject= "Cat detection from " + hostname
    text = "test cat detection\n"
    message = 'Subject: {}\n\n{}'.format(subject, text)
    print(message)
    smtpconn.sendmail(afzender, recipient, message)
    smtpconn.close()
