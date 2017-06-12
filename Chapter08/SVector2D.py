# -*- coding: utf-8 -*-
from math import sqrt

class SVector2D(object):
	def __init__(self, a=0.0, b=0.0):
		self._x = a
		self._y = b

		return

	def __add__(self, rhs):
		return SVector2D(self._x+rhs._x, self._y+rhs._y)

	def __sub__(self, rhs):
		return SVector2D(self._x-rhs._x, self._y-rhs._y)

	def __mul__(self, rhs):
		if isinstance(rhs, SVector2D):
			return SVector2D(self._x*rhs._x, self._y*rhs._y)
		else:
			return SVector2D(self._x*rhs, self._y*rhs)

	def __div__(self, rhs):  #这些都可以改写成 return SVector2D(self._x/rhs._x, self._y/rhs._y) if isinstance(rhs, SVector2D) else SVector2D(self._x/rhs, self._y/rhs) 
		if isinstance(rhs, SVector2D):
			return SVector2D(self._x/rhs._x, self._y/rhs._y)
		else:
			return SVector2D(self._x/rhs, self._y/rhs)


def Vec2DLength(v):
	return sqrt(v._x*v._x + v._y*v._y)

def Vec2DNormalize(v):
	vector_length = Vec2DLength(v)
	return SVector2D(v._x/vector_length, v._y/vector_length)

def Vec2DDot(v1, v2):
	return v1._x*v2._x + v1._y*v2._y

def Vec2DSign(v1, v2):
	return 1 if v1._y*v2._x > v1._x*v2._y else -1
