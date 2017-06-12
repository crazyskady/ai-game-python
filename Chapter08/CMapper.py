# -*- coding: utf-8 -*-

dCellSize = 20
WindowWidth            = 400
WindowHeight           = 400

class SCell(object):
	def __init__(self, xmin, xmax, ymin, ymax):
		self._iTicksSpentHere = 0
		self._left  = xmin
		self._right = xmax
		self._top   = ymin
		self.bottom = ymax

	def Update(self):
		self._iTicksSpentHere += 1

	def Reset(self):
		self._iTicksSpentHere = 0

class CMapper(object):
	def __init__(self, MaxRangeX, MaxRangeY):
		self._dCellSize = dCellSize
		self._NumCellsX = (MaxRangeX/self._dCellSize) + 1
		self._NumCellsY = (MaxRangeY/self._dCellSize) + 1
		self._2DvecCells = []

		for x in xrange(self._NumCellsX):
			temp = []
			for y in xrange(self._NumCellsY):
				temp.append(SCell(x*self._dCellSize, (x+1)*self._dCellSize, y*self._dCellSize, (y+1)*self._dCellSize))
			self._2DvecCells.append(temp)

		self._iTotalCells = self._NumCellsX * self._NumCellsY

	def Update(self, xPos, yPos):
		if ((xPos < 0) or (xPos > WindowWidth) or (yPos < 0) or (yPos > WindowHeight)):
			return

		cellX = int(xPos/self._dCellSize)
		cellY = int(yPos/self._dCellSize)
		self._2DvecCells[cellX][cellY].Update()

	def TicksLingered(self, xPos, yPos):
		if ((xPos < 0) or (xPos > WindowWidth) or (yPos < 0) or (yPos > WindowHeight)):
			return 999

		cellX = int(xPos/self._dCellSize)
		cellY = int(yPos/self._dCellSize)
		return self._2DvecCells[cellX][cellY]._iTicksSpentHere

	def BeenVisited(self, xPos, yPos):
		print "Not implemented!"

	def Render(self):
		print "To be implemented"

	def Reset(self):
		for i in xrange(self._NumCellsX):
			for j in xrange(self._NumCellsY):
				self._2DvecCells[i][j].Reset()

	def NumCellsVisited(self):
		total = 0
		for i in xrange(self._NumCellsX):
			for j in xrange(self._NumCellsY):
				if self._2DvecCells[i][j]._iTicksSpentHere > 0:
					total += 1
		return total