# Multi-frame tkinter application v2.3
import tkinter as tk
import paho.mqtt.client as paho
import Broker
from threading import Thread
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN)
GPIO.setup(5, GPIO.IN)
GPIO.setup(7, GPIO.IN)

class PongApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(MainMenu)

        paddle = " "
        direction = "S"
        speed = 0
        askedSide = False
        gameStarted = False
        GUIStarted = False

        mqtt = Thread(target=MQTT)

        job1.start

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def MQTT():
        def on_message(client, userdata, msg):
            if paddle == " ":
                paddle = str(msg.payload)[1]
                askedSide = False
                client.publish("broker/groep9", "Connected", qos=1)
            elif str(msg.payload) == "Start":
                gameStarted = True
        def UpdateBroker():
            message = paddle + direction + str(speed)
            client.publish("broker/groep9", message)
        
        def upButton(channel):
            direction = "U"
            UpdateBroker()
            
        def downButton(channel):
            direction = "D"
            UpdateBroker()

        def ReleaseUpButton(channel):
            if direction == "U":
                direction = "S"
                UpdateBroker()

        def ReleaseDownButton(channel):
            if direction == "D":
                direction = "S"
                UpdateBroker()

        def SpeedButtonSwitch(channel):
            if speed == 0:
                speed = 1
            else
                speed = 0
            UpdateBroker()
            
        client = paho.Client()
        
        client.on_message = on_message
        client.connect("84.197.165.225", 667)
        client.subscribe("broker/groep9")

        while !GUIStarted:
            print("WaitingForStart")

        client.publish("broker/groep9", "Connect", qos=1)

        while !gameStarted:
            print("MQTT Waiting")

        GPIO.add_event_detect(3, GPIO.RISING, callback=upButton, bouncetime=300)
        GPIO.add_event_detect(3, GPIO.FALLING, callback=ReleaseUpButton, bouncetime=300)

        GPIO.add_event_detect(5, GPIO.RISING, callback=downButton, bouncetime=300)
        GPIO.add_event_detect(5, GPIO.FALLING, callback=ReleaseDownButton, bouncetime=300)

        GPIO.add_event_detect(7, GPIO.RISING, callback=SpeedButtonSwitch, bouncetime=300)

        while gamestarted:
            
        GPIO.cleanup()

class MainMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="black")
        tk.Label(self, text="Welcome to the Main Menu", bg="black", fg="white").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Start Game", command=lambda: master.switch_frame(GameScreen), bg="red").pack()

class GameScreen(tk.Frame):      
    def __init__(self, master):
        self.LPaddlePosY = 300
        self.RPaddlePosY = 300
        self.LPaddlePosYBottom = self.LPaddlePosY + 200
        self.RPaddlePosYBottom = self.RPaddlePosY + 200

        GUIStarted = True

        while !gameStarted:
            print("GUI Waiting")
        
        tk.Frame.__init__(self, master, bg="black")
        self.canvas = tk.Canvas(master, bg="black", width=1080, height=800)
        self.LeftPaddle = self.canvas.create_rectangle(0, self.LPaddlePosY, 50, self.LPaddlePosYBottom, fill="white")
        self.RightPaddle = self.canvas.create_rectangle(1030, self.RPaddlePosY, 1080, self.RPaddlePosYBottom, fill="red")
        self.Ball = self.canvas.create_oval(80,300,130,350,fill="blue")
        self.canvas.pack()
        tk.Button(self, text="End the Game!", command=lambda: master.switch_frame(VictoryScreen), bg="red").pack()
        tk.Button(self, text="Move you dipshit", command=lambda: self.Movement(), bg="red").pack()
        self.Movement()

    def Movement(self):
        self.x = 0
        self.y = 5
        self.canvas.move(self.LeftPaddle, self.x, self.y)

class VictoryScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="black")
        tk.Label(self, text="This is the end there is nothing beyond here", bg="black", fg="white").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to the Main menu", command=lambda: master.switch_frame(MainMenu), bg="red").pack()

if __name__ == "__main__":
    app = PongApp()
    app.mainloop()
