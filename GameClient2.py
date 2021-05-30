#!/usr/bin/python3
# Multi-frame tkinter application v2.3
import tkinter as tk
import paho.mqtt.client as paho
import Broker
from threading import Thread
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN)
GPIO.setup(5, GPIO.IN)
GPIO.setup(7, GPIO.IN)

class PongApp(tk.Tk):
    def __init__(self):
        print("lkdqjf")
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(MainMenu)
        self.paddle = " "
        self.direction = "S"
        self.speed = 0
        self.askedSide = False
        self.gameStarted = False
        self.GUIStarted = False
        self.BallPrevPosX = 0
        self.BallPrevPosY = 0
        self.BallNewPosX = 0
        self.BallNewPosY = 0
        self.BallNewPosBottomX = self.BallNewPosX + 50
        self.BallNewPosBottomY = self.BallNewPosY + 50
        self.LPaddlePrevPosY = 0
        self.RPaddlePrevPosY = 0
        self.LPaddleNewPosY = 0
        self.RPaddleNewPosY = 0
        self.LPaddleNewPosBottomY = self.LPaddleNewPosY + 200
        self.RPaddleNewPosBottomY = self.RPaddleNewPosY + 200
        self.RScore = 0
        self.Lscore = 0
        
        self.canvas = tk.Canvas(self, bg="black", width=0, height=0)
        self.LeftPaddle = self.canvas.create_rectangle(0, 0 , 0, 0, fill="white")
        self.RightPaddle = self.canvas.create_rectangle(0, 0, 0, 0, fill="red")
        self.Ball = self.canvas.create_oval(0, 0 0, master.BallNewPosBottomY, fill="blue")
        self.canvas.pack()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def MQTT(self):
        print('ldkqsjfl')
        def on_message(client, callback, msg):
            if not self.gameStarted:
                if self.askedSide and str(msg.payload) is not "b'Connect'":
                    print("test")
                    paddle = str(str(msg.payload)[1])
                    print(str(msg.payload))
                    self.askedSide = False
                    client.publish("broker/groep9", "Connected")
                elif str(msg.payload) == "b'Start'":
                    self.gameStarted = True
                    print("has started")
            else:
                data = str(msg.payload)
                list_data = data.split(';')
                self.BallPrevPosX = self.BallNewPosX
                update = list_data[0].split(':')[1]
                self.BallNewPosX = int(update.split('.')[0])
                self.BallPrevPosY = self.BallNewPosY
                update = list_data[1].split(':')[1]
                self.BallNewPosY = int(update.split('.')[0])
                update = list_data[2].split(':')[1]
                self.Lscore = int(update.split('.')[0])
                self.LPaddlePrevPosY = self.LPaddleNewPosY
                update = list_data[3].split(':')[1]
                self.LPaddleNewPosY = int(update.split('.')[0])
                update = list_data[4].split(':')[1]
                self.Rscore = int(update.split('.')[0])
                self.RPaddlePrevPosY = self.RPaddleNewPosY
                update = list_data[5].split(':')[1]
                self.RPaddleNewPosY = int(update.split('.')[0])
                master = self
                GameScreen.Movement(master)
                
        def UpdateBroker():
            message = self.paddle + self.direction + str(speed)
            client.publish("broker/groep9", message)
        
        def upButton(channel):
            if self.direction is "U":
                self.direction = "S"
            else:
                self.direction = "U"
            UpdateBroker()
            
        def downButton(channel):
            if self.direction is "D":
                self.direction = "S"
            else:
                self.direction = "D"
            UpdateBroker()

        def SpeedButtonSwitch(channel):
            if speed == 0:
                speed = 1
            else:
                speed = 0
            UpdateBroker()
        
        def WaitFor():
            client.loop_forever()
            
        client = paho.Client()
        client.on_message = on_message
        client.connect("84.197.165.225", port=667)
        client.subscribe("broker/groep9")

        while not self.GUIStarted:
            #print("WaitingForStart")
            pass

        client.publish("broker/groep9", "Connect")
        self.askedSide = True
        job_Loop = Thread(target = WaitFor)
        job_Loop.start()

        while not self.gameStarted:
            #print("MQTT Waiting")
            pass

        GPIO.add_event_detect(3, GPIO.BOTH, callback=upButton, bouncetime=300)

        GPIO.add_event_detect(5, GPIO.BOTH, callback=downButton, bouncetime=300)

        GPIO.add_event_detect(7, GPIO.RISING, callback=SpeedButtonSwitch, bouncetime=300)
        
        self.switch_frame(GameScreen)
        print("I wonder why")
        
        while self.gamestarted:
            print()
        GPIO.cleanup()

class MainMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="black")
        tk.Label(self, text="Welcome to the Main Menu", bg="black", fg="white").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Start Game", command=lambda: master.switch_frame(GameScreen), bg="red").pack()
        self.job = Thread(target=master.MQTT)
        print("sdl")
        self.job.start()

class GameScreen(tk.Frame):      
    def __init__(self, master):
        master.GUIStarted = True

        while not master.gameStarted:
            #print("GUI Waiting")
            pass
        
        tk.Frame.__init__(self, master, bg="black")
        self.canvas = tk.Canvas(master, bg="black", width=1080, height=800)
        self.LeftPaddle = self.canvas.create_rectangle(0, master.LPaddleNewPosY , 50, master.LPaddleNewPosBottomY, fill="white")
        self.RightPaddle = self.canvas.create_rectangle(1030, master.RPaddleNewPosY, 1080, master.RPaddleNewPosBottomY, fill="red")
        self.Ball = self.canvas.create_oval(master.BallNewPosX, master.BallNewPosY, master.BallNewPosBottomX, master.BallNewPosBottomY, fill="blue")
        self.canvas.pack()
        tk.Button(self, text="End the Game!", command=lambda: master.switch_frame(VictoryScreen), bg="red").pack()      
        
    def Movement(master):
        self.LPY = master.LPaddlePrevPosY - master.LPaddleNewPosY
        self.RPY = master.RPaddlePrevPosY - master.RPaddleNewPosY
        self.BPX = master.BallPrevPosX - master.BallNewPosX
        self.BPY = master.BallPrevPosY - master.BallNewPosY
        self.canvas.move(self.LeftPaddle, 0, self.LPY)
        self.canvas.move(self.RightPaddle, 0, self.RPY)
        self.canvas.move(self.Ball, self.BPX, self.BPY)

class VictoryScreen(tk.Frame):
    def __init__(master):
        tk.Frame.__init__(self, master, bg="black")
        tk.Label(self, text="This is the end there is nothing beyond here", bg="black", fg="white").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to the Main menu", command=lambda: master.switch_frame(MainMenu), bg="red").pack()

if __name__ == "__main__":
    app = PongApp()
    app.mainloop()
