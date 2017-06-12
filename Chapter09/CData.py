# -*- coding: utf-8 -*-

class CData(object):
	def __init__(self):

		self._iVectorSize = 12
		self._iNumPatterns= 11  # We have 11 patterns now
		self._vecPatterns = [[1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0],
							[-1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0],
							[0,1.0, 0,1.0, 0,1.0, 0,1.0, 0,1.0, 0,1.0, 0,1.0, 0,1.0, 0,1.0, 0,1.0, 0,1.0, 0,1.0],
							[0,-1.0, 0,-1.0, 0,-1.0, 0,-1.0, 0,-1.0, 0,-1.0, 0,-1.0, 0,-1.0, 0,-1.0, 0,-1.0, 0,-1.0, 0,-1.0],
							[1.0,0, 1.0,0, 1.0,0, 0,1.0, 0,1.0, 0,1.0, -1.0,0, -1.0,0, -1.0,0, 0,-1.0, 0,-1.0, 0,-1.0],
							[-1.0,0, -1.0,0, -1.0,0, 0,1.0, 0,1.0, 0,1.0, 1.0,0, 1.0,0, 1.0,0, 0,-1.0, 0,-1.0, 0,-1.0],
							[1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0, -0.45,0.9, -0.9, 0.45, -0.9,0.45],
							[-1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0, -1.0,0, 0.45,0.9, 0.9, 0.45, 0.9,0.45],
							[-0.7,0.7, -0.7,0.7, -0.7,0.7, -0.7,0.7, -0.7,0.7, -0.7,0.7, -0.7,0.7, -0.7,0.7, -0.7,0.7, -0.7,0.7, -0.7,0.7, -0.7,0.7],
							[0.7,0.7, 0.7,0.7, 0.7,0.7, 0.7,0.7, 0.7,0.7, 0.7,0.7, 0.7,0.7, 0.7,0.7, 0.7,0.7, 0.7,0.7, 0.7,0.7, 0.7,0.7],
							[1.0,0, 1.0,0, 1.0,0, 1.0,0, -0.72,0.69,-0.7,0.72,0.59,0.81, 1.0,0, 1.0,0, 1.0,0, 1.0,0, 1.0,0]]

		self._vecNames = ["Right", "Left", "Down", "Up", "Clockwise Square", "Anti-Clockwise Square",
						"Right Arrow", "Left Arrow", "South West", "Sout East", "Zorro"]

		self._SetIn  = []
		self._SetOut = []

		self.CreateTrainingSetFromData()
		return

	def CreateTrainingSetFromData(self):
		self._SetIn  = []
		self._SetOut = []

		for i in xrange(self._iNumPatterns):
			self._SetIn.append(self._vecPatterns[i])
			outputs = [0]*self._iNumPatterns
			outputs[i] = 1
			self._SetOut.append(outputs)
		return

	def PatternName(self, idx):
		try:
			name = self._vecNames[idx]
		except:
			name = "Unknown pattern"

		return name

	def AddData(self):
		# I won't implement this function in my demo, lazy

		return

	def GetInputSet(self):
		return self._SetIn

	def GetOutputSet(self):
		return self._SetOut