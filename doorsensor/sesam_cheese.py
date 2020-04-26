#!/usr/bin/env python3
# cc0 copyleft -- public domain
# keep checking if door is opened or closed
# on change, take a picture

import RPi.GPIO as GPIO
import time
import sys
import signal

import catarazzi
import penny_caught_you
import configparser
import datetime

# read settings from config file
config = configparser.ConfigParser()
config.read('catarazzi_settings.ini')
cat_picture_dir = config['catpics']['picture_dir']
db = config['catpics']['picture_db']
table = config['catpics']['picture_db_table']

subject = "Catarazzi cat alert"
date = datetime.datetime.today().isoformat()
bodyopen = "Ali Baba opened the cave! Time of openening:"
bodyclosed = "Ali Baba closed the cave! Time of closing:"
bodyopen += "\n" + date
bodyclosed += "\n" + date



def cleanup(signal, frame):
    """
    # Clean up when the user exits with keyboard interrupt
    """
    GPIO.cleanup()
    sys.exit(0)


def check_sesam():
    """
    Check if door status changed.
    If it did, take a picture and send it.
    """

    isOpen = None
    oldIsOpen = None


    while True:
        oldIsOpen = isOpen
        isOpen = GPIO.input(DOOR_SENSOR_PIN)
        if (isOpen and (isOpen != oldIsOpen)):
            print "Door is open!"
            print "isOpen is", isOpen
            print "oldIsOpen is", oldIsOpen
            picturepath = catarazzi.click('opened', cat_picture_dir, db=db, picture_db_table=table)
            # you could send an email here but this is now done separately
            #penny_caught_you.send_email_with_attachment(receiver_email, subject, bodyopen, picturepath)
        elif (isOpen != oldIsOpen):
            print "Door is closed!"
            print "isOpen is", isOpen
            print "oldIsOpen is", oldIsOpen
            picturepath = catarazzi.click('closed', cat_picture_dir, db=db, picture_db_table=table)
            # you could send an email here but this is now done separately
            #penny_caught_you.send_email_with_attachment(receiver_email, subject, bodyclosed, picturepath)
        time.sleep(0.1)

if __name__ == "__main__":


    # Source:
    # https://medium.com/conectric-networks/playing-with-raspberry-pi-door-sensor-fun-ab89ad499964

    # Set Broadcom mode so we can address GPIO pins by number.
    GPIO.setmode(GPIO.BCM)


    # This is the GPIO pin number we have one of the door sensor
    # wires attached to, the other should be attached to a ground pin.
    DOOR_SENSOR_PIN = 18


    # Set up the door sensor pin.
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # Set the cleanup handler for when user hits Ctrl-C to exit
    signal.signal(signal.SIGINT, cleanup)

    check_sesam()

