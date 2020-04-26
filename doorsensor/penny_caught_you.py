#!/usr/bin/env python3
# cc0 copyleft -- public domain
# write email with picture in attachment

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import smtplib
import socket
import datetime
import subprocess
import sql3 as sql
import os
import sys
import configparser

# read email addresses and passwords from config file
config = configparser.ConfigParser()
config.read('catarazzi_settings.ini')
sender_email = config['sender']['email'] # e.g. myemail@gmail.com
sender_password = config['sender']['password'] # e.g. myemailpasswd
smtp_server = config['sender']['smtp'] # e.g. smtp.gmail.com
port = config['sender']['smtp_port'] # 465 for SSL
receiver_email = config['recipient']['email'] # e.g. youremail@gmail.com
directory = config['catpics']['picture_dir']
db = config['catpics']['picture_db']
table = config['catpics']['picture_db_table']


def send_email_with_attachment(receiver_email, subject, body, filename, sender_email=sender_email, password=sender_password):
    """
    Send an email from sender_email to receiver_email with the subject subject and text body.
    Attach the file filename to the email.
    """
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    print("made email message:\n")
    print(message)


    # Open PDF file in binary mode
    if not os.path.exists(filename):
        message.attach(MIMEText('\n File was not found! ' + filename, "plain"))
    else:
        with open(filename, "rb") as attachment:
            print("attaching file " + filename + "...")
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            "attachment; filename= " + os.path.basename(filename),
            #"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
    text = message.as_string()
    print("converted message to text\n")

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        print("logging into mail server " + smtp_server + "...")
        server.login(sender_email, sender_password)
        print("sending email from " + sender_email + " to " + receiver_email + "...")
        server.sendmail(sender_email, receiver_email, text)
        print("Sent email.")

def new_pictures(cat_picture_dir, picture_db=db, picture_db_table=table):
    """
    Check db if pictures sent.
    Return dictionary with pictures that have not yet been sent.
    """
    dicts = sql.dicts_from_db_table(os.path.join(cat_picture_dir, picture_db), picture_db_table, constraints={'sent_email': 0})
    return dicts

def old_new_pictures(cat_picture_dir):
    """
    Create a tempfile that indicates when this function was last called.
    Check against previous tempfile what files are newer.
    Return date and filepath for new picture files.
    """
    tempfilename = "last_time_checked_for_pictures"
    tempfilepath = os.path.join(cat_picture_dir, tempfilepath)
    command = "find " + cat_picture_dir + " -type f -newerB " + tempfilepath
    print(command)
    output = subprocess.check_output(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    print(output)
    with(tempfilepath, 'w') as writetempfile:
        writetempfile.write(datetime.datetime.today().isoformat())
    for picture in output:
        print(picture)
    sys.exit()




if __name__ == "__main__":


    testing = False
    # testing = True
    if testing:
        subject = "Catarazzi cat alert -- testing"
        date = datetime.datetime.today().isoformat()
        body = "Ali Baba opened the cave! Time of openening:"
        body += "\n" + date
        filename = "cat.jpg"  # In same directory as script
        send_email_with_attachment(receiver_email, subject, body, filename)
        sys.exit()


    subject = "Catarazzi cat alert"
    bodyopen = "Ali Baba opened the cave! Time of picture:"
    bodyclosed = "Ali Baba closed the cave! Time of picture:"
    cat_picture_dir = directory
    # find any new pictures: emails not sent
    newpics = new_pictures(cat_picture_dir)
    write_to_db = []
    for picture in newpics:
        picturepath = picture['picture']
        date = picture['date']
        body = bodyopen if picture['door_open'] else bodyclosed
        #date = datetime.datetime.today().isoformat()
        body += "\n" + date.replace('T', ' ')
        send_email_with_attachment(receiver_email, subject, body, picturepath)
        # update dictionary to be written to db: mail has been sent
        picture.update({'sent_email': 1})
        write_to_db.append(picture)
        print("writing dict to db...")
        sql.dict_to_db(picture, os.path.join(cat_picture_dir, db), table) #, verbose=True)




