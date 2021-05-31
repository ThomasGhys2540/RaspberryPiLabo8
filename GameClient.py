#!/usr/bin/python3
# Multi-frame tkinter application v2.3
import tkinter as tk
import paho.mqtt.client as paho
import Broker
from threading import Thread
import RPi.GPIO as GPIO
from time import sleep

up = 3
down = 5
speed = 7

playerledl = 33
playerledr = 35
startled = 37

GPIO.setmode(GPIO.BCM)

GPIO.setup(up, GPIO.IN)
GPIO.setup(down, GPIO.IN)
GPIO.setup(speed, GPIO.IN)

GPIO.setup(startled, GPIO.OUT)
GPIO.setup(playerledl, GPIO.OUT)
GPIO.setup(playerledr, GPIO.OUT)

class PongApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.gameStarted = False
        self.askedSide = False
        self.PlayerPaddle = "*"
        
        self.BallPrevPosX = 0
        self.BallPrevPosY = 0
        self.BallNewPosX = 515
        self.BallNewPosY = 375
        self.BallNewPosBottomX = 565
        self.BallNewPosBottomY = 425
        
        self.LPaddlePrevPosY = 0
        self.LPaddleNewPosY = 300
        self.LPaddleNewPosBottomY = 500
        
        self.RPaddlePrevPosY = 0
        self.RPaddleNewPosY = 300
        self.RPaddleNewPosBottomY = 500
        
        self.ScoreL = 0
        self.ScoreR = 0
        
        for F in (MainMenu, GameScreen, VictoryScreen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.ChangeScreen(MainMenu)
    
    def ChangeScreen(self, X):
        frame = self.frames[X]
        frame.tkraise()
    
    def MQTT(self):
        def on_message(client, userdata, msg):
            if not self.gameStarted:
                print("Game hasn't started yet")
                
                if self.askedSide and not "Connect" in str(msg.payload):
                    print("Has received a side")
                    
                    self.PlayerPaddle = str(msg.payload)
                    
                    if "PR" in self.PlayerPaddle:
                        self.PlayerPaddle = "PR"
                        
                        GPIO.OUTPUT(playerledl, GPIO.LOW)
                        GPIO.OUTPUT(playerledr, GPIO.HIGH)
                    elif "PL" in self.PlayerPaddle:
                        self.PlayerPaddle = "PL"
                        
                        GPIO.OUTPUT(playerledl, GPIO.LOW)
                        GPIO.OUTPUT(playerledr, GPIO.HIGH)
                    
                    print(self.PlayerPaddle)
                    
                    client.publish("broker/groep9", "Connected")
                    self.askedSide = False
                    
                elif "Start" in str(msg.payload):
                    print("Game will start now")
                    
                    for x in range (3):
                        GPIO.OUTPUT(startled, GPIO.HIGH)
                        time.sleep(100)
                        GPIO.OUTPUT(startled, GPIO.LOW)
                        time.sleep(100)
                    
                    self.gameStarted = True
                    
                    self.frames[GameScreen].InitialDraw()
                    
            elif self.ScoreL is 10 or self.ScoreR is 10:
                self.ChangeScreen(VictoryScreen)
            else:
                print("Game is playing")
                
                data = str(msg.payload)
                print(data)
                list_data = data.split(';')
                
                self.BallPrevPosX = self.BallNewPosX
                update = list_data[0].split(':')[1]
                self.BallNewPosX = int(update.split('.')[0])
                
                self.BallPrevPosY = self.BallNewPosY
                update = list_data[1].split(':')[1]
                self.BallNewPosY = int(update.split('.')[0])
                
                self.BallNewPosBottomX = self.BallNewPosX + 50
                self.BallNewPosBottomY = self.BallNewPosY + 50
                
                self.LPaddlePrevPosY = self.LPaddleNewPosY
                update = list_data[2].split(':')[1]
                self.LPaddleNewPosY = int(update.split('.')[0])
                
                self.LPaddleNewPosBottomY = self.LPaddleNewPosY + 200
                
                self.RPaddlePrevPosY = self.RPaddleNewPosY
                update = list_data[3].split(':')[1]
                self.RPaddleNewPosY = int(update.split('.')[0])
                
                self.RPaddleNewPosBottomY = self.RPaddleNewPosY + 200
                
                update = list_data[4].split(':')[1]
                self.ScoreL = int(update)
                
                update = list_data[5].split(':')[1]
                self.ScoreR = int(update.split('\'')[0])
                
                print("Ball: " + str(self.BallNewPosX) + ", " + str(self.BallNewPosY))
                self.frames[GameScreen].Movement()
        
        client = paho.Client()
        client.on_message = on_message
        client.connect("84.197.165.225", port=667)
        client.subscribe("broker/groep9")
        
        client.publish("broker/groep9", "Connect")
        self.askedSide = True
        
        client.loop_forever()

    def StartGame(self):
        self.ChangeScreen(GameScreen)
        
        self.StartMQTT = Thread(target = self.MQTT)
        self.StartMQTT.start()
        
        
class MainMenu(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        tk.Label(self, text="Welcome to the Main Menu", bg="black", fg="white").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Start Game", command=lambda: controller.StartGame(), bg="red").pack(side="bottom", fill="x", pady=10)
        
        print("MainMenu has been succesfully initialised")

class GameScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="black")
        self.controller = controller
        self.master = master
        
        print("GameScreen has been succesfully initialised")
        
    def InitialDraw(self):
        self.canvas = tk.Canvas(self.controller, bg="black", width=1080, height=800)
        self.LPaddle = self.canvas.create_rectangle(0, self.controller.LPaddleNewPosY, 50, self.controller.LPaddleNewPosBottomY, fill="white")
        self.RPaddle = self.canvas.create_rectangle(1030, self.controller.RPaddleNewPosY, 1080, self.controller.RPaddleNewPosBottomY, fill="white")
        self.Ball = self.canvas.create_oval(self.controller.BallNewPosX, self.controller.BallNewPosY, self.controller.BallNewPosBottomX, self.controller.BallNewPosBottomY, fill="white")
        self.canvas.pack(side="top")
    
    def Movement(self):
        self.BallX = self.controller.BallNewPosX - self.controller.BallPrevPosX
        self.BallY = self.controller.BallNewPosY - self.controller.BallPrevPosY
        self.canvas.move(self.Ball, self.BallX, self.BallY)
        
        self.LPaddleY = self.controller.LPaddleNewPosY - self.controller.LPaddlePrevPosY
        self.canvas.move(self.controller.LPaddle, 0, self.LPaddleY)
        
        self.RPaddleY = self.controller.RPaddleNewPosY - self.controller.RPaddlePrevPosY
        self.canvas.move(self.controller.RPaddle, 0, self.RPaddleY)

class VictoryScreen(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg="black")
        self.controller = controller
        tk.Label(self, text="Welcome to the Victory Menu", bg="black", fg="white").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Main Menu", command=lambda: controller.ChangeScreen(MainMenu), bg="red").pack()
        print("VictoryScreen has been succesfully initialised")
        
if __name__ == "__main__":
    app = PongApp()
    app.mainloop()
