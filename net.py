import numpy as np
import math
import random

def sigmoid(x):
	return 1 / ( 1 + np.exp(-1 * x))

def relu(x):
    a = x
    a[x < 0] = 0
    return a
	
class Specimen:
	min_weight = -0.1
	max_weight  = 0.1

	def __init__(self, inputs, nr_layer1, nr_layer2):
		self.l1_weights = np.random.uniform(low=Specimen.min_weight, high=Specimen.max_weight, size=(inputs, nr_layer1))
		self.l2_weights = np.random.uniform(low=Specimen.min_weight, high=Specimen.max_weight, size=(nr_layer1, nr_layer2))
		self.out_weights = np.random.uniform(low=Specimen.min_weight, high=Specimen.max_weight, size=(nr_layer2, 1))
		self.score = 0
		
	def output(self, input_vector):
		l1_out = np.matmul(input_vector, self.l1_weights)
		l1_out = relu(l1_out)
		l2_out = np.matmul(self.l1_weights, self.l2_weights)
		l2_out = relu(l2_out)
		return sigmoid(np.matmul(self.l2_weights, self.out_weights))
		
a = Specimen(2, 2, 2)
print(a.output(np.array([[2, 3]])))
