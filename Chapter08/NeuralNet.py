# -*- coding: utf-8 -*-
import random
import copy
from math import *

dBias = -1
dActivationResponse = 1

iNumInputs  = 5
iNumOutputs = 2
iNumHidden  = 1  
iNeuronsPerHiddenLayer = 10


class SNeuron(object):
	def __init__(self, NumInputs):
		self._NumInputs = NumInputs
		self._Weights   = []

		for i in xrange(self._NumInputs):
			self._Weights.append(random.random() - random.random()) #生成一个-1, 1之间的随机Weight
		return


class SNeuronLayer(object):
	def __init__(self, NumNeurons, NumInputsPerNeuron):
		self._NumNeurons = NumNeurons
		self._Neurons    = []

		for i in xrange(self._NumNeurons):
			self._Neurons.append(SNeuron(NumInputsPerNeuron))

		return


class CNeuralNet(object):
	def __init__(self, NumInputs=iNumInputs, NumOutputs=iNumOutputs, NumHidden=iNumHidden, NeuronsPerHiddenLayer=iNeuronsPerHiddenLayer):
		self._NumInputs = NumInputs
		self._NumOutputs = NumOutputs
		self._NumHiddenLayers = NumHidden
		self._NeuronsPerHiddenLyr = NeuronsPerHiddenLayer
		self._Layers = []

		self.CreateNet()

		return

	def CreateNet(self):
		if self._NumHiddenLayers > 0:
			# 第一个hidden layer
			self._Layers.append(SNeuronLayer(self._NeuronsPerHiddenLyr, self._NumInputs))
			# 其余的hidden layer
			for i in xrange(self._NumHiddenLayers - 1):
				self._Layers.append(SNeuronLayer(self._NeuronsPerHiddenLyr, self._NeuronsPerHiddenLyr))

			# 输出层
			self._Layers.append(SNeuronLayer(self._NumOutputs, self._NeuronsPerHiddenLyr))

		else:
			self._Layers.append(SNeuronLayer(self._NumOutputs, self._NumInputs))

	def GetWeights(self):
		weights = []
		for i in xrange(self._NumHiddenLayers + 1):
			for j in xrange(self._Layers[i]._NumNeurons):
				for k in xrange(self._Layers[i]._Neurons[j]._NumInputs):
					weights.append(self._Layers[i]._Neurons[j]._Weights[k])

		return weights

	def PutWeights(self, weights):
		weightIdx = 0
		for i in xrange(self._NumHiddenLayers + 1):
			for j in xrange(self._Layers[i]._NumNeurons):
				for k in xrange(self._Layers[i]._Neurons[j]._NumInputs):
					self._Layers[i]._Neurons[j]._Weights[k] = weights[weightIdx]
					weightIdx += 1

	def GetNumberOfWeights(self):
		weightIdx = 0
		for i in xrange(self._NumHiddenLayers + 1):
			for j in xrange(self._Layers[i]._NumNeurons):
				for k in xrange(self._Layers[i]._Neurons[j]._NumInputs):
					weightIdx += 1
		return weightIdx

	def Update(self, inputs):
		outputs = []
		weightIdx = 0

		if len(inputs) != self._NumInputs:
			print "inputs num %d, expected inputs num %d" % (len(inputs), self._NumInputs)
			return outputs

		for i in xrange(self._NumHiddenLayers + 1):
			if i > 0:
				inputs = copy.deepcopy(outputs)

			outputs = []
			weightIdx  = 0

			for j in xrange(self._Layers[i]._NumNeurons):
				netinput = 0.0
				NumInputs = self._Layers[i]._Neurons[j]._NumInputs

				for k in xrange(NumInputs-1):
					netinput  += (self._Layers[i]._Neurons[j]._Weights[k] * inputs[weightIdx])
					weightIdx += 1

				netinput += (self._Layers[i]._Neurons[j]._Weights[NumInputs-1] * dBias) #dBias = -1

				outputs.append(self.Sigmoid(netinput, dActivationResponse)) # dActivationResponse = 1
				weightIdx = 0

		return outputs

	def Sigmoid(self, netinput, response):
		return (1 / (1 + exp(-netinput / response)))

	def CalculateSplitPoints(self):
		SplitPoints = []
		WeightCounter = 0

		for i in xrange(self._NumHiddenLayers + 1):
			for j in xrange(self._Layers[i]._NumNeurons):
				for k in xrange(self._Layers[i]._Neurons[j]._NumInputs):
					WeightCounter += 1
				SplitPoints.append(WeightCounter - 1)
		print SplitPoints
		return SplitPoints


# test code
#a = CNeuralNet(20, 20, 4, 20)
#inputaaa = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
#print len(inputaaa)
#print a.Update(inputaaa)