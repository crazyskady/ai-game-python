# -*- coding: utf-8 -*-
import math
# Actually, use numpy is more better, but for study purpose, we write it again here.
from numpy import *
class SPoint(object):
	def __init__(self, a=0.0, b=0.0):
		self._x = a
		self._y = b

class S2DMatrix_Old(object):
	def __init__(self):
		self._2DMatrix = [[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]]
		return

	def show(self):
		for i in xrange(len(self._2DMatrix)):
			lineStr = ""
			for j in xrange(len(self._2DMatrix[i])):
				lineStr += str(self._2DMatrix[i][j]) + ", "
			print lineStr

class C2DMatrix_Old(object):
	def __init__(self):
		self._Matrix = S2DMatrix()

		self.Identity()
		return

	def Identity(self):
		self._Matrix._2DMatrix = [[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0]]
		return

	def S2DMatrixMultiply(self, mIn):
		temp = S2DMatrix()
		selfMatrix = self._Matrix._2DMatrix
		temp._2DMatrix[0][0] = selfMatrix[0][0]*mIn._2DMatrix[0][0] + selfMatrix[0][1]*mIn._2DMatrix[1][0] + selfMatrix[0][2]*mIn._2DMatrix[2][0]
		temp._2DMatrix[0][1] = selfMatrix[0][0]*mIn._2DMatrix[0][1] + selfMatrix[0][1]*mIn._2DMatrix[1][1] + selfMatrix[0][2]*mIn._2DMatrix[2][1]
		temp._2DMatrix[0][2] = selfMatrix[0][0]*mIn._2DMatrix[0][2] + selfMatrix[0][1]*mIn._2DMatrix[1][2] + selfMatrix[0][2]*mIn._2DMatrix[2][2]

		temp._2DMatrix[1][0] = selfMatrix[1][0]*mIn._2DMatrix[0][0] + selfMatrix[1][1]*mIn._2DMatrix[1][0] + selfMatrix[1][2]*mIn._2DMatrix[2][0]
		temp._2DMatrix[1][1] = selfMatrix[1][0]*mIn._2DMatrix[0][1] + selfMatrix[1][1]*mIn._2DMatrix[1][1] + selfMatrix[1][2]*mIn._2DMatrix[2][1]
		temp._2DMatrix[1][2] = selfMatrix[1][0]*mIn._2DMatrix[0][2] + selfMatrix[1][1]*mIn._2DMatrix[1][2] + selfMatrix[1][2]*mIn._2DMatrix[2][2]

		temp._2DMatrix[2][0] = selfMatrix[2][0]*mIn._2DMatrix[0][0] + selfMatrix[2][1]*mIn._2DMatrix[1][0] + selfMatrix[2][2]*mIn._2DMatrix[2][0]
		temp._2DMatrix[2][1] = selfMatrix[2][0]*mIn._2DMatrix[0][1] + selfMatrix[2][1]*mIn._2DMatrix[1][1] + selfMatrix[2][2]*mIn._2DMatrix[2][1]
		temp._2DMatrix[2][2] = selfMatrix[2][0]*mIn._2DMatrix[0][2] + selfMatrix[2][1]*mIn._2DMatrix[1][2] + selfMatrix[2][2]*mIn._2DMatrix[2][2]

		self._Matrix = temp
		return

	def Translate(self, x, y):
		mat = S2DMatrix()
		mat._2DMatrix = [[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[x, y, 1.0]]

		self.S2DMatrixMultiply(mat)
		return

	def Scale(self, xScale, yScale):
		mat = S2DMatrix()
		mat._2DMatrix = [[xScale, 0.0, 0.0],[0.0, yScale, 0.0],[0.0, 0.0, 1.0]]

		self.S2DMatrixMultiply(mat)
		return

	def Rotate(self, rot):
		mat = S2DMatrix()
		Sin = math.sin(rot)
		Cos = math.cos(rot)
		mat._2DMatrix = [[Cos, Sin, 0.0],[-Sin, Cos, 0.0],[0.0, 0.0, 1.0]]

		self.S2DMatrixMultiply(mat)
		return

	def TransformSPoints(self, vPoints):
		for idx, point in enumerate(vPoints):
			tempX = self._Matrix._2DMatrix[0][0] * point._x + self._Matrix._2DMatrix[1][0] * point._y + self._Matrix._2DMatrix[2][0]
			tempY = self._Matrix._2DMatrix[0][1] * point._x + self._Matrix._2DMatrix[1][1] * point._y + self._Matrix._2DMatrix[2][1]
			point._x = tempX
			point._y = tempY

		return vPoints

	def show(self):
		for i in xrange(len(self._Matrix._2DMatrix)):
			lineStr = ""
			for j in xrange(len(self._Matrix._2DMatrix[i])):
				lineStr += str(self._Matrix._2DMatrix[i][j]) + ", "
			print lineStr


class S2DMatrix(object):
	def __init__(self):
		self._2DMatrix = array([[0.0, 0.0, 0.0],[0.0, 0.0, 0.0],[0.0, 0.0, 0.0]])
		return

class C2DMatrix(object):
	def __init__(self):
		self._Matrix = S2DMatrix()

		self.Identity()
		return

	def Identity(self):
		self._Matrix._2DMatrix = array([[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[0.0, 0.0, 1.0]])
		return

	def S2DMatrixMultiply(self, mIn):
		self._Matrix._2DMatrix = dot(self._Matrix._2DMatrix, mIn._2DMatrix)
		return

	def Translate(self, x, y):
		mat = S2DMatrix()
		mat._2DMatrix = array([[1.0, 0.0, 0.0],[0.0, 1.0, 0.0],[x, y, 1.0]])

		self.S2DMatrixMultiply(mat)
		return

	def Scale(self, xScale, yScale):
		mat = S2DMatrix()
		mat._2DMatrix = array([[xScale, 0.0, 0.0],[0.0, yScale, 0.0],[0.0, 0.0, 1.0]])

		self.S2DMatrixMultiply(mat)
		return

	def Rotate(self, rot):
		mat = S2DMatrix()
		Sin = math.sin(rot)
		Cos = math.cos(rot)
		mat._2DMatrix = array([[Cos, Sin, 0.0],[-Sin, Cos, 0.0],[0.0, 0.0, 1.0]])

		self.S2DMatrixMultiply(mat)
		return

	def TransformSPoints(self, vPoints):
		for idx, point in enumerate(vPoints):
			tempX = self._Matrix._2DMatrix[0][0] * point._x + self._Matrix._2DMatrix[1][0] * point._y + self._Matrix._2DMatrix[2][0]
			tempY = self._Matrix._2DMatrix[0][1] * point._x + self._Matrix._2DMatrix[1][1] * point._y + self._Matrix._2DMatrix[2][1]
			point._x = tempX
			point._y = tempY

		return vPoints

	def show(self):
		for i in xrange(len(self._Matrix._2DMatrix)):
			lineStr = ""
			for j in xrange(len(self._Matrix._2DMatrix[i])):
				lineStr += str(self._Matrix._2DMatrix[i][j]) + ", "
			print lineStr

#a = C2DMatrix()
#a.show()
#print '---------'
#a.Translate(1,2)
#a.show()
#print '---------'
#a.Scale(2,3)
#a.show()
#print '---------'
#a.Rotate(30)
#a.show()