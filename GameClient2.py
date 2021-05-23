# Multi-frame tkinter application v2.3
import tkinter as tk

class PongApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(MainMenu)

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
        tk.Frame.__init__(self, master, bg="black")
        
        tk.Button(self, text="End the Game!", command=lambda: master.switch_frame(VictoryScreen), bg="red").pack()

class VictoryScreen(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="black")
        tk.Label(self, text="This is the end there is nothing beyond here", bg="black", fg="white").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to the Main menu", command=lambda: master.switch_frame(MainMenu), bg="red").pack()

if __name__ == "__main__":
    app = PongApp()
    app.mainloop()