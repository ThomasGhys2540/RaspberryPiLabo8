#!/usr/bin/python3

#import GameMath
from GameMath import Point
from GameMath import Vector
from GameMath import Circle
from GameMath import Rectangle

#import other
import paho.mqtt.client as paho
import math
from threading import Thread
import random
from time import sleep

WINDOWWIDTH = 1080
WINDOWHEIGHT = 800

PADDLEHEIGHT = 200
PADDLEWIDTH = 50

BALLSIZE = 50
BALLSTARTSPEED = 5

FPS = 10

invertOrNotToInvertThatsTheQuestion = [-1, 1]

def CheckBallCollision(ball, paddle):
	#Ball Y in paddle range
	if ball.pos.y > paddle.top and ball.pos.y < paddle.bottom:
		if ball.pos.x > paddle.left:
			if ball.pos.x - ball.r <= paddle.right:
				ball.vector = Vector(abs(ball.vector.x), ball.vector.y)
		else:
			if ball.pos.x + ball.r >= paddle.left:
				ball.vector = Vector(-abs(ball.vector.x), ball.vector.y)
	#Ball Y under paddle range
	elif ball.pos.y > paddle.bottom:
		if (ball.pos - Point(paddle.right, paddle.bottom)).magnitude < ball.r:
			xFact = 0
			if ball.pos.x > paddel.right:
				xFact = 1
			else:
				xFact = -1
			yDif = float(ball.pos.y - paddle.bottom)
			ball.vector = Vector(xFact * (1 - (yDif / ball.r)) * abs(ball.vector.x), (yDif / ball.r) * abs(ball.vector.y))
	#Ball Y above paddle range
	elif ball.pos.y < paddle.top:
		if (ball.pos - Point(paddle.right, paddle.top)).magnitude < ball.r:
			xFact = 0
			if ball.pos.x > paddle.right:
				xFact = 1
			else:
				xFact = -1
			yDif = float(paddle.top - ball.pos.y)
			ball.vector = Vector(xFact * (1 - (yDif / ball.r)) * abs(ball.vector.x), -(yDif / ball.r) * abs(ball.vector.y))

class Ball(Circle):
	def __init__(self, pos, r, vector = Vector(0, 0)):
		self.vector = vector
		Circle.__init__(self, pos, r)

	def move(self):
		self.pos += self.vector

class Game:
	def __init__(self, ball, paddleL, paddleR, fps):
		self.ball = ball
		self.paddleL = paddleL
		self.paddleR = paddleR
		self.playersConnected = 0
		self.state = "lobby"
		self.client = paho.Client()
		self.playersConnectRequested = 0
		self.fps = fps
		self.scoreL = 0
		self.scoreR = 0

	def KeepInRange(self, num, low, high):
		if num < low:
			num = low
		if num > high:
			num = high
		return num
	
	def Collision(self):
		def vertCollision():
			if self.ball.pos.y - self.ball.r / 2 <= 0 or self.ball.pos.y + self.ball.r / 2 >= WINDOWHEIGHT:
				self.ball.vector = Vector(self.ball.vector.x, -self.ball.vector.y)

		def horCollision():
			if self.ball.pos.x - self.ball.r / 2 <= 0:
				self.scoreR += 1
				print("One Point To gRyfindor!")
				collidedSide()
				
			if self.ball.pos.x + self.ball.r / 2 >= WINDOWWIDTH:
				self.scoreL += 1
				print("One Point To sLytherin!")
				collidedSide()

		def collidedSide():
			self.ball.pos = Point(WINDOWWIDTH / 2 - self.ball.r / 2, WINDOWHEIGHT / 2 - self.ball.r / 2)
			self.ball.vector = Vector(random.randrange(-1, 2, 2) * random.uniform(0.5, 1), random.randrange(-1, 2, 2) * random.uniform(0, 0.5)).unitVect() * BALLSTARTSPEED
		
		vertCollision()
		horCollision()

	def MQTT(self):
		def lobby(msg):
			if msg == "Connect":
				print("Answering connection request")
				if self.playersConnectRequested == 0:
					self.client.publish("broker/groep9", "PL")
				else:
					self.client.publish("broker/groep9", "PR")
				self.playersConnectRequested += 1
			elif msg == "Connected":
				self.playersConnected += 1
				print(str(self.playersConnected) + " players connected")

		def on_message(client, userdata, msg):
			if self.state == "lobby":
				lobby(str(msg.payload))
		
		self.client.on_message = on_message

		self.client.connect("84.197.165.225", 667)
		self.client.subscribe("broker/groep9")

		self.client.loop_forever()

	def UpdateClock(self):
		while True:
			sleep(float(1) / self.fps)
			message = "bx:" + str(self.KeepInRange(math.floor(self.ball.pos.x - self.ball.r / 2), 0, WINDOWWIDTH)) + ";"
			message += "by:" + str(self.KeepInRange(math.floor(self.ball.pos.y - self.ball.r / 2), 0, WINDOWHEIGHT)) + ";"
			message += "ls:" + str(self.scoreL) + ";"
			message += "ly:" + str(self.KeepInRange(math.floor(self.paddleL.pos.y), 0, WINDOWHEIGHT)) + ";"
			message += "rs:" + str(self.scoreR) + ";"
			message += "ry:" + str(self.KeepInRange(math.floor(self.paddleR.pos.y), 0, WINDOWHEIGHT))
			self.client.publish("broker/groep9", message)
		
	def startGame(self):
		mqtt = Thread(target=self.MQTT)
		mqtt.start()
		
		while self.state == "lobby":
			if self.playersConnected == 2:
				self.state = "game"

		clock = Thread(target=self.UpdateClock)
		clock.start()

		while self.state == "game":
			sleep(float(1) / self.fps)
			self.Collision()
			self.ball.move() 
			
ballPos = Point(WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
LPaddlePos = Point(0, (WINDOWHEIGHT / 2) - (PADDLEHEIGHT / 2))
RPaddlePos = Point(WINDOWWIDTH - PADDLEWIDTH, (WINDOWHEIGHT / 2) - (PADDLEHEIGHT / 2))

startVector = Vector(random.randrange(-1, 2, 2) * random.uniform(0.5, 1), random.randrange(-1, 2, 2) * random.uniform(0, 0.5)).unitVect() * BALLSTARTSPEED

ball = Ball(ballPos, BALLSIZE / 2, startVector)
LPaddle = Rectangle(LPaddlePos, PADDLEHEIGHT, PADDLEWIDTH)
RPaddle = Rectangle(RPaddlePos, PADDLEHEIGHT, PADDLEWIDTH)

game = Game(ball, LPaddle, RPaddle, FPS)
game.startGame()
