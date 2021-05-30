#!/usr/bin/python3
import paho.mqtt.client as paho
import os

def on_message(client, userdata, msg):
	coords = str(msg.payload).split(';')
	for received in coords:
		print(received)
	print("===============")

os.system('clear')

client = paho.Client()

client.on_message = on_message

client.connect("84.197.165.225", 667)
client.subscribe("broker/groep9")

client.loop_forever()
