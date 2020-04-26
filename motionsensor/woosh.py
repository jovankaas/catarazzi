import RPi.GPIO as GPIO
import time
import signal
import sys

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

# Set board mode so we can address GPIO pins.
# GPIO.setmode(GPIO.BOARD)
# Set Broadcom mode so we can address GPIO pins by number.
GPIO.setmode(GPIO.BCM)

# Set up the motion sensor pin
# GPIO.setup(pir_sensor, GPIO.IN)
GPIO.setup(pir_sensor, GPIO.IN)
# , pull_up_down = GPIO.PUD_UP)

# Start with no motion
current_state = 0

# Clean up when the user exits with keyboard interrupt
def cleanup(signal, frame): 
    GPIO.cleanup() 
    sys.exit(0)

# Set the cleanup handler for when user hits Ctrl-C to exit
signal.signal(signal.SIGINT, cleanup)

while True:
    old_state = current_state
    current_state = GPIO.input(pir_sensor)
    if current_state == 1 and (current_state != old_state):
        # PIR is detecting movement!
        print("GPIO pin %s is %s" % (pir_sensor, current_state))
        # Check if this is the first time movement was
        # detected and print a message!
        if current_state != old_state:
            print('Motion detected!')
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
    time.sleep(1)
# while True:
#     time.sleep(0.1)
#     current_state = GPIO.input(pir_sensor)
#     # When motion detected:
#     if current_state == 1:
#         print("cat alarm!")
#         # stop after one second:
#         time.sleep(1)
#         time.sleep(5)
#     else:
#         print("GPIO pin %s is %s" % (pir_sensor, current_state))
#         print("no cat!")
#     current_state = 0
# except KeyboardInterrupt:
#     pass
# finally:
#     GPIO.cleanup()
