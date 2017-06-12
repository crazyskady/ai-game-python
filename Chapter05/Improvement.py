# -*- coding: utf-8 -*-
import random

MUTATION_RATE = 0.2

def ChooseSection(max_span, min_span):
	beg = random.randint(0, max_span-min_span)
	end = random.randint(min_span + beg, max_span)

	return beg, end

# 散播变异
# 1. 在染色体上随机的选择一对位置
# 2. 将这一对位置中间的值进行随机的位置交换
def MutateSM(chromo):
	#if random.random() > MUTATION_RATE:
		#return chromo

	MinSpanSize = 3

	beg, end = ChooseSection(len(chromo) - 1, MinSpanSize)

	span = end - beg
	NumberOfSwapsRqd = span - 1

	while NumberOfSwapsRqd != 0:
		idx1 = beg + random.randint(0, span)
		idx2 = beg + random.randint(0, span)
		chromo[idx1], chromo[idx2] = chromo[idx2], chromo[idx1]
		NumberOfSwapsRqd = NumberOfSwapsRqd - 1

	return chromo

# 移位变异
# 1. 在染色体上随机的选择一对位置
# 2. 将这一对位置中间的值全部随机的移到剩余染色体中间的任一位置
def MutateDM(chromo):
	#if random.random() > MUTATION_RATE:
		#return chromo

	MinSpanSize = 3
	beg, end = ChooseSection(len(chromo) - 1, MinSpanSize)

	TheSection = chromo[beg:end]
	TheLeft = chromo[:beg] + chromo[end:]

	randPos = random.randint(0, len(TheLeft) - 1) # 如果len(TheLeft) == 0，randint会报错

	newChromo = TheLeft[:randPos] + TheSection + TheLeft[randPos:]

	return newChromo

# 插入变异
# 1. 随机选择一个Gen
# 2. 将选中的Gen随机的插入到染色体的其他的位置
def MutateIM(chromo):
	#if random.random() > MUTATION_RATE:
		#return chromo

	selectedPos = random.randint(0, len(chromo) - 1)
	selectedGen = [chromo[selectedPos]]

	newChromo = chromo[:selectedPos] + chromo[(selectedPos + 1) :]	

	newPos = random.randint(0, len(newChromo))  # [1,2,3], 可以有4个位置插入新的Gen

	return newChromo[:newPos] + selectedGen + newChromo[newPos:]

# 倒置变异
# 1. 在染色体上随机的选择一对位置
# 2. 将这一对位置中间的值倒置
def MutateRM(chromo):
	#if random.random() > MUTATION_RATE:
		#return chromo

	MinSpanSize = 3
	beg, end = ChooseSection(len(chromo) - 1, MinSpanSize)

	TheSection = chromo[beg:end]
	TheSection.reverse()
	return chromo[:beg] + TheSection + chromo[end:]

# 倒置移位变异
# 1. 在染色体上随机的选择一对位置
# 2. 将这一对位置中间的值倒置
# 3. 将这一对位置中间的值随机插入到染色体其他位置
def MutateRDM(chromo):
	#if random.random() > MUTATION_RATE:
		#return chromo

	MinSpanSize = 3
	beg, end = ChooseSection(len(chromo) - 1, MinSpanSize)

	TheSection = chromo[beg:end]
	TheSection.reverse()

	TheLeft = chromo[:beg] + chromo[end:]

	randPos = random.randint(0, len(TheLeft) - 1) # 如果len(TheLeft) == 0，randint会报错

	newChromo = TheLeft[:randPos] + TheSection + TheLeft[randPos:]

	return newChromo

#print MutateRDM([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
#for i in xrange(100000):
	#MutateRDM([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])

#############################################################################################################
import copy

# 基于顺序的杂交算子
# 1. 随机选择2个以上的位置，如mum=[1,2,3,4,5], dad=[5,4,3,2,1]中选择位置(2,3)，则mum中被选中的是[3,4], dad中被选中的是[3,2]
# 2. ......再想想措辞吧
def CrossoverOBX(mum, dad):

	baby1 = copy.deepcopy(mum)
	baby2 = copy.deepcopy(dad)
	tempGens  = []
	Positions = []

	Pos = random.randint(0, len(mum) - 2) #先随机选择第一个

	while Pos < len(mum):
		Positions.append(Pos)
		tempGens.append(mum[Pos])
		Pos += random.randint(1, len(mum)-Pos)
	#print "Pos :", Positions
	#print "City:", tempGens
	cPos = 0
	for idx, gen in enumerate(baby2):
		for idx1, gen1 in enumerate(tempGens):
			if gen == gen1:
				#print "idx: ", idx, "city before:", baby2[idx], "city after:", tempGens[cPos]
				baby2[idx] = tempGens[cPos]
				cPos += 1
				break

	tempGens = []
	for idx in xrange(len(Positions)):
		tempGens.append(dad[Positions[idx]])

	cPos = 0
	for idx, gen in enumerate(baby1):
		for idx1, gen1 in enumerate(tempGens):
			if gen == gen1:
				baby1[idx] = tempGens[cPos]
				cPos += 1
				break

	return baby1, baby2

# 基于位置的杂交算子
def CrossoverPBX(mum, dad):
	Positions = []
	tempGens  = []
	Pos = random.randint(0, len(mum) - 2) #先随机选择第一个

	while Pos < len(mum):
		Positions.append(Pos)
		tempGens.append(mum[Pos])
		Pos += random.randint(1, len(mum)-Pos)
	#print Positions, tempGens
	baby1 = []
	for i in xrange(len(dad)):
		if i in Positions:
			baby1.append(mum[i])

		if dad[i] not in tempGens:
			baby1.append(dad[i])

	baby2 = []
	tempGens = []
	for idx in xrange(len(Positions)):
		tempGens.append(dad[Positions[idx]])

	for i in xrange(len(mum)):
		if i in Positions:
			baby2.append(dad[i])

		if mum[i] not in tempGens:
			baby2.append(mum[i])

	return baby1, baby2



if __name__ == "__main__":
	#print CrossoverPBX([1,2,3,4,5,6,7,8,9], [9,8,7,6,5,4,3,2,1])
	for i in xrange(100000):
		CrossoverPBX([1,2,3,4,5,6,7,8,9], [9,8,7,6,5,4,3,2,1])