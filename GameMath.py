#!/usr/bin/python3

from math import sqrt

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other):
		if type(other) == Vector:
			return Point(self.x + other.x, self.y + other.y)
		raise TypeError("Only a Vector can be added to a Point")

	def __iadd__(self, other):
		self = self + other
		return self

	def __sub__(self, other):
		if type(other) == Vector:
			return Point(self.x - other.x, self.y - other.y)
		if type(other) == Point:
			return Vector(self.x - other.x, self.y - other.y)
		raise TypeError(type(other) + " cannot be subtracted from a Point")

	def __isub__(self, other):
		if type(other) == Vector:
			self = self - other
			return self
		raise TypeError("Point - " + {type(other)}  + " would not return a Point")

class Vector:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.magnitude = sqrt(pow(x, 2) + pow(y, 2))

	def __add__(self, other):
		if type(other) == Vector:
			return Vector(self.x + other.x, self.y + other.y)
		raise TypeError("Only a Vector can be added to another Vector")

	def __radd__(self, other):
		return self + other

	def __iadd__(self, other):
		self = self + other
		return self

	def __sub__(self, other):
		if type(other) == Vector:
			return Vector(self.x - other.x, other.y - self.y)
		raise TypeError("Only a Vector can be subtracted from another Vector")

	def __rsub__(self, other):
		if type(other) == Point:
			return Point(other.x - self.x, other.y - self.y)
		if type(other) == Vector:
			return Vector(other.x - self.x, other.y - self.y)
		raise TypeError("A Vector can only be subtracted from another Vector or a Point")

	def __isub__(self, other):
		if type(other) == Vector:
			self = self - other
			return self
		raise TypeError("Only a Vector can be subtracted from another Vector")

	def __mul__(self, other):
		if type(other) == int or type(other) == float:
			return Vector(self.x * other, self.y * other)
		raise TypeError("Only a number can be multiplied with a Vector")

	def __rmul__(self, other):
		return self * other

	def __imul__(self, other):
		self = self * other
		return self

	def __neg__(self):
		return Vector(-self.x, -self.y)

	def __abs__(self):
		return Vector(abs(self.x), abs(self.y))

	def __invert__(self):
		return -self

	def magnitude(self):
		return sqrt((self.x * self.x) + (self.y * self.y))

	def unitVect(self):
		return Vector(self.x / self.magnitude(), self.y / self.magnitude)
		
class Circle:
	def __init__(self, pos, r):
		if not type(pos) == Point:
			raise TypeError("'pos' must be a Point")
		self.pos = pos
		self.r = r

	def __add__(self, other):
		if type(other) == Vector:
			return Circle(self.pos + other, self.r)
		if type(other) == int or type(other) == float:
			return Circle(self.pos, self.r + other)
		raise TypeError(type(other) + " cannot be added to a Circle")

	def __iadd__(self, other):
		self = self + other
		return self

	def __sub__(self, other):
		if type(other) == Vector:
			return Circle(self.pos - other, self.r)
		if type(other) == int or type(other) == float:
			return Circle(self.pos, self.r - other)
		raise TypeError(type(other) + " cannot be subtracted from a Circle")

	def __isub__(self, other):
		self = self - other
		return self

	def __mul__(self, other):
		if type(other) == int or type(other) == float:
			return Circle(self.pos, self.r * other)
		raise TypeError("Circle cannot be multiplied by " + type(other))

	def __rmul__(self, other):
		return self * other

	def __imul__(self, other):
		self = self * other
		return self

class Rectangle:
	def __init__(self, pos, height, width):
		if not type(pos) == Point:
			raise TypeError("'pos' must be a Point")
		self.pos = pos
		self.height = height
		self.width = width
		self.left = pos.x
		self.right = pos.x + width
		self.top = pos.y
		self.bottom = pos.y + height

	def __add__(self, other):
		if type(other) == Vector:
			return Rectangle(self.pos + other, self.length, self.width)
		raise TypeError(type(other) + " cannot be added to Rectangle")

	def __iadd__(self, other):
		self = self + other
		return self

	def __sub__(self, other):
		if type(other) == Vector:
			return Rectangle(self.pos - other, self.length, self.width)
		raise TypeError(type(other) + " cannot be subtracted from Rectangle")

	def __isub__(self, other):
		self = self - other
		return self

	def __mul__(self, other):
		if type(other) == int or type(other) == float:
			return Rectangle(self.pos, self.length * other, self.width * other)
		raise TypeError("Rectangle cannot be multiplied by " + type(other))

	def __imul__(self, other):
		self = self * other
		return self
