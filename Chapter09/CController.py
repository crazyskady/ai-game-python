# -*- coding: utf-8 -*-
from CData import CData
from NeuralNet import CNeuralNet
from SVector2D import SVector2D, Vec2DNormalize
import copy
from math import sqrt

# For paint
import pygame
from pygame.locals import *
from sys import exit

UNREADY  = 0
TRAINING = UNREADY + 1
ACTIVE   = TRAINING + 1
LEARNING = ACTIVE + 1


class CController(object):
	def __init__(self, screen):
		self._Data = CData()   # NUM_VECTORS = 12 now
		self._Net  = CNeuralNet(12*2, 11, 6, 0.5)  # 12 vector, 11 patterns, 6 neur, 0.5 learning rate
		self._NumSmoothPoints = 12 + 1

		self._Path = []
		self._SmoothPath = []
		self._Vectors = []

		self._Mode = UNREADY
		self._Screen = screen

		self._HighestOutput = 0.0
		self._BestMatch = 0
		self._Match = -1

		self._Drawing = False
		return

	def Clear(self):
		self._Path = []
		self._SmoothPath = []
		self._Vectors = []

		return

	def TrainNetwork(self):
		self._Mode = TRAINING
		if self._Net.Train(self._Data, self._Screen) == False:
			print 'Train Failed!'
			return False

		self._Mode = ACTIVE

		return True

	def TestForMatch(self):
		outputs = self._Net.Update(self._Vectors)

		if len(outputs) == 0:
			print "Error in with ANN output"
			return False

		self._HighestOutput = 0.0
		self._BestMatch = 0
		self._Match = -1

		for i in xrange(len(outputs)):
			if outputs[i] > self._HighestOutput:
				self._HighestOutput = outputs[i]
				self._BestMatch = i

				if self._HighestOutput > 0.96: #MATCH_TOLERANCE
					self._Match = self._BestMatch

		return True

	def CreateVectors(self):
		for p in xrange(1, len(self._SmoothPath)):
			x = self._SmoothPath[p]._x - self._SmoothPath[p-1]._x
			y = self._SmoothPath[p]._y - self._SmoothPath[p-1]._y

			v1 = SVector2D(1.0, 0.0)    # What's the hell v1?
			v2 = SVector2D(x, y)

			v2 = Vec2DNormalize(v2)
			self._Vectors.append(v2._x)
			self._Vectors.append(v2._y)
		return


	def Smooth(self):
		if len(self._Path) < self._NumSmoothPoints:
			print "Length of Path not correct: %d, expected: %d" % (len(self._Path), self._NumSmoothPoints)
			return False

		self._SmoothPath = copy.deepcopy(self._Path)

		while len(self._SmoothPath) > self._NumSmoothPoints:
			ShortestSoFar = 99999999.9
			PointMarker = 0

			for SpanFront in xrange(2, len(self._SmoothPath)-1):
				xTmp = self._SmoothPath[SpanFront-1]._x - self._SmoothPath[SpanFront]._x
				yTmp = self._SmoothPath[SpanFront-1]._y - self._SmoothPath[SpanFront]._y
				length = sqrt(xTmp*xTmp + yTmp*yTmp)

				if length < ShortestSoFar:
					ShortestSoFar = length
					PointMarker = SpanFront

			newPoint = SVector2D((self._SmoothPath[PointMarker-1]._x + self._SmoothPath[PointMarker]._x)/2,\
				(self._SmoothPath[PointMarker-1]._y + self._SmoothPath[PointMarker]._y)/2)

			self._SmoothPath[PointMarker-1] = newPoint

			self._SmoothPath = self._SmoothPath[:PointMarker] + self._SmoothPath[(PointMarker+1):]

		return True

	def AddPoint(self, point):
		self._Path.append(point)
		return

	def IsDrawing(self):
		return self._Drawing

	def Drawing(self, val):

		if val == True:
			self.Clear()
		else:
			if self.Smooth() == True:
				self.CreateVectors()

				if self._Mode == ACTIVE:
					if self.TestForMatch() == False:
						print "Error when test for match"
						return False

		self._Drawing = val
		return True

	def Render(self, screen, font):
		if self._Mode == TRAINING:
			errStr = "Error: " + str(self._Net.Error())
			screen.blit(font.render(errStr, True, (0, 0, 255)), (20, 20))
			epochStr = "Epochs: " + str(self._Net.Epoch())
			screen.blit(font.render(epochStr, True, (0, 0, 255)), (120, 20))
		showStr = ""
		if self._Net.Trained():
			if self._Mode == ACTIVE:
				showStr = "Recognition circuits active"

			if self._Mode == LEARNING:
				showStr = "Recognition circuits offline - Enter a new gesture"

		else:
			showStr = "Training in progress..."

		screen.blit(font.render(showStr, True, (0, 0, 255)), (20, 380))

		if self._Drawing == False:
			if self._HighestOutput > 0.0:
				if len(self._SmoothPath) > 1 and self._Mode != LEARNING:
					if self._HighestOutput < 0.96: #MATCH_TOLERANCE
						showStr = "I'm guessing this is the pattern " + self._Data.PatternName(self._BestMatch)
						screen.blit(font.render(showStr, True, (0, 0, 255)), (20, 20))
					else:
						showStr = self._Data.PatternName(self._Match)
						screen.blit(font.render(showStr, True, (0, 255, 0)), (20, 20))
				elif self._Mode != LEARNING:
					showStr = "Not enough points drawn - plz try again"
					screen.blit(font.render(showStr, True, (255, 0, 0)), (20, 20))

		if len(self._Path) < 2:
			return
		drawPoints = []
		for i in xrange(len(self._Path)):
			drawPoints.append([int(self._Path[i]._x), int(self._Path[i]._y)])
		pygame.draw.lines(screen, [0, 255, 0], False, drawPoints, 1)

		if self._Drawing==False and len(self._SmoothPath) > 0:
			for idx, item in enumerate(self._SmoothPath):
				pygame.draw.circle(screen, [255,0,0], [int(item._x), int(item._y)], 5, 0)


if __name__ == "__main__":
	WINDOW_WIDTH  = 400
	WINDOW_HEIGHT = 400	
	pygame.init()	

	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
	font = pygame.font.SysFont("arial", 16)
	clock=pygame.time.Clock()

	g_pController = CController(screen)
	#g_pController.TrainNetwork()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					g_pController.TrainNetwork()

			if event.type == MOUSEBUTTONDOWN:
				g_pController.Drawing(True)
			if event.type == MOUSEBUTTONUP:
				g_pController.Drawing(False)

			if event.type == MOUSEMOTION:
				if g_pController.IsDrawing():
					pos = pygame.mouse.get_pos()
					g_pController.AddPoint(SVector2D(pos[0], pos[1]))

		clock.tick(2000)
		screen.fill((255, 255, 255))
		g_pController.Render(screen, font)

		pygame.display.update()