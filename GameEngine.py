
#!/usr/bin/python3

#import GameMath
from GameMath import Point
from GameMath import Vector
from GameMath import Circle
from GameMath import Rectangle

#import other
import paho.mqtt.client as paho
from threading import Thread

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
		super(Ball, self).__init__(pos, r)

class Game:
	def __init__(self, ball: Ball, paddleL: Rectangle, paddleR: Rectangle):
		self.ball = ball
		self.paddleL = paddleL
		self.paddleR = paddleR
		self.p1Connected = false
		self.p2Connected = false

	def MQTT():
		client = paho.Client()

		client.connect("")
		def lobby():
			

ballPos = Point(WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
LPaddlePos = Point(0, (WINDOWHEIGHT / 2) - (PADDLEHEIGHT / 2))
RPaddlePos = Point(WINDOWWIDTH - PADDLEWIDTH, (WINDOWHEIGHT / 2) - (PADDLEHEIGHT / 2))

startVector = Vector(random, random).unitVect() * BALLSTARTSPEED

ball = Ball(ballPos, BALLWIDTH / 2, startVector)
LPaddle = Rectangle(LPaddlePos, PADDLEHEIGHT, PADDLEWIDTH)
RPaddle = Rectangle(RPaddlePos, PADDLEHEIGHT, PADDLEWIDTH)
