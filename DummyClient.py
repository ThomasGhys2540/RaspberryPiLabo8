#!/usr/bin/python3
import paho.mqtt.client as paho
from threading import Thread
import os

game = False

answeredFirst = False;

def on_message(client, userdata, msg):
	global game
	if not game:
		if str(msg.payload) == "PL":
			print("Sending message")
			client.publish("broker/groep9", "Connected")
		elif str(msg.payload) == "PR":
			print("Sending message")
			client.publish("broker/groep9", "Connected")
			game = True
	else:
		clear()
		coords = str(msg.payload).split(';')
		print("===============")
		for received in coords:
			print(received)
		print("===============")

def loopForever(self):
	client.loop_forever()

def stop(self):
	client.loop_stop()
	client.unsubscribe("broker/groep9")
	client.disconnect()

clear = lambda: os.system('clear')	

client = paho.Client()

client.on_message = on_message

client.connect("84.197.165.225", 667)
client.subscribe("broker/groep9")

client.publish("broker/groep9", "Connect")

client.loop_start()

while not answeredFirst:
	pass

client.loop_stop()

client.publish("broker/groep9", "Connect")

while True:
	client.loop_forever()
