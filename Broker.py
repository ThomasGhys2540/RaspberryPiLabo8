#!/usr/bin/python3
import paho.mqtt.client as paho
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
button1 = 3
button2 = 5
button3 = 7
button4 = 8
button5 = 10
button6 = 12

speed = "0"
speedp2 = "0"

GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def on_connect(client, userdata, flags, rc):
 print("Connected with result code " + str(rc))

def on_publish(client, userdata, msg):
 print("Message has been send")

def on_message(client, userdata, msg):
 message = str(msg.payload)
 print("Message that has been received: "+ message)

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
 global button4
 global button5
 global button6
 GPIO.add_event_detect(button4, GPIO.RISING, callback=my_callback, bouncetime=300)
 GPIO.add_event_detect(button5, GPIO.RISING, callback=my_callback, bouncetime=300)
 GPIO.add_event_detect(button6, GPIO.RISING, callback=my_callback, bouncetime=300)

def my_callback(chnl):
 global button1, button2, button3, button4, button5 ,button6, speed, speedp2
 if chnl == button1:
  sendToBroker("L", "U", str(speed))
 if chnl == button2:
  if speed == "0":
   speed = "1"
  elif speed == "1":
   speed = "0"
 if chnl == button3:
  sendToBroker("L", "D", str(speed))
 if chnl == button4:
  sendToBroker("R", "U", str(speedp2))
 if chnl == button5:
  if speedp2 == "0":
   speedp2 = "1"
  elif speedp2 == "1":
   speedp2 = "0"
 if chnl == button6:
  sendToBroker("R", "D", str(speedp2))

def sendToBroker(player, direction, speed):
 message = str(player) + str(direction) + str(speed)
 (rc, mid) = client.publish("broker/groep9", message, qos=1)

def remevents():
 global button1
 global button2
 global button3
 GPIO.remove_event_detect(button1)
 GPIO.remove_event_detect(button2)
 GPIO.remove_event_detect(button3)
 global button4
 global button5
 global button6
 GPIO.remove_event_detect(button4)
 GPIO.remove_event_detect(button5)
 GPIO.remove_event_detect(button6)

addevents()
client.loop_forever()
remevents()
GPIO.cleanup()
