import RPi.GPIO as GPIO
import time
import sys
import signal
import datetime


# Source:
# https://medium.com/conectric-networks/playing-with-raspberry-pi-door-sensor-fun-ab89ad499964

# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)


# This is the GPIO pin number we have one of the door sensor
# wires attached to, the other should be attached to a ground pin.
DOOR_SENSOR_PIN = 18


isOpen = None
oldIsOpen = None

# Clean up when the user exits with keyboard interrupt
def cleanup(signal, frame): 
    GPIO.cleanup() 
    sys.exit(0)


# Set up the door sensor pin.
GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# Set the cleanup handler for when user hits Ctrl-C to exit
signal.signal(signal.SIGINT, cleanup)

def date_time_no_float():
    """
    Return date and time now in isoformat up to the float:
    no fractions of seconds.
    Replace T with space.
    """
    iso = datetime.datetime.isoformat(datetime.datetime.now())
    return iso[:iso.index('.')].replace('T', ' ')

while True: 
    oldIsOpen = isOpen 
    isOpen = GPIO.input(DOOR_SENSOR_PIN)
    if (isOpen and (isOpen != oldIsOpen)):
        print "Door is open! Time: ", date_time_no_float()
        print "pin value is", isOpen
        print "old pin value is", oldIsOpen
    elif (isOpen != oldIsOpen):
        print "Door is closed! Time: ", date_time_no_float()
        print "pin value is", isOpen
        print "old pin value is", oldIsOpen
    time.sleep(0.1)
