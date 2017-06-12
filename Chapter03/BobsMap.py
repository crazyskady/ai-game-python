# -*- coding: utf-8 -*-
import random
import pygame
from pygame.locals import *
from sys import exit

BobsMap = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
[8, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1],
[1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1],
[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1],
[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 5],
[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

MapHeight = len(BobsMap)
MapWidth  = len(BobsMap[0])
startPos  = [14, 7]
endPos    = [0, 2]

# 15 * 40 = 600, 10 * 40 = 400
block_size = 40

def TestRoute(Path):
	posX = startPos[0]
	posY = startPos[1]

	for direction in Path:
		if direction == 0: #North
			if posY - 1 > 0 and BobsMap[posY - 1][posX] != 1:
				posY -= 1

		elif direction == 1: #South
			if posY + 1 < MapHeight and BobsMap[posY + 1][posX] != 1:
				posY += 1

		elif direction == 2: #East
			if posX + 1 < MapWidth and BobsMap[posY][posX + 1] != 1:
				posX += 1

		elif direction == 3: #West
			if posX - 1 >= 0 and BobsMap[posY][posX - 1] != 1:
				posX -= 1

		else:
			print "Unknown direction: ", direction

	DiffX = abs(posX - endPos[0])
	DiffY = abs(posY - endPos[1])

	return 1.0/(DiffX + DiffY + 1)

class Genome(object):
	def __init__(self, num_bits): #check num_bits length
		self.Fitness = 0.0
		self.Bits    = []
		for i in xrange(num_bits):
			self.Bits.append(random.randint(0, 1))   # This loop can be replaced by:       map(lambda _:random.randint(0,1), xrange(num_bits))

	def _show(self):
		print self.Bits, self.Fitness

class GaBob(object):
	def __init__(self, cross_rat, mut_rate, pop_size, num_bits, gene_len):
		self.Genomes           = []
		self.PopSize           = pop_size
		self.CrossoverRate     = cross_rat
		self.MutationRate      = mut_rate
		self.ChromoLength      = num_bits
		self.GeneLength        = gene_len
		self.FittestGenome     = 0
		self.BestFitnessScore  = 0.0
		self.TotalFitnessScore = 0.0
		self.Generation        = 0
		self.Busy              = False
		pass

	def Run(self):
		self.CreateStartPopulation()
		self.Busy = True

	def _showPopulation(self):
		for i in xrange(self.PopSize):
			print self.Genomes[i].Bits

	def CreateStartPopulation(self):
		self.Genomes = []

		for i in xrange(self.PopSize):
			self.Genomes.append(Genome(self.ChromoLength))

		self.FittestGenome     = 0
		self.BestFitnessScore  = 0.0
		self.TotalFitnessScore = 0.0
		self.Generation        = 0
		return

	# 赌轮盘的选择方式:
	# 1. 随机生成一个在0到总适应度之间的值
	# 2. 遍历种群，对每个染色体的适应度进行累加
	# 3. 当遇到第一个大于1中生成的适应度的染色体时，停止累加，返回该染色体
	# 适应度越大的染色体被选中的概率越大 
	def RouletteWheelSelection(self):
		fSlice  = random.random() * self.TotalFitnessScore
		cfTotal = 0.0
		SelectedGenome = 0

		for i in xrange(self.PopSize):
			cfTotal += self.Genomes[i].Fitness
			if cfTotal > fSlice:
				SelectedGenome = i
				break
		return self.Genomes[SelectedGenome]

	def Mutate(self, bits):  #bits is a list
		for i in xrange(len(bits)):
			if random.random() < self.MutationRate:
				if bits[i] == 0:  #if bitArray, it's more easy to reverse
					bits[i] = 1
				if bits[i] == 1:
					bits[i] = 0
		return bits

	def Crossover(self, mum, dad):
		if random.random() > self.CrossoverRate or mum == dad:
			return mum, dad

		cp = random.randint(0, self.ChromoLength - 1)
		return mum[:cp]+dad[cp:], dad[:cp]+mum[cp:]

	def BinToInt(self, bins):
		val = 0
		multiplier = 1
		for bin in bins[::-1]:
			val += bin * multiplier
			multiplier *= 2
		return val

	def Decode(self, bits):
		directions = []
		for i in range(0, len(bits), self.GeneLength):
			ThisGene = []
			for j in range(self.GeneLength):
				ThisGene.append(bits[i+j])
			directions.append(self.BinToInt(ThisGene))
		return directions

	def UpdateFitnessScores(self):
		self.FittestGenome     = 0
		self.BestFitnessScore  = 0.0
		self.TotalFitnessScore = 0.0

		for i in xrange(self.PopSize):
			directions = self.Decode(self.Genomes[i].Bits)
			self.Genomes[i].Fitness = TestRoute(directions)
			#print directions, self.Genomes[i].Fitness
			self.TotalFitnessScore += self.Genomes[i].Fitness

			if self.Genomes[i].Fitness > self.BestFitnessScore:
				self.BestFitnessScore = self.Genomes[i].Fitness
				self.FittestGenome = i
				if self.Genomes[i].Fitness == 1:
					#we found, stop
					print "Found Path"
					print "Path is :", self.ShowPath(self.Decode(self.Genomes[i].Bits))
					self.Busy = False

		return

	def Epoch(self):
		self.UpdateFitnessScores()
		if not self.Busy:
			return
		NewBabies = 0
		BabyGenomes = []

		while NewBabies < self.PopSize:
			mum = self.RouletteWheelSelection()
			dad = self.RouletteWheelSelection()
			#print mum.Bits, dad.Bits
			baby1 = Genome(0)
			baby2 = Genome(0)
			baby1.Bits, baby2.Bits = self.Crossover(mum.Bits, dad.Bits)
			baby1.Bits = self.Mutate(baby1.Bits)
			baby2.Bits = self.Mutate(baby2.Bits)

			BabyGenomes.append(baby1)
			BabyGenomes.append(baby2)

			NewBabies += 2

		self.Genomes = BabyGenomes
		self.Generation += 1
		#print self.Generation, self.BestFitnessScore
		return

	def ShowPath(self, Path):
		pathStr = ""
		for direction in Path:
			if direction == 0: #North
				pathStr += "-North"

			elif direction == 1: #South
				pathStr += "-South"

			elif direction == 2: #East
				pathStr += "-East"

			elif direction == 3:
				pathStr += "-West"	

			else:
				pathStr += "-Unknown direction: ", direction

		return pathStr


	def Started(self):
		return self.Busy

	def Stop(self):
		self.Busy = False
		return

	def GetFittestDirection(self):
		return self.Decode(self.Genomes[self.FittestGenome].Bits)

# pos = (x, y), top left position of the rect
def set_block(screen, color, pos):
	top_side_rect   = Rect(pos[0], pos[1], block_size, 1)
	right_side_rect = Rect(pos[0] + block_size, pos[1], 1, block_size)
	bottom_side_rect= Rect(pos[0], pos[1] + block_size, block_size, 1)
	left_side_rect  = Rect(pos[0], pos[1], 1, block_size)
	center_rect     = Rect(pos[0]+1, pos[1]+1, block_size-1, block_size-1)
	pygame.draw.rect(screen, (255, 255, 255), top_side_rect)
	pygame.draw.rect(screen, (255, 255, 255), right_side_rect)
	pygame.draw.rect(screen, (255, 255, 255), bottom_side_rect)
	pygame.draw.rect(screen, (255, 255, 255), left_side_rect)
	pygame.draw.rect(screen, color, center_rect)

def set_path(screen, color, path):
	posX = startPos[0]
	posY = startPos[1]

	for direction in path:
		if direction == 0: #North
			if posY - 1 > 0 and BobsMap[posY - 1][posX] != 1:
				posY -= 1

		elif direction == 1: #South
			if posY + 1 < MapHeight and BobsMap[posY + 1][posX] != 1:
				posY += 1

		elif direction == 2: #East
			if posX + 1 < MapWidth and BobsMap[posY][posX + 1] != 1:
				posX += 1

		elif direction == 3: #West
			if posX - 1 >= 0 and BobsMap[posY][posX - 1] != 1:
				posX -= 1
		else:
			print "Unknown direction: ", direction

		if [posX, posY] == startPos:
			continue
		current_pos = (posX*block_size, posY*block_size)
		set_block(screen, color, current_pos)

if __name__ == "__main__":
	CROSSOVER_RATE = 0.7
	MUTATION_RATE  = 0.015	
	POP_SIZE       = 140
	CHROMO_LENGTH  = 70
	GENE_LENGTH    = 2	

	test_gaBob = GaBob(CROSSOVER_RATE, MUTATION_RATE, POP_SIZE, CHROMO_LENGTH, GENE_LENGTH)	
	test_gaBob.Run()

	pygame.init()	

	screen = pygame.display.set_mode((600, 400), 0, 32)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				exit()

		screen.fill((255, 255, 255))		
		#set_block(screen, (255,0,0), (100, 100))
		for yIdx, rowItem in enumerate(BobsMap):
			for xIdx, blockItem in enumerate(rowItem):
				if blockItem == 1:
					block_pos = (xIdx*block_size, yIdx*block_size)
					set_block(screen, (0, 0, 0), block_pos)
				elif blockItem == 5:
					block_pos = (xIdx*block_size, yIdx*block_size)
					set_block(screen, (255, 0, 0), block_pos)
				elif blockItem == 8:
					block_pos = (xIdx*block_size, yIdx*block_size)
					set_block(screen, (0, 255, 0), block_pos)	

		if test_gaBob.Started():
			test_gaBob.Epoch()

		set_path(screen, (0, 0, 255), test_gaBob.GetFittestDirection())

		pygame.display.update()
