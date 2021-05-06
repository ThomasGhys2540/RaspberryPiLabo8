#!/usr/bin/python3

class Point:
	def __init__(x, y)
		self.x = x
		self.y = y

class Ball:
	def __init__(pos, r)
		if not isinstance(pos, Point):
			raise TypeError("pos must be a Point")
		self.pos = pos
		self.r = r

class Paddle:
	def __init__(pos, length)
		if not isinstance(pos, Point):
			raise TypeError("pos must be a Point")
		self.pos = pos
		self.length = length
