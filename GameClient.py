#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)

isPlaying = True
speed = False
temp = 0

def determineInput():
    if GPIO.input(2):
        print("Omhoog")
        global temp 
        temp += 1
        return
    elif GPIO.input(3):
        print("Omlaag")
        return
    elif GPIO.input(4):
        speed = not speed
        if (speed == True):
            print("Snel")
        elif (speed == False):
            print("Traag")
x = 0
while x < 3:
    GPIO.output(14, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(14, GPIO.LOW)
    time.sleep(1)
    x += 1

while (isPlaying):
    determineInput()
    if (temp == 5):
        GPIO.output(14, GPIO.LOW)
        GPIO.cleanup()
        sys.exit()
