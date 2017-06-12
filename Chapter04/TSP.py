# -*- coding: utf-8 -*-
import random
import math
import copy

import pygame
from pygame.locals import *
from sys import exit

EPSILON = 0.000001
NUM_BEST_TO_ADD	= 2

class CoOrd(object):
	def __init__(self, a, b):
		self._x = a
		self._y = b

	def X(self):
		return self._x

	def Y(self):
		return self._y

class mapTSP(object):
	#mapWidth, mapHeight 是这些城市所在的画布的大小
	def __init__(self, mapWidth, mapHeight, numCities):
		self._mapWidth          = mapWidth
		self._mapHeight         = mapHeight
		self._numCities         = numCities
		self._BestPossibleRoute = 0
		self._CityCoOrds        = []

		self.CreateCitiesCircular()
		self.CalculateBestPossibleRoute()
		return

	def CreateCitiesCircular(self):
		margin = 40 #if you have GUI, this parameter should be set
		radius = 0

		if self._mapHeight < self._mapWidth:
			radius = (self._mapHeight/2) - margin
		else:
			radius = (self._mapWidth/2) - margin

		origin = CoOrd(self._mapWidth/2, self._mapHeight/2)
		segmentSize = 2 * math.pi / self._numCities

		angle  = 0


		while angle < (2 * math.pi):
			thisCity = CoOrd((radius*math.sin(angle) + origin.X()), (radius * math.cos(angle) + origin.Y()))
			self._CityCoOrds.append(thisCity)
			angle += segmentSize

		return

	def CalculateA_to_B(self, city1, city2):
		#print city1, city2
		xDist = city1.X() - city2.X()
		yDist = city1.Y() - city2.Y()

		return math.sqrt(xDist*xDist + yDist*yDist)

	def CalculateBestPossibleRoute(self):
		#print "Enter CalculateBestPossibleRoute"
		self._BestPossibleRoute = 0

		for idx, city in enumerate(self._CityCoOrds[:-1]):
			self._BestPossibleRoute += self.CalculateA_to_B(city, self._CityCoOrds[idx+1])
			self._BestPossibleRoute += EPSILON

		self._BestPossibleRoute += self.CalculateA_to_B(self._CityCoOrds[-1], self._CityCoOrds[0])
		return

	def BestPossibleRoute(self):
		return self._BestPossibleRoute

	def GetTourLength(self, route):
		#print "Enter GetTourLength", route
		TotalDistance = 0

		for idx, city in enumerate(route[:-1]):
			TotalDistance += self.CalculateA_to_B(self._CityCoOrds[city], self._CityCoOrds[route[idx+1]])

		TotalDistance += self.CalculateA_to_B(self._CityCoOrds[route[-1]], self._CityCoOrds[route[0]])
		return TotalDistance


class SGenome(object):
	def __init__(self, nc):
		self._Fitness = 0
		self._Cities = self.GrabPermutation(nc)

		return

	def GrabPermutation(self, limit):
		Perm = []
		for i in xrange(limit):
			NextPossibleNumber = random.randint(0, limit-1)
			while NextPossibleNumber in Perm:
				NextPossibleNumber = random.randint(0, limit-1)
			Perm.append(NextPossibleNumber)
		return Perm

	def Show(self):
		print self._Cities


