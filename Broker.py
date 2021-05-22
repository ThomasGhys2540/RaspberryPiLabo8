#!/usr/bin/python3
import paho.mqtt.client as paho
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
button1 = 3
button2 = 5
button3 = 7
up_mess = "VAR=UP;NAAM=GoingUP"
speed_mess = "VAR=SP;NAAM=SPEED"
dn_mess = "VAR=DN;NAAM=GoingDown"

GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def on_connect(client, userdata, flags, rc):
 print("Connected with result code " + str(rc))

def on_publish(client, userdata, msg):
 print("Message has been send")

def on_message(client, userdata, msg):
 message = str(msg.payload)
 sub_message = message[6:8]
 print("Message that has been received: "+ sub_message)

def on_disconnect(client, userdata, rc):
 print("Disconnecting with result code " + str(rc))

def on_subscribe(client, userdata, mid, granted_qos):
 print("Subscribed: " + str(mid) + " " + str(granted_qos))

client = paho.Client()
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish
client.connect("broker.mqttdashboard.com", 1883)
client.subscribe("broker/groep9")

def addevents():
 global button1
 global button2
 global button3
 GPIO.add_event_detect(button1, GPIO.RISING, callback=my_callback, bouncetime=300)
 GPIO.add_event_detect(button2, GPIO.RISING, callback=my_callback, bouncetime=300)
 GPIO.add_event_detect(button3, GPIO.RISING, callback=my_callback, bouncetime=300)

def my_callback(chnl):
 global button1, button2, button3, up_mess, dn_mess, speed_mess
 if chnl == button1:
  (rc, mid) = client.publish("broker/groep9", up_mess, qos=1)
 if chnl == button2:
  (rc, mid) = client.publish("broker/groep9", dn_mess, qos=1)
 if chnl == button3:
  (rc, mid) = client.publish("broker/groep9", speed_mess, qos=1)

def remevents():
 global button1
 global button2
 global button3
 GPIO.remove_event_detect(button1)
 GPIO.remove_event_detect(button2)
 GPIO.remove_event_detect(button3)

addevents()
client.loop_forever()
remevents()
GPIO.cleanup()
