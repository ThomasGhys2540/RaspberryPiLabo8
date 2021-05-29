#!/usr/bin/python3

import paho.mqtt.client as paho

client = paho.Client()
client.connect("84.197.165.225", 667)
client.subscribe("groep9")

client.loop_forever()
