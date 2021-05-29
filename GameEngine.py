
#!/usr/bin/python3

#import GameMath
from GameMath import Point
from GameMath import Vector
from GameMath import Circle
from GameMath import Rectangle

#import other
import paho.mqtt.client as paho
from threading import Thread
from random import random

WINDOWWIDTH = 1080
WINDOWHEIGHT = 800

PADDLEHEIGHT = 200
PADDLEWIDTH = 50

BALLSIZE = 50
BALLSTARTSPEED = 5

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

class Game:
	def __init__(self, ball, paddleL, paddleR):
		self.ball = ball
		self.paddleL = paddleL
		self.paddleR = paddleR
		self.playersConnected = 0
		self.state = "lobby"
		self.client = paho.Client()

	def MQTT(self):
		playersConnectRequested = 0;

		def lobby(msg):
			if msg == "Connect":
				if playersConnectRequested == 0:
					client.publish("broker/groep9", "PL")
				else:
					client.publish("broker/groep9", "PR")
				playersConnectRequested += 1
			elif msg == "Connected":
				self.playersConnected += 1
		
		def on_message(client, userdata, msg):
			print(str(client) + "\n" + str(userdata))
			
			if self.state == "lobby":
				lobby(str(msg.payload))

		self.client.on_connect = on_connect
		self.client.on_subscribe = on_subscribe
		self.client.on_message = on_message

		self.client.connect("84.197.165.225", 667)
		self.client.subscribe("broker/groep9")

		while self.playersConnected < 2:
			pass

	def startGame(self):
		mqtt = Thread(target=self.MQTT)
		mqtt.start()
		while not self.state == "done":
			pass
		
ballPos = Point(WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
LPaddlePos = Point(0, (WINDOWHEIGHT / 2) - (PADDLEHEIGHT / 2))
RPaddlePos = Point(WINDOWWIDTH - PADDLEWIDTH, (WINDOWHEIGHT / 2) - (PADDLEHEIGHT / 2))

startVector = Vector(random(), random()).unitVect() * BALLSTARTSPEED

ball = Ball(ballPos, BALLSIZE / 2, startVector)
LPaddle = Rectangle(LPaddlePos, PADDLEHEIGHT, PADDLEWIDTH)
RPaddle = Rectangle(RPaddlePos, PADDLEHEIGHT, PADDLEWIDTH)

game = Game(ball, LPaddle, RPaddle)
game.startGame()