class gaTSP(object):
	def __init__(self, mutRate, crossRate, popSize, numCities, mapWidth, mapHeight):
		self._MutationRate = mutRate
		self._CrossoverRate = crossRate
		self._PopSize = popSize
		self._FittestGenome = 0
		self._Generation = 0
		self._ShortestRoute = 9999999999
		self._LongestRoute = 0
		self._ChromoLength = numCities
		self._Busy = False
		self._TotalFitness = 0.0

		self._Population = []

		self._Map = mapTSP(mapWidth, mapHeight, numCities)
		self.CreateStartingPopulation()

		return

	def CreateStartingPopulation(self):
		self._Population = []

		for i in xrange(self._PopSize):
			self._Population.append(SGenome(self._ChromoLength))

		self._Generation    = 0
		self._ShortestRoute = 9999999999
		self._FittestGenome = 0
		self._Busy          = False
		return

	def RouletteWhellSelection(self):
		fSlice = random.random() * self._TotalFitness
		cfTotal = 0.0
		SelectedGenome = 0

		for i in xrange(self._PopSize):
			cfTotal += self._Population[i]._Fitness
			if cfTotal > fSlice:
				SelectedGenome = i
				break

		return self._Population[SelectedGenome]

	def MutateEM(self, chromo):
		if random.random() > self._MutationRate:
			return chromo

		pos1 = random.randint(0, len(chromo)-1)
		pos2 = pos1

		while pos1 == pos2:
			pos2 = random.randint(0, len(chromo)-1)

		chromo[pos1], chromo[pos2] = chromo[pos2], chromo[pos1]

		return chromo

	def CrossoverPMX(self, mum, dad):
		if random.random() > self._CrossoverRate or mum == dad:
		#if random.random() > self._CrossoverRate:
			return mum, dad
			
		baby1 = copy.deepcopy(mum)
		baby2 = copy.deepcopy(dad)

		beg = random.randint(0, len(mum)-2)
		end = random.randint(beg+1, len(mum)-1)

		for pos in range(beg, end+1):
			gene1 = baby1[pos]
			gene2 = baby2[pos]

			if gene1 != gene2: #每个数字都是应该不重复的
				posGene1 = baby1.index(gene1)
				posGene2 = baby1.index(gene2)
				baby1[posGene1], baby1[posGene2] = baby1[posGene2], baby1[posGene1]

				posGene1 = baby2.index(gene1)
				posGene2 = baby2.index(gene2)
				baby2[posGene1], baby2[posGene2] = baby2[posGene2], baby2[posGene1]

		return baby1, baby2

	def CalculatePopulationsFitness(self):
		for i in xrange(self._PopSize):
			TourLength = self._Map.GetTourLength(self._Population[i]._Cities)
			self._Population[i]._Fitness = TourLength

			if TourLength < self._ShortestRoute:
				self._ShortestRoute = TourLength
				self._FittestGenome = i

			if TourLength > self._LongestRoute:
				self._LongestRoute = TourLength

		for i in xrange(self._PopSize):
			self._Population[i]._Fitness = self._LongestRoute - self._Population[i]._Fitness
			self._TotalFitness += self._Population[i]._Fitness

		return

	def Reset(self):
		self._ShortestRoute = 9999999999
		self._LongestRoute  = 0
		self._TotalFitness  = 0
		return

	def Epoch(self):
		self.Reset()
		self.CalculatePopulationsFitness()

		if self._ShortestRoute <= self._Map.BestPossibleRoute():
			self._Busy = False
			print "Generation: ", self._Generation, " Find Path: ", self._Population[self._FittestGenome]._Cities
			return

		NewPop = []
		for i in xrange(NUM_BEST_TO_ADD):
			NewPop.append(copy.deepcopy(self._Population[self._FittestGenome]))

		while len(NewPop) < self._PopSize:
			mum = self.RouletteWhellSelection()
			dad = self.RouletteWhellSelection()
			baby1 = SGenome(0)
			baby2 = SGenome(0)

			baby1._Cities, baby2._Cities = self.CrossoverPMX(mum._Cities, dad._Cities)

			baby1._Cities = self.MutateEM(baby1._Cities)
			baby2._Cities = self.MutateEM(baby2._Cities)

			NewPop.append(baby1)
			NewPop.append(baby2)

		self._Population = NewPop
		self._Generation += 1

		return

	def Run(self):
		self.CreateStartingPopulation()
		self._Busy = True

	def Started(self):
		return self._Busy

	def Stop(self):
		self._Busy = False
		return


if __name__ == "__main__":

	WINDOW_WIDTH  = 500
	WINDOW_HEIGHT = 500	
	NUM_CITIES = 20
	CITY_SIZE = 5
	MUTATION_RATE = 0.2
	CROSSOVER_RATE = 0.75
	POP_SIZE = 40	

	#Test Code(self, mutRate, crossRate, popSize, numCities, mapWidth, mapHeight):
	test_gaTSP = gaTSP(MUTATION_RATE, CROSSOVER_RATE, POP_SIZE, NUM_CITIES, WINDOW_WIDTH, WINDOW_HEIGHT)
	test_gaTSP.Run()

	pygame.init()	

	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
	font = pygame.font.SysFont("arial", 16)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

		screen.fill((255, 255, 255))

		for idx, item in enumerate(test_gaTSP._Map._CityCoOrds):
			pygame.draw.circle(screen,[255,0,0],[int(item._x), int(item._y)],5,0)

		if test_gaTSP.Started():
			test_gaTSP.Epoch()

		drawPoints = []
		for idx, item in enumerate(test_gaTSP._Population[test_gaTSP._FittestGenome]._Cities):
			cityPos = test_gaTSP._Map._CityCoOrds[item]
			drawPoints.append([int(cityPos._x), int(cityPos._y)])

		pygame.draw.lines(screen, [0, 255, 0], True, drawPoints, 2)
		generatioinStr = "Generation: " + str(test_gaTSP._Generation)
		screen.blit(font.render(generatioinStr, True, (0, 0, 255)), (20, 20))

		pygame.display.update()



		

