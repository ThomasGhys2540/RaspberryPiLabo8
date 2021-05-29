#!/usr/bin/python3

import paho.mqtt.client as paho

def on_message(client, callback, msg):
	print(str(msg.payload))

client = paho.Client()
client.connect("84.197.165.225", 667)
client.subscribe("broker/groep9")

client.on_message = on_message

client.publish("groep9", "Test")

print("done")

client.loop_forever()
