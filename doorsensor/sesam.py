import RPi.GPIO as GPIO
import time
import sys
import signal


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

while True: 
    oldIsOpen = isOpen 
    isOpen = GPIO.input(DOOR_SENSOR_PIN)
    if (isOpen and (isOpen != oldIsOpen)):
        print "Door is open!"
        print "isOpen is", isOpen
        print "oldIsOpen is", oldIsOpen
    elif (isOpen != oldIsOpen):
        print "Door is closed!"
        print "isOpen is", isOpen
        print "oldIsOpen is", oldIsOpen
    time.sleep(0.1)
