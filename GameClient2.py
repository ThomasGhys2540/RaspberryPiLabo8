#!/usr/bin/python3

import gpiozero
import time

button1 = gpiozero.InputDevice(16)
button2 = gpiozero.InputDevice(20)
button3 = gpiozero.InputDevice(21)
led = gpiozero.LED(14)

isPlaying = True
speed = False
temp = 0

def determineInput():
	if button1.value:
		print("Omhoog")
		return
	elif button2.value:
		print("Omlaag")
		return
	elif button3.value:
		global speed
		if speed:
			print("Snel")
		elif not speed:
			print("Traag")

x = 0
while x < 3:
	led.on()
	time.sleep(1)
	led.off()
	time.sleep(1)
	x += 1

while (isPlaying):
    determineInput()
    if (temp == 5):
        led.off()
        GPIO.cleanup()
        sys.exit()
