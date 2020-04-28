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
import time

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


def check_sesam_woosh():
    """
    Check if door status changed.
    If it did, take a picture and send it.
    """

    isOpen = None
    oldIsOpen = None
    # Start with no motion
    current_state = 0


    msg = 'opened' # door is always 'open'
    while True:
        # oldIsOpen = isOpen
        isOpen = GPIO.input(DOOR_SENSOR_PIN)
        #msg = 'opened' if isOpen else 'closed'
        # print("Door is currently " + msg)
        # print("Checking for change in door state...")
        # actually waiting for door sensor to close = logical 0
        print("Waiting for door to open...")
        #if isOpen != oldIsOpen:
        if isOpen == 0: # catflap moved past sensor! door sensor "closed"
            # State change! Start detecting motion
            # register whether door opened or closed:
            catarazzi_message = 'opened' # door is always 'open'
            #if isOpen:
            #    print "Door is open! Was closed before."
            #    catarazzi_message = 'opened'
            #else:
            #    print "Door is closed! Was opened before."
            #    catarazzi_message = 'closed'
            # start detecting motion for 20 seconds
            t_detect = 20
            t_end = time.time() + t_detect
            picturepath = catarazzi.click(catarazzi_message, cat_picture_dir, db=db, picture_db_table=table)
            while time.time() < t_end:
                old_state = current_state
                current_state = GPIO.input(pir_sensor)
                catarazzi_message = 'motion'
                print("will detect motion for " + str(t_end - time.time()) + " more seconds")
                # take pictures first 4 seconds
                if int((t_end - time.time())) > (t_detect - 4):
                    print("Take picture anyway!")
                    picturepath = catarazzi.click(catarazzi_message, cat_picture_dir, db=db, picture_db_table=table)
                    time.sleep(0.5)
                    continue

                # then check if motion is detected
                if current_state == 1 and (current_state != old_state):

                    # PIR is detecting movement!
                    print("GPIO pin %s is %s" % (pir_sensor, current_state))
                    # Check if this is the first time movement was
                    # detected and print a message!
                    if current_state != old_state:
                        print('Motion detected!')
                    picturepath = catarazzi.click(catarazzi_message, cat_picture_dir, db=db, picture_db_table=table)
                    # reset to no motion detected, else you get 20 pictures in a row...?
                    # print("Resetting state to no motion detected")
                    # current_state = 0 # reset to no motion
                elif (current_state != old_state):
                    # PIR is not detecting movement.
                    # Again check if this is the first time movement
                    # stopped and print a message.
                    # if old_state == 0:
                    print('Motion ended!')
                else:
                    if current_state == 1:
                        print("cat still here")
                    else:
                        print("still no cat")

                # take time between checking for motion
                time.sleep(0.5)
            print("finished detecting motion. start waiting for door...")
            # oldIsOpen = 1 # set to logical 1 meaning open: should check for door to 'close' or when flap passes sensor --> logical 0

        # sleep between checking door sensor
        time.sleep(0.1)



if __name__ == "__main__":


    # Source:
    # https://medium.com/conectric-networks/playing-with-raspberry-pi-door-sensor-fun-ab89ad499964

    # Set Broadcom mode so we can address GPIO pins by number.
    GPIO.setmode(GPIO.BCM)


    # This is the GPIO pin number we have one of the door sensor
    # wires attached to, the other should be attached to a ground pin.
    DOOR_SENSOR_PIN = 18

    # passive infrared motion sensor connected to
    # VCC to pin 2
    # OUT to pin 16 (GPIO 23)
    # GND to pin 6 (GND)
    # Source:
    # https://tutorials-raspberrypi.com/connect-and-control-raspberry-pi-motion-detector-pir/

    # the order of the pins on the motion sensor when seen on the bottom is VCC OUT GND
    # Source:
    # https://www.hackster.io/hardikrathod/pir-motion-sensor-with-raspberry-pi-415c04

    # PIR sensor OUT is connected to GPIO pin 23
    # https://medium.com/conectric-networks/playing-with-raspberry-pi-door-sensor-fun-ab89ad499964
    # https://pinout.xyz/#
    pir_sensor = 23


    # Set up the door sensor pin.
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # Set up the motion sensor pin
    # GPIO.setup(pir_sensor, GPIO.IN)
    GPIO.setup(pir_sensor, GPIO.IN)
    # , pull_up_down = GPIO.PUD_UP)


    # Set the cleanup handler for when user hits Ctrl-C to exit
    signal.signal(signal.SIGINT, cleanup)


    check_sesam_woosh()

