#!/usr/bin/env python3
"""
From 
http://www.themakercupboard.space/Raspberry/blog_files/lisiparoi.html
and
https://github.com/uktechreviews/picademy-camera/blob/master/flash.py
and
https://pinout.xyz/#
"""

image_name = 'hi_withleds'
#image_name = 'hi_noleds'

image_path = '/home/pi/'
extension = '.jpg'
your_addition = ''
image_dest = image_path + image_name + str(your_addition) + extension
print("Will save image to " + image_dest)

from picamera import PiCamera
import time
import RPi.GPIO as GPIO


LED = 16

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED,GPIO.OUT)
GPIO.output(LED,GPIO.LOW)

# frames = int(input("How many frames? "))
# timebetween = int(input("Interval between each photo "))
# actual_timebetween = timebetween - 6
# framecount = 0
# total_time = round((frames * timebetween)/60)
# print ("It will take approx ",total_time," minutes")


print("Camera LEDS going ON")
GPIO.output(LED, GPIO.HIGH)
if 'noleds' in image_name:
    print("Camera LEDS going OFF")
    GPIO.output(LED, GPIO.LOW)
time.sleep(2)
camera = PiCamera()
camera.rotation = 180

print("Capturing image to " + image_dest)
localtime = time.asctime( time.localtime(time.time()) )
camera.annotate_text=localtime
camera.capture(image_dest)
time.sleep(2)

print("Camera LEDS going OFF")
GPIO.output(LED, GPIO.LOW)
time.sleep(2)

# while framecount < frames:
#     with PiCamera() as camera:
#     #    camera.start_preview()
#         GPIO.output(LED, GPIO.HIGH)
#         localtime = time.asctime( time.localtime(time.time()) )
#         camera.annotate_text=localtime
#         camera.capture('/home/pi/hi%s.jpg'%(framecount))
#         framecount +=1
#         GPIO.output(LED, GPIO.LOW)
#         time.sleep(actual_timebetween)
#camera.stop_preview()
GPIO.cleanup() 