# Multi-frame tkinter application v2.3
import tkinter as tk
import paho.mqtt.client as paho
import Broker


class PongApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(MainMenu)
        client = paho.Client()
        client.on_connect = Broker.on_connect
        client.on_subscribe = Broker.on_subscribe
        client.on_message = Broker.on_message
        client.on_publish = Broker.on_publish
        client.connect("broker.mqttdashboard.com", 1883)
        client.subscribe("broker/groep9")

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

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