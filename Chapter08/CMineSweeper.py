# -*- coding: utf-8 -*-
import random
from SVector2D import SVector2D, Vec2DLength, Vec2DNormalize, Vec2DDot, Vec2DSign
from NeuralNet import CNeuralNet
from C2DMatrix import C2DMatrix, SPoint
from SVector2D import SVector2D
from CMapper import CMapper
from math import *
import copy

from collision import LineIntersection2D

dPi     = 3.14159265358979
dHalfPi = dPi / 2
dTwoPi  = dPi * 2
iSweeperScale= 5

WindowWidth  = 400
WindowHeight = 400

iNumSensors  = 5
dSensorRange = 25.0

iNumOutputs = 2
iNumHidden  = 1  
iNeuronsPerHiddenLayer = 10

dMaxTurnRate = 0.2

dCollisionDist = (iSweeperScale + 1.0)/dSensorRange

class CMinesweeper(object):
	def __init__(self):
		self._dRotation = random.random() * dTwoPi
		self._lTrack = 0.16
		self._rTrack = 0.16
		self._dFitness = 0
		self._dScale   = iSweeperScale
		self._bCollided = False

		self._vPosition = SVector2D(180, 200)

		self._Sensors = self.CreateSensors(iNumSensors, dSensorRange)
		self._tranSensors = []
		self._vecdSensors = []
		self._vecFeelers  = []

		self._MemoryMap = CMapper(WindowWidth, WindowHeight)
		self._ItsBrain = CNeuralNet()

		self._vLookAt = SVector2D()
		self._dSpeed = 0.0
		self._dSpinBonus = 0
		self._dCollisionBonus = 0
		return

	def CreateSensors(self, NumSensors, SensorRange):
		sensors = []
		SegmentAngle = dPi / (NumSensors - 1)
		for i in xrange(NumSensors):
			angle = i * SegmentAngle - dHalfPi
			sensors.append(SPoint((-sin(angle)*SensorRange), cos(angle)*SensorRange))
		return sensors


	def Reset(self):
		self._vPosition = SVector2D(180, 200)
		self._dFitness = 0
		self._dRotation= random.random() * dTwoPi
		self._MemoryMap.Reset()
		self._dSpinBonus = 0
		self._dCollisionBonus = 0
		return

	def Render(self):
		print "To be implemetented"

	def WorldTransform(self, sweeper, scale):
		matTransform = C2DMatrix()
		matTransform.Scale(scale, scale)
		matTransform.Rotate(self._dRotation)
		matTransform.Translate(self._vPosition._x, self._vPosition._y)

		return matTransform.TransformSPoints(sweeper)  # sweeper是引用传递，保持统一直接全部用return来返回了

	def Update(self, objs):
		inputs = []
		self.TestSensors(objs)

		for idx,sr in enumerate(self._vecdSensors):
			inputs.append(self._vecdSensors[idx])

		output = self._ItsBrain.Update(inputs)
		if len(output) != iNumOutputs:
			print "Number of Outputs is wrong, current: %d, expected: %d" % (len(output), iNumOutputs)
			return False

		self._lTrack = output[0]
		self._rTrack = output[1]
		RotForce = self._lTrack - self._rTrack
		# Clamp rotation
		RotForce = -dMaxTurnRate if RotForce < -dMaxTurnRate else dMaxTurnRate if RotForce > dMaxTurnRate else RotForce
		
		self._dRotation += RotForce
		self._vLookAt._x = -sin(self._dRotation)
		self._vLookAt._y = cos(self._dRotation)

		if self._bCollided == False:
			self._dSpeed = self._lTrack + self._rTrack
			self._vPosition = self._vPosition + (self._vLookAt * self._dSpeed)
			#print self._vPosition._x

		RotationTolerance = 0.03
		if -RotationTolerance < RotForce < RotationTolerance:
			self._dSpinBonus += 1

		if self._bCollided == False:
			self._dCollisionBonus += 1

		return True

	def TestSensors(self, objs):
		self._bCollided = False

		self._tranSensors = copy.deepcopy(self._Sensors)
		self._tranSensors = self.WorldTransform(self._tranSensors, 1)
		self._vecdSensors = []

		objs_len = len(objs)
		PointA = SPoint(self._vPosition._x, self._vPosition._y)
		#print len(objs), len(self._tranSensors)
		for sr in self._tranSensors:
			bHit = False
			dist = 0.0
			for seg in xrange(0, objs_len, 2):
				#print self._vPosition._x, self._vPosition._y, sr._x, sr._y, objs[seg]._x, objs[seg]._y
				#bHit, dist = LineIntersection2D(PointA,sr,objs[seg],objs[seg+1])
				bHit, dist = LineIntersection2D(PointA._x, PointA._y, sr._x, sr._y, objs[seg]._x, objs[seg]._y, objs[seg+1]._x, objs[seg+1]._y)
				if bHit == True:
					break

			if bHit == True:
				self._vecdSensors.append(dist)
				if dist < dCollisionDist:   # dist is also in [0, 1]
					self._bCollided = True
			else:
				self._vecdSensors.append(-1)

	def EndOfRunCalculations(self):
		self._dFitness = self._dFitness + self._dSpinBonus + self._dCollisionBonus

	def CalculateSplitPoints(self):
		return self._ItsBrain.CalculateSplitPoints()

	def Fitness(self):
		return self._dFitness

	def NumCellsVisited(self):
		return self._MemoryMap.NumCellsVisited()

	def Collided(self):
		return self._bCollided

	def GetNumberOfWeights(self):
		return self._ItsBrain.GetNumberOfWeights()

	def PutWeights(self, weights):
		self._ItsBrain.PutWeights(weights)

	def Scale(self):
		return self._dScale


