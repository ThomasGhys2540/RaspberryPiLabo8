#!/usr/bin/python3
import paho.mqtt.client as paho
from threading import Thread
import os
from random import choice
from time import sleep

game = False

direction = ["S", "U", "D"]
speed = ["1", "0"]

side = "*"

def on_message(client, userdata, msg):
	global game
	global side
	if not game:
		if "PL" in str(msg.payload) or "PR" in str(msg.payload):
			if "PL" in str(msg.payload):
				side = "L"
			else:
				side = "R"
			print(side)
			client.publish("broker/groep9", "Connected")
		elif "Start" in str(msg.payload):
			game = True

def loopForever():
	client.loop_forever()

def stop(self):
	client.loop_stop()
	client.unsubscribe("broker/groep9")
	client.disconnect()

def on_publish(client, userdata, result):
	print(str(result))

clear = lambda: os.system('clear')	

client = paho.Client()

client.on_message = on_message

client.on_publish = on_publish

client.connect("84.197.165.225", port=667)
client.subscribe("broker/groep9")

client.publish("broker/groep9", "Connect")

mqtt = Thread(target=loopForever)
mqtt.start()

while not game:
	pass

while game:
	sleep(0.25)
	client.publish("broker/groep9", side + choice(direction) + choice(speed))
