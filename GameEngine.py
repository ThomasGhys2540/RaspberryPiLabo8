#!/usr/bin/python3

#import GameMath
from GameMath import Point
from GameMath import Vector
from GameMath import Circle
from GameMath import Rectangle

#import other
import math
import random
from time import sleep
from time import time
from threading import Thread
import paho.mqtt.client as paho

WINDOWHEIGHT = 800
WINDOWWIDTH = 1080

PADDLEHEIGHT = 200
PADDLEWIDTH = 50

BALLSIZE = 50
BALLSTARTSPEED = 5

FPS = 10

PADDLESPEED = 4

class Timer():
	def __init__(self):
		self.prevTime = time()
		self.deltaTime = self.prevTime - time()

	def Update(self):
		self.deltaTime = time() - self.prevTime
		self.prevTime = time()

class Ball(Circle):
	def __init__(self, pos, r, vector = Vector(0, 0)):
		self.vector = vector
		Circle.__init__(self, pos, r)

	def move(self):
		global timer
		self.pos += self.vector * timer.deltaTime

class Paddle(Rectangle):
	def __init__(self, pos, height, width, movement = 0):
		self.movement = movement
		Rectangle.__init__(self, pos, height, width)

	def move(self):
		global timer
		self.pos.y += self.movement * timer.deltaTime

