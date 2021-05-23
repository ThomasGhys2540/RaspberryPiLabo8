#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.OUT, initial=GPIO.LOW)

isPlaying = True
speed = False
temp = 0

def determineInput():
    if GPIO.input(16):
        var = GPIO.input(16)
        print(var)
        var = GPIO.input(20)
        print(var)
        var = GPIO.input(21)
        print(var)
        print("Omhoog")
        global temp 
        temp += 1
        return
    elif GPIO.input(20):
        print("Omlaag")
        return
    elif GPIO.input(21):
        global speed
        speed = not speed
        if (speed == True):
            print("Snel")
        elif (speed == False):
            print("Traag")
x = 0
while x < 3:
    GPIO.output(26, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(26, GPIO.LOW)
    time.sleep(1)
    x += 1

while (isPlaying):
    determineInput()
    if (temp == 5):
        GPIO.output(14, GPIO.LOW)
        GPIO.cleanup()
        sys.exit()
