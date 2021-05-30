#!/usr/bin/python3
import paho.mqtt.client as paho
from threading import Thread
import os

game = False

def on_message(client, userdata, msg):
	global game
	if not game:
		if "PL" in str(msg.payload) or "PR" in str(msg.payload):
			print("Sending message")
			client.publish("broker/groep9", "Connected")
		elif "Start" in str(msg.payload):
			game = True

def loopForever():
	client.loop_forever()

def stop(self):
	client.loop_stop()
	client.unsubscribe("broker/groep9")
	client.disconnect()

clear = lambda: os.system('clear')	

client = paho.Client()

client.on_message = on_message

client.connect("84.197.165.225", port=667)
client.subscribe("broker/groep9")

client.publish("broker/groep9", "Connect")

mqtt = Thread(target=loopForever)
mqtt.start()

while not game:
	pass

while game:
	x = input()
	client.publish("broker/groep9", x)