class Game:
	def __init__(self, ball, paddleL, paddleR, fps):
		#GameObjects
		self.ball = ball
		self.paddleL = paddleL
		self.paddleR = paddleR

		#GameVariables
		self.scoreL = 0
		self.scoreR = 0

		#GameState and Connection
		self.state = "lobby"
		self.client = paho.Client()

		self.playersConnected = 0
		self.playersConnectRequested = 0

		#Frequency variables
		self.fps = fps

	def KeepInRange(self, num, low, high):
		if num < low:
			num = low
		if num > high:
			num = high
		return num

	def Collision(self):
		def vertCollision():
			if self.ball.pos.y - self.ball.r <= 0 or self.ball.pos.y + self.ball.r / 2 >= WINDOWHEIGHT:
				self.ball.vector = Vector(self.ball.vector.x, -self.ball.vector.y)

		def horCollision():
			if self.ball.pos.x - self.ball.r <= 0:
				self.scoreR += 1
				print("One Point To gRyfindor!")
				collidedSide()

			if self.ball.pos.x + self.ball.r >= WINDOWWIDTH:
				self.scoreL += 1
				print("One Point To sLytherin!")
				collidedSide()

		def collidedSide():
			self.ball.pos = Point(WINDOWWIDTH / 2 - self.ball.r, WINDOWHEIGHT / 2 - self.ball.r)
			self.ball.vector = Vector(random.randrange(-1, 2, 2) * random.uniform(0.5, 1), random.randrange(-1, 2, 2) * random.uniform(0, 0.5)).unitVect() * BALLSTARTSPEED

		def collPaddles():
			#Enough left to hit paddle
			if self.ball.pos.x - self.ball.r <= PADDLEWIDTH:
				#Center ball above paddle
				if self.ball.pos.y < self.paddleL.pos.y:
					if self.ball.pos.y + self.ball.r >= self.paddleL.pos.y:
						angle = 0
						tempVec = Vector(0, 0)

						if self.ball.vector.y < 0:
							angle = (float(abs((self.paddleL.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r))
						else:
							angle = -(1 - (float(abs((self.paddleL.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r)))

						tempVec = Vector(abs(ball.vector.x), -abs(ball.vector.y))
						tempVec = Vector(tempVec.x * math.cos(angle) - tempVec.y * math.sin(angle), tempVec.x * math.sin(angle) + tempVec.y * math.cos(angle))
						self.ball.vector = tempVec

				#Center paddle under paddle
				elif self.ball.pos.y > self.paddleL.pos.y + PADDLEHEIGHT:
					if self.ball.pos.y - self.ball.r <= self.paddleL.pos.y + PADDLEHEIGHT:
						angle = 0
						tempVec = Vector(0, 0)

						if self.ball.vector.y < 0:
							angle = -(1 - (float(abs((self.paddleL.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r)))
						else:
							angle = (float(abs((self.paddleL.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r))

						tempVec = Vector(abs(ball.vector.x), -abs(ball.vector.y))
						tempVec = Vector(tempVec.x * math.cos(angle) - tempVec.y * math.sin(angle), tempVec.x * math.sin(angle) + tempVec.y * math.cos(angle))
						self.ball.vector = tempVec

				#Center ball in front of paddle
				else:
					angle = (float(abs((self.paddleL.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r))
					tempVec = Vector(abs(ball.vector.x), ball.vector.y)

					if ball.vector.y > 0:
						angle = -angle

					tempVec = Vector(tempVec.x * math.cos(angle) - tempVec.y * math.sin(angle), tempVec.x * math.sin(angle) + tempVec.y * math.cos(angle))
					self.ball.vector = tempVec

			#Enough right to hit paddle
			elif self.ball.pos.x + self.ball.r >= WINDOWWIDTH - PADDLEWIDTH:
				#Center ball above paddle
				if self.ball.pos.y < self.paddleR.pos.y:
					if self.ball.pos.y + self.ball.r >= self.paddleR.pos.y:
				 		angle = 0
				  		tempVec = Vector(0, 0)

						if self.ball.vector.y < 0:
							angle = (float(abs((self.paddleR.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r))
						else:
							angle = -(1 - (float(abs((self.paddleR.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r)))

						tempVec = Vector(abs(ball.vector.x), -abs(ball.vector.y))
						tempVec = Vector(tempVec.x * math.cos(angle) - tempVec.y * math.sin(angle), tempVec.x * math.sin(angle) + tempVec.y * math.cos(angle))
						self.ball.vector = tempVec
				#Center ball under paddle
				elif self.ball.pos.y > self.paddleR.pos.y + PADDLEHEIGHT:
					if self.ball.pos.y - self.ball.r <= self.paddleR.pos.y + PADDLEHEIGHT:
						angle = 0
						tempVec = Vector(0, 0)

						if self.ball.vector.y < 0:
							angle = -(1 - (float(abs((self.paddleR.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r)))
						else:
							angle = (float(abs((self.paddleR.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r))

						tempVec = Vector(abs(ball.vector.x), -abs(ball.vector.y))
						tempVec = Vector(tempVec.x * math.cos(angle) - tempVec.y * math.sin(angle), tempVec.x * math.sin(angle) + tempVec.y * math.cos(angle))
						self.ball.vector = tempVec
				#Center ball in front of paddle
				else:
					angle = (float(abs((self.paddleL.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r))
					tempVec = Vector(abs(ball.vector.x), ball.vector.y)

					if self.ball.vector.y > 0:
						angle = -angle

					tempVec = Vector(tempVec.x * math.cos(angle) - tempVec.y * math.sin(angle), tempVec.x * math.sin(angle) + tempVec.y * math.cos(angle))
					self.ball.vector = tempVec

		vertCollision()
		horCollision()
		collPaddles()

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

		def movePaddle(msg):
			speed = PADDLESPEED
			if msg[2] == '1':
				speed *= 2
			if msg[0] == 'L':
				if msg[1] == 'U':
					self.padlleL.movement = -speed
				elif msg[1] == 'D':
					self.paddleL.movement = speed
				elif msg[1] == 'S':
					self.paddleL.movement = 0
			elif msg[0] == 'R':
				if msg[1] == 'U':
					self.paddleR.movement = -speed
				elif msg[1] == 'D':
					self.paddleR.movement = speed
				elif msg[1] == 'S':
					self.paddleR.movement = 0

		def on_message(client, userdata, msg):
			if self.state == "lobby":
				lobby(str(msg.payload))
			elif self.state == "game":
				movePaddle(str(msg.payload))

		self.client.on_message = on_message

		self.client.connect("84.197.165.225", 667)
		self.client.subscribe("broker/groep9")

		self.client.loop_forever()

	def UpdateClock(self):
		while True:
			sleep(float(1) / self.fps)
			message = "bx:" + str(self.KeepInRange(math.floor(self.ball.pos.x - self.ball.r), 0, WINDOWWIDTH)) + ";"
			message += "by:" + str(self.KeepInRange(math.floor(self.ball.pos.y - self.ball.r), 0, WINDOWHEIGHT)) + ";"
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

		print("Start game")
		self.client.publish("broker/groep9", "Start")

		clock = Thread(target=self.UpdateClock)
		clock.start()

		global timer
		timer.Update()
		
		while self.state == "game":
			sleep(float(1) / self.fps)
			timer.Update()
			self.Collision()
			self.ball.move()
			self.paddleL.move()
			self.paddleR.move()

ballPos = Point(WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
LPaddlePos = Point(0, (WINDOWHEIGHT / 2) - (PADDLEHEIGHT / 2))
RPaddlePos = Point(WINDOWWIDTH - PADDLEWIDTH, (WINDOWHEIGHT / 2) - (PADDLEHEIGHT / 2))

startVector = Vector(random.randrange(-1, 2, 2) * random.uniform(0.5, 1), random.randrange(-1, 2, 2) * random.uniform(0, 0.5)).unitVect() * BALLSTARTSPEED

ball = Ball(ballPos, BALLSIZE / 2, startVector)
LPaddle = Paddle(LPaddlePos, PADDLEHEIGHT, PADDLEWIDTH)
RPaddle = Paddle(RPaddlePos, PADDLEHEIGHT, PADDLEWIDTH)

timer = Timer()

game = Game(ball, LPaddle, RPaddle, FPS)
game.startGame()
