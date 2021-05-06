#!/usr/bin/python3

#import GameMath
import Point from GameMath as Point
import Vector from GameMath as Vector
import Circle from GameMath as Circle
import Rectangle from GameMath as Rectangle

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
		if ball.pos - Point(paddle.right, paddle.bottom) < ball.r:
			xFact = 0
			if ball.pos.x > paddel.right:
				xFact = 1
			else:
				xFact = -1
			yDif = float(ball.pos.y - paddle.bottom)
			ball.vector = Vector(xFact * (1 - (yDif / ball.r)) * abs(ball.vector.x), (yDif / ball.r) * abs(ball.vector.y))
	#Ball Y above paddle range
	elif ball.pos.y < paddle.top:
		if ball.pos - Point(paddle.right, paddle.top) < ball.r:
			xFact = 0
			if ball.pos.x > paddle.right:
				xFact = 1
			else:
				xFact = -1
			yDif = float(paddle.top - ball.pos.y)
			ball.vector = Vector(xFact * (1 - (yDif / ball.r)) * abs(ball.vector.x), -(yDif / ball.r) * abs(ball.vector.y))

class Ball(Circle):
	def __oninit__(pos, r, vector = Vector(0, 0)):
		super().__init__(pos, r)
		self.vector = vector
