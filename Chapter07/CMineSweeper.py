# -*- coding: utf-8 -*-
import random
from SVector2D import SVector2D, Vec2DLength, Vec2DNormalize, Vec2DDot, Vec2DSign
from NeuralNet import CNeuralNet
from C2DMatrix import C2DMatrix
import math

dPi     = 3.14159265358979
dHalfPi = dPi / 2
dTwoPi  = dPi * 2
dStartEnergy = 20.0
iSweeperScale= 5

WindowWidth  = 400
WindowHeight = 400

iNumInputs  = 4
iNumOutputs = 2
iNumHidden  = 1  
iNeuronsPerHiddenLayer = 10

dMaxTurnRate = 0.3

class CMinesweeper(object):
	def __init__(self):
		self._dRotation = random.random() * dTwoPi
		self._lTrack = 0.16
		self._rTrack = 0.16
		self._dFitness = dStartEnergy
		self._dScale   = iSweeperScale
		self._iClosestMine = 0
		self._vLookAt = SVector2D()
		self._ItsBrain = CNeuralNet()
		self._dSpeed = 0.0

		self._vPosition = SVector2D(random.random()*WindowWidth, random.random()*WindowHeight)
		return

	def Reset(self):
		self._vPosition = SVector2D(random.random()*WindowWidth, random.random()*WindowHeight)
		self._dFitness = dStartEnergy
		self._dRotation= random.random() * dTwoPi
		return

	def WorldTransform(self, sweeper):
		matTransform = C2DMatrix()
		matTransform.Scale(self._dScale, self._dScale)
		matTransform.Rotate(self._dRotation)
		matTransform.Translate(self._vPosition._x, self._vPosition._y)

		return matTransform.TransformSPoints(sweeper)  # sweeper是引用传递，保持统一直接全部用return来返回了

	def GetClosestMine(self, mines):
		closest_so_far = 99999.9
		vClosestObj = SVector2D(0.0, 0.0)

		for idx, mine in enumerate(mines):
			len_to_obj = Vec2DLength(mine - self._vPosition)
			if len_to_obj < closest_so_far:
				closest_so_far = len_to_obj
				vClosestObj = self._vPosition - mine  # 计算当前Position到最近的mine的矢量距离
				self._iClosestMine = idx

		return vClosestObj

	def CheckForMine(self, mines, size):
		DistToObj = self._vPosition - mines[self._iClosestMine]
		if Vec2DLength(DistToObj) < (size + 5):
			return self._iClosestMine

		return -1

	def Update(self, mines):
		inputs = []

		vClosestMine = self.GetClosestMine(mines)
		vClosestMine = Vec2DNormalize(vClosestMine)
		'''
		dot  = Vec2DDot(self._vLookAt, vClosestMine)
		sign = Vec2DSign(self._vLookAt, vClosestMine)
		inputs.append(dot * sign)
		'''

		inputs.append(vClosestMine._x)
		inputs.append(vClosestMine._y)
		inputs.append(self._vLookAt._x)
		inputs.append(self._vLookAt._x)
		output = self._ItsBrain.Update(inputs)

		if len(output) < iNumOutputs:
			print "Output size not correct. Length of output %d, iNumOutputs %d" % (len(output), iNumOutputs)
			return False

		self._lTrack = output[0]
		self._rTrack = output[1]

		RotForce = self._lTrack - self._rTrack
		# Clamp rotation
		RotForce = -dMaxTurnRate if RotForce < -dMaxTurnRate else dMaxTurnRate if RotForce > dMaxTurnRate else RotForce

		self._dRotation += RotForce

		self._dSpeed = self._lTrack + self._rTrack
		self._vLookAt._x = -math.sin(self._dRotation)
		self._vLookAt._y = math.cos(self._dRotation)

		self._vPosition = self._vPosition + (self._vLookAt * self._dSpeed) # 注意这里都是重载了Vector的运算

		self._vPosition._x = 0 if self._vPosition._x > WindowWidth else WindowWidth if self._vPosition._x < 0 else self._vPosition._x
		self._vPosition._y = 0 if self._vPosition._y > WindowHeight else WindowHeight if self._vPosition._y < 0 else self._vPosition._y

		return True

	def GetNumberOfWeights(self):
		return self._ItsBrain.GetNumberOfWeights()

	def CalculateSplitPoints(self):
		return self._ItsBrain.CalculateSplitPoints()

	def PutWeights(self, weights):
		self._ItsBrain.PutWeights(weights)

	def IncrementFitness(self):
		self._dFitness += 1

	def Fitness(self):
		return self._dFitness