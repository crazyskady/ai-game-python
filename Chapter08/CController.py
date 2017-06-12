# -*- coding: utf-8 -*-
import random
import copy
from C2DMatrix import SPoint, C2DMatrix
from CMineSweeper import CMinesweeper
from CGenAlg import CGenAlg
from SVector2D import SVector2D

# For paint
import pygame
from pygame.locals import *
from sys import exit

dCrossoverRate = 0.7
dMutationRate  = 0.1
iNumTicks      = 2000
iNumElite      = 4

NumSweeperVerts    = 16
sweeper = [SPoint(-0.5, -0.5), SPoint(-0.5, -1), SPoint(-1, -1), SPoint(-1, 1), SPoint(-0.5, 1), SPoint(-0.5, 0.5), SPoint(-0.25, 0.5), SPoint(-0.25, 1.75),
SPoint(0.25, 1.75), SPoint(0.25, 0.5), SPoint(0.5, 0.5), SPoint(0.5, 1), SPoint(1,1), SPoint(1, -1), SPoint(0.5, -1), SPoint(0.5, -0.5)]

objects = [SPoint(80, 60),SPoint(200,60),SPoint(200,60),SPoint(200,100),SPoint(200,100),SPoint(160,100),SPoint(160,100),SPoint(160,200),SPoint(160,200),SPoint(80,200),SPoint(80,200),SPoint(80,60),
SPoint(250,100),SPoint(300,40),SPoint(300,40),SPoint(350,100),SPoint(350,100),SPoint(250, 100),
SPoint(220,180),SPoint(320,180),SPoint(320,180),SPoint(320,300),SPoint(320,300),SPoint(220,300),SPoint(220,300),SPoint(220,180),
SPoint(12,15),SPoint(380, 15),SPoint(380,15),SPoint(380,360),SPoint(380,360),SPoint(12,360),SPoint(12,360),SPoint(12,340),SPoint(12,340),SPoint(100,290),SPoint(100,290),SPoint(12,240),SPoint(12,240),SPoint(12,15)]

class CController(object):
	def __init__(self, NumSweepers, WindowWidth, WindowHeight):
		self._iTicks = 0
		self._NumSweepers = NumSweepers
		self._cxClient = WindowWidth
		self._cyClient = WindowHeight

		self._vecSweepers = []

		#self._vecSweepers = [CMinesweeper()] * self._NumSweepers CMinesweeper中有随机变量，如果用这种方式会直接拷贝而不会随机生成了
		for i in xrange(self._NumSweepers):
			self._vecSweepers.append(CMinesweeper())

		self._NumWeightsInNN = self._vecSweepers[0].GetNumberOfWeights()
		SplitPoints = self._vecSweepers[0].CalculateSplitPoints()

		self._pGA = CGenAlg(self._NumSweepers, dMutationRate, dCrossoverRate, self._NumWeightsInNN, SplitPoints)

		self._vecThePopulation = self._pGA.GetChromos()

		for i in xrange(self._NumSweepers):
			self._vecSweepers[i].PutWeights(self._vecThePopulation[i]._vecWeights)

		self._vecAvFitness = []
		self._vecBestFitness = []
		self._iGenerations = 0
		self._bFastRender  = False


	def Update(self):
		self._iTicks += 1
		if self._iTicks < iNumTicks:
			for i in xrange(self._NumSweepers):
				if self._vecSweepers[i].Update(objects) == False:
					print "Wrong amount of NN inputs"
					return False

		else:
			for i in xrange(self._NumSweepers):
				self._vecSweepers[i].EndOfRunCalculations()
				self._vecThePopulation[i]._dFitness = self._vecSweepers[i].Fitness()

			self._vecAvFitness.append(self._pGA.AverageFitness())   # A little different, I don't use raw here.
			self._vecBestFitness.append(self._pGA.BestFitness())

			self._iGenerations += 1

			self._iTicks = 0

			self._vecThePopulation = self._pGA.Epoch(self._vecThePopulation)

			for i in xrange(self._NumSweepers):
				self._vecSweepers[i].PutWeights(self._vecThePopulation[i]._vecWeights)
				self._vecSweepers[i].Reset()

		return True

	def Render(self, screen, font):
		blue = (0, 0, 255)
		red  = (255, 0, 0)
		green= (0, 150, 0)
		black= (0, 0, 0)


		if self._bFastRender == False:
			generationStr = "Generation:       " + str(self._iGenerations)
			screen.blit(font.render(generationStr, True, (0, 0, 255)), (20, 20))

			# 画墙
			for i in xrange(0, len(objects), 2):
				pygame.draw.line(screen, black, (objects[i]._x, objects[i]._y), (objects[i+1]._x, objects[i+1]._y), 2)

			# 画sweepers，最优的前iNumElite用红色画出来
			for i in xrange(self._NumSweepers):
				sweeperVB = copy.deepcopy(sweeper)
				sweeperVB = self._vecSweepers[i].WorldTransform(sweeperVB, self._vecSweepers[i].Scale())
				points4Paint = []
				for item in sweeperVB:
					points4Paint.append((item._x, item._y))
				if i < iNumElite:
					pygame.draw.polygon(screen, red, points4Paint, 1)
				else:
					pygame.draw.polygon(screen, blue, points4Paint, 1)

		else:
			bestStr       = "Best Fitness     :" + str(self._pGA.BestFitness())
			avgStr        = "Average Fitness  :" + str(self._pGA.AverageFitness())
			generationStr = "Generation       :" + str(self._iGenerations)
			screen.blit(font.render(generationStr, True, (0, 0, 255)), (20, 10))
			screen.blit(font.render(bestStr, True, (0, 0, 255)), (20, 25))
			screen.blit(font.render(avgStr, True, (0, 0, 255)), (20, 40))

			HSlice = self._cxClient * 1.0 / (self._iGenerations + 1)
			VSlice = self._cyClient * 1.0 / ((self._pGA.BestFitness() + 1) * 2)

			# 画Best线，画的有问题，懒得Fix了~~~
			x = 0.0
			previousPos = (0, 0) 
			for idx, item in enumerate(self._vecBestFitness):
				pygame.draw.line(screen, red, previousPos, (x, item*VSlice))
				previousPos = (x, item*VSlice)
				x += HSlice

	def FastRenderToggle(self):
		self._bFastRender = not self._bFastRender

'''
if __name__ == "__main__":
	WINDOW_WIDTH  = 400
	WINDOW_HEIGHT = 400	
	pygame.init()	

	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
	font = pygame.font.SysFont("arial", 16)
	clock=pygame.time.Clock()

	g_pController = CController(40,WINDOW_WIDTH,WINDOW_HEIGHT);
	i = 0
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					g_pController.FastRenderToggle()

		clock.tick(2000)
		screen.fill((255, 255, 255))

		g_pController.Update()
		g_pController.Render(screen, font)

		pygame.display.update()
'''

def Test_func():
	WINDOW_WIDTH  = 400
	WINDOW_HEIGHT = 400	
	g_pController = CController(40,WINDOW_WIDTH,WINDOW_HEIGHT);

	i = 2000
	while i>0:
		g_pController.Update()
		i = i - 1

import cProfile

cProfile.run('Test_func()')
