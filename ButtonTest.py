#!/usr/bin/python3
# Multi-frame tkinter application v2.3
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread

up = 3
down = 5
speed = 7

GPIO.setmode(GPIO.BCM)

GPIO.setup(up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(speed, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

Speed = 0
Direction = "S"

def UpButton(channel):
    if Direction is "U":
        Direction = "S"
        print("Direction static")
    else:
        Direction = "U"
        print("Direction going up")

def DownButton(channel):
    if Direction is "D":
        Direction = "S"
    else:
        Direction = "D"

def SpeedButton(channel):
    if Speed is 0:
        Speed = 1
        print("Speed is now 1")
    else:
        Speed = 0
        print("Speed is now 0")

GPIO.add_event_detect(up, GPIO.BOTH, callback=UpButton, bouncetime=300)
GPIO.add_event_detect(down, GPIO.BOTH, callback=DownButton, bouncetime=300)
GPIO.add_event_detect(speed, GPIO.RISING, callback=SpeedButton, bouncetime=300)