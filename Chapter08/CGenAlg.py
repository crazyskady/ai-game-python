# -*- coding: utf-8 -*-
import random
import copy

dMaxPerturbation = 0.3
iNumCopiesElite  = 1
iNumElite        = 4
iTournamentCompetitors = 4

class SGenome(object):
	def __init__(self, w, f=0.0):
		self._vecWeights = w
		self._dFitness   = f

	def __lt__(self, rhs):
		return self._dFitness < rhs._dFitness

class CGenAlg(object):
	def __init__(self, popSize, muteRate, crossRate, numWeights, splits):
		self._iPopSize = popSize
		self._dMutationRate = muteRate
		self._dCrossoverRate= crossRate
		self._iChromoLength = numWeights
		self._dTotalFitness = 0.0
		self._cGeneration   = 0
		self._iFittestGenome= 0
		self._dBestFitness  = 0.0
		self._dWorstFitness = 999999999.9
		self._dAverageFitness = 0.0
		self._vecSplitPoints = splits

		self._vecPop = []

		for i in xrange(self._iPopSize):
			self._vecPop.append(SGenome([], 0.0))

		for i in xrange(self._iPopSize):
			for j in xrange(self._iChromoLength):
				self._vecPop[i]._vecWeights.append(random.random() - random.random())
		return

	def Mutate(self, chromo):
		newChromo = []
		for idx, gene in enumerate(chromo):
			if random.random() < self._dMutationRate:
				gene += (random.random() - random.random()) * dMaxPerturbation # dMaxPerturbation = 0.3
			newChromo.append(gene)
		return newChromo

	def GetChromos(self):
		return self._vecPop

	def GetChromoRoulette(self):
		Slice = random.random() * self._dTotalFitness
		TheChosenOne = None

		FitnessSoFar = 0

		for i in xrange(self._iPopSize):
			FitnessSoFar += self._vecPop[i]._dFitness
			if FitnessSoFar >= Slice:
				TheChosenOne = copy.deepcopy(self._vecPop[i])
				break

		return TheChosenOne

	def TournamentSelection(self, N):
		BestFitnessSoFar = -999999
		ChosenOne = 0
		
		for i in xrange(N):
			ThisTry = random.randint(0, self._iPopSize - 1)
			if self._vecPop[ThisTry]._dFitness > BestFitnessSoFar:
				ChosenOne = ThisTry
				BestFitnessSoFar = self._vecPop[ThisTry]._dFitness
		#print ChosenOne
		return self._vecPop[ChosenOne]

	def Crossover(self, mum, dad):
		baby1 = []
		baby2 = []
		if random.random() > self._dCrossoverRate or mum == dad:
			baby1 = copy.deepcopy(mum)
			baby2 = copy.deepcopy(dad)
			return baby1, baby2

		cp = random.randint(0, self._iChromoLength-1)
		baby1 = mum[:cp] + dad[cp:]
		baby2 = dad[:cp] + mum[cp:]

		return baby1, baby2

	def CrossoverAtSplits(self, mum, dad):
		baby1 = []
		baby2 = []
		if random.random() > self._dCrossoverRate or mum == dad:
			baby1 = copy.deepcopy(mum)
			baby2 = copy.deepcopy(dad)
			return baby1, baby2

		cpIdx1 = random.randint(0, len(self._vecSplitPoints)-2)
		cp1 = self._vecSplitPoints[cpIdx1]
		cp2 = self._vecSplitPoints[random.randint(cpIdx1, len(self._vecSplitPoints)-1)]

		baby1 = mum[:cp1] + dad[cp1:cp2] + mum[cp2:]
		baby2 = dad[:cp1] + mum[cp1:cp2] + dad[cp2:]

		return baby1, baby2

	def CalculateBestWorstAvTot(self):
		self._dTotalFitness = 0.0
		HighestSoFar = 0.0
		LowestSoFar  = 999999999.9

		for idx, chromo in enumerate(self._vecPop):
			if chromo._dFitness > HighestSoFar:
				HighestSoFar = chromo._dFitness
				self._iFittestGenome = idx
				self._dBestFitness = HighestSoFar

			if chromo._dFitness < LowestSoFar:
				LowestSoFar = chromo._dFitness
				self._dWorstFitness = LowestSoFar

			self._dTotalFitness += chromo._dFitness

		self._dAverageFitness = self._dTotalFitness / self._iPopSize

	def FitnessScaleRank(self):
		FitnessMultiplier = 1
		for idx, chromo in enumerate(self._vecPop):
			self._vecPop[i]._dFitness = idx * FitnessMultiplier

		self.CalculateBestWorstAvTot()

	def Reset(self):
		self._dTotalFitness = 0.0
		self._dBestFitness  = 0.0
		self._dWorstFitness = 999999999.9
		self._dAverageFitness = 0.0

	def GrabNBest(self, NBest, NumCopies):
		Pop = []
		while NBest != 0:
			for i in xrange(NumCopies):
				Pop.append(self._vecPop[(self._iPopSize - 1) - NBest])
			NBest -= 1

		return Pop

	def Epoch(self, old_pop):
		self._vecPop = copy.deepcopy(old_pop)

		self.Reset()

		self._vecPop.sort()  # 我们为SGenome重载了__lt__

		self.CalculateBestWorstAvTot()

		vecNewPop = []
		if (iNumCopiesElite * iNumElite) % 2 == 0:
			vecNewPop = vecNewPop + self.GrabNBest(iNumElite, iNumCopiesElite)

		while len(vecNewPop) < self._iPopSize:
			mum = self.TournamentSelection(iTournamentCompetitors)
			dad = self.TournamentSelection(iTournamentCompetitors)

			baby1, baby2 = self.CrossoverAtSplits(mum._vecWeights, dad._vecWeights)

			baby1 = self.Mutate(baby1)
			baby2 = self.Mutate(baby2)

			vecNewPop.append(SGenome(baby1, 0.0))
			vecNewPop.append(SGenome(baby2, 0.0))

		self._vecPop = copy.deepcopy(vecNewPop)

		return self._vecPop

	def AverageFitness(self):
		return self._dTotalFitness/self._iPopSize

	def BestFitness(self):
		return self._dBestFitness