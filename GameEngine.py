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
BALLSTARTSPEED = 100

FPS = 10

PADDLESPEED = 90

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
		self.paddleHitsL = 0
		self.paddleHitsR = 0

		self.paddleHit = False

		self.round = 1

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
				self.scoreR += self.paddleHitsR * 5
				self.paddleHitsL = 0
				self.paddleHitsR = 0
				self.paddleHit = True
				self.round += 1

				print("One Point To gRyfindor!")
				collidedSide()

			if self.ball.pos.x + self.ball.r >= WINDOWWIDTH:
				self.scoreL += self.paddleHitsL * 5
				self.paddleHitsL = 0
				self.paddleHitsR = 0
				self.paddleHit = True
				self.round += 1
 
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
						if not self.paddleHit:
							self.paddleHitsL += 1
							self.paddleHit = True

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
						if not self.paddleHit:
							self.paddleHitsL += 1
							self.paddleHit = True

						angle = 0
						tempVec = Vector(0, 0)

						if self.ball.vector.y < 0:
							angle = (1 - (float(abs((self.paddleL.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r)))
						else:
							angle = -(float(abs((self.paddleL.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r))

						tempVec = Vector(abs(ball.vector.x), -abs(ball.vector.y))
						tempVec = Vector(tempVec.x * math.cos(angle) - tempVec.y * math.sin(angle), tempVec.x * math.sin(angle) + tempVec.y * math.cos(angle))
						self.ball.vector = tempVec
					else:
						self.paddleHit = False

				#Center ball in front of paddle
				else:
					if not self.paddleHit:
						self.paddleHitsL += 1
						self.paddleHit = True

					tempVec = Vector(abs(ball.vector.x), ball.vector.y)
					self.ball.vector = tempVec

			#Enough right to hit paddle
			elif self.ball.pos.x + self.ball.r >= WINDOWWIDTH - PADDLEWIDTH:
				#Center ball above paddle
				if self.ball.pos.y < self.paddleR.pos.y:
					if self.ball.pos.y + self.ball.r >= self.paddleR.pos.y:
						if not self.paddleHit:
							self.paddleHitsL += 1
							self.paddleHit = True

						angle = 0
						tempVec = Vector(0, 0)

						if self.ball.vector.y < 0:
							angle = (float(abs((self.paddleR.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r))
						else:
							angle = -(1 - (float(abs((self.paddleR.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r)))

						tempVec = Vector(-abs(ball.vector.x), -abs(ball.vector.y))
						tempVec = Vector(tempVec.x * math.cos(angle) - tempVec.y * math.sin(angle), tempVec.x * math.sin(angle) + tempVec.y * math.cos(angle))
						self.ball.vector = tempVec
					else:
						paddleHit = False
				#Center ball under paddle
				elif self.ball.pos.y > self.paddleR.pos.y + PADDLEHEIGHT:
					if self.ball.pos.y - self.ball.r <= self.paddleR.pos.y + PADDLEHEIGHT:
						if not self.paddleHit:
							self.paddleHitsL += 1
							self.paddleHit = True
						angle = 0
						tempVec = Vector(0, 0)

						if self.ball.vector.y < 0:
							angle = -(1 - (float(abs((self.paddleR.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r)))
						else:
							angle = (float(abs((self.paddleR.pos.y + PADDLEHEIGHT / 2) - self.ball.pos.y)) / (PADDLEHEIGHT / 2 + self.ball.r))

						tempVec = Vector(-abs(ball.vector.x), abs(ball.vector.y))
						tempVec = Vector(tempVec.x * math.cos(angle) - tempVec.y * math.sin(angle), tempVec.x * math.sin(angle) + tempVec.y * math.cos(angle))
						self.ball.vector = tempVec
				#Center ball in front of paddle
				else:
					if not self.paddleHit:
						self.paddleHitsL += 1
						self.paddleHit = True
					tempVec = Vector(-abs(ball.vector.x), ball.vector.y)
					self.ball.vector = tempVec
			else:
				self.paddleHit = False

		vertCollision()
		horCollision()
		collPaddles()

	def MQTT(self):
		def lobby(msg):
			if "Connect" in msg and "Connected" not in msg:
				print("Answering connection request")
				if self.playersConnectRequested == 0:
					self.client.publish("broker/groep9", "PL")
				else:
					self.client.publish("broker/groep9", "PR")
				self.playersConnectRequested += 1
			elif "Connected" in msg:
				self.playersConnected += 1
				print(str(self.playersConnected) + " players connected")

		def movePaddle(msg):
			speed = PADDLESPEED
			if '1' in msg:
				speed *= 2
			if 'L' in msg:
				if 'U' in msg:
					self.padlleL.movement = -speed
				elif 'D' in msg:
					self.paddleL.movement = speed
				elif 'S' in msg:
					self.paddleL.movement = 0
			elif 'R' in msg:
				if 'U' in msg:
					self.paddleR.movement = -speed
				elif 'D' in msg:
					self.paddleR.movement = speed
				elif 'S' in msq:
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
		while self.state is "game":
			sleep(float(1) / self.fps)
			message = "bx:" + str(self.KeepInRange(math.floor(self.ball.pos.x - self.ball.r), 0, WINDOWWIDTH)) + ";"
			message += "by:" + str(self.KeepInRange(math.floor(self.ball.pos.y - self.ball.r), 0, WINDOWHEIGHT)) + ";"
			message += "ly:" + str(self.KeepInRange(math.floor(self.paddleL.pos.y), 0, WINDOWHEIGHT)) + ";"
			message += "ry:" + str(self.KeepInRange(math.floor(self.paddleR.pos.y), 0, WINDOWHEIGHT)) + ";"
			message += "ls:" + str(self.scoreL) + ";"
			message += "rs:" + str(self.scoreR)
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
			if self.round is 10:
				self.state = "victory"

		sleep(float(1) / self.fps)

		message = "bx:" + str(self.KeepInRange(math.floor(self.ball.pos.x - self.ball.r), 0, WINDOWWIDTH)) + ";"
		message += "by:" + str(self.KeepInRange(math.floor(self.ball.pos.y - self.ball.r), 0, WINDOWHEIGHT)) + ";"
		message += "ly:" + str(self.KeepInRange(math.floor(self.paddleL.pos.y), 0, WINDOWHEIGHT)) + ";"
		message += "ry:" + str(self.KeepInRange(math.floor(self.paddleR.pos.y), 0, WINDOWHEIGHT)) + ";"
		message += "ls:" + str(self.scoreL) + ";"
		message += "rs:" + str(self.scoreR) + ";"
		message += "r:" + str(self.round) + ";"

		self.client.publish("broker/groep9", message)
		if self.scroreL > self.scoreR:
			self.client.publish("broker/groep9", "WL")
		else:
			self.client.publish("broker/groep9", "WR")

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
