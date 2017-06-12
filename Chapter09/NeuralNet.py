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
		self._NumInputs = NumInputs + 1   # 注意這裡 + 1了
		self._Weights   = []
		self._Activation = 0.0
		self._Error = 0.0

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
	def __init__(self, NumInputs, NumOutputs, NeuronsPerHiddenLayer, LearningRate):
		self._NumInputs = NumInputs
		self._NumOutputs = NumOutputs
		self._NumHiddenLayers = 1
		self._NeuronsPerHiddenLyr = NeuronsPerHiddenLayer
		self._LearningRate = LearningRate
		self._ErrorSum = 9999.9
		self._Trained = False
		self._NumEpochs = 0
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
		return

	def InitializeNetwork(self):
		for i in xrange(self._NumHiddenLayers + 1):
			for n in xrange(self._Layers[i]._NumNeurons):
				for k in xrange(self._Layers[i]._Neurons[n]._NumInputs):
					self._Layers[i]._Neurons[n]._Weights[k] = random.random() - random.random()

		self._ErrorSum = 9999.9
		self._NumEpochs = 0
		return

	def Update(self, inputs):
		outputs = []

		Weight = 0

		if len(inputs) != self._NumInputs:
			print "Input Size not correct, current %d, expected: %d" % (len(inputs), self._NumInputs)
			return outputs

		for i in xrange(self._NumHiddenLayers + 1):
			if i > 0:
				inputs = copy.deepcopy(outputs)

			outputs = []
			Weight = 0

			for n in xrange(self._Layers[i]._NumNeurons):
				netinput = 0.0
				NumInputs = self._Layers[i]._Neurons[n]._NumInputs

				for k in xrange(NumInputs - 1):
					netinput += self._Layers[i]._Neurons[n]._Weights[k] * inputs[Weight]
					Weight += 1

				netinput += self._Layers[i]._Neurons[n]._Weights[NumInputs-1] * dBias

				self._Layers[i]._Neurons[n]._Activation = self.Sigmoid(netinput, 1.0)  # ACTIVATION_RESPONSE = 1.0
				outputs.append(self._Layers[i]._Neurons[n]._Activation)
				Weight = 0

		return outputs

	def NetworkTrainingEpoch(self, SetIn, SetOut):
		self._ErrorSum = 0

		for vec in xrange(len(SetIn)):
			outputs = self.Update(SetIn[vec])

			if len(outputs) == 0:
				return False

			for op in xrange(self._NumOutputs):
				err = (SetOut[vec][op] - outputs[op]) * outputs[op] * (1 - outputs[op])

				self._Layers[1]._Neurons[op]._Error = err

				self._ErrorSum += (SetOut[vec][op] - outputs[op]) * (SetOut[vec][op] - outputs[op])

				for i in xrange(len(self._Layers[1]._Neurons[op]._Weights) - 1):
					self._Layers[1]._Neurons[op]._Weights[i] += err*self._LearningRate*self._Layers[0]._Neurons[i]._Activation
				self._Layers[1]._Neurons[op]._Weights[-1] += err * self._LearningRate * dBias

			for i in xrange(len(self._Layers[0]._Neurons)):
				err = 0
				for j in xrange(len(self._Layers[1]._Neurons)):
					err += self._Layers[1]._Neurons[j]._Error * self._Layers[1]._Neurons[j]._Weights[i]

				err *= self._Layers[0]._Neurons[i]._Activation * (1 - self._Layers[0]._Neurons[i]._Activation)

				for w in xrange(self._NumInputs):
					self._Layers[0]._Neurons[i]._Weights[w] += err * self._LearningRate * SetIn[vec][w]
				self._Layers[0]._Neurons[i]._Weights[self._NumInputs] += err * dBias

		return True

	def Train(self, data, screen):
		SetIn = data.GetInputSet()
		SetOut= data.GetOutputSet()

		if len(SetIn) != len(SetOut) or len(SetIn[0]) != self._NumInputs or len(SetOut[0]) != self._NumOutputs:
			print "Inputs/Outputs length is invalid."
			return False

		self.InitializeNetwork()

		while self._ErrorSum > 0.003:
			if self.NetworkTrainingEpoch(SetIn, SetOut) == False:
				return False

			self._NumEpochs += 1

			# 這裡需要更新窗口
			print "Epoch: %d, ErrorSum: %f" % (self._NumEpochs, self._ErrorSum)
		self._Trained = True
		return True

	def Trained(self):
		return self._Trained

	def Error(self):
		return self._ErrorSum

	def Epoch(self):
		return self._NumEpochs

	def Sigmoid(self, netinput, response):
		return (1 / (1 + exp(-netinput / response)))