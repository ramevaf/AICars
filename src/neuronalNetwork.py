'''
Created on 29.09.2019

@author: D.Ramonat
'''
import numpy as np

class NeuronalNetwork:

    def __init__(self, structure):
        
        '''The list ``structure`` contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron.'''
        
        self.numOfLayers = len(structure)
        self.structure = structure
        
        # create an array for the biases. There will be no biases for the input layeer.
        # If for example the structure of the NN is [2,3,1] then there will be biases 
        # for the last two layers means the size of the biases array is [3,1]
        # The biases are initialized randomly with a normal distribution with variance 1
        # so the value are between -1 and 1
        self.biases = [np.random.randn(y, 1) for y in structure[1:]]
        # store number of biases overall. In the given example this must be 4
        self.numOfBiases = sum(structure[1:])
        
        # create an array for the weigths. There are no weights for the input layer. Each
        # neuron in a hiden layer n(l) is conneced to each neuron of the layer before n(l-1)
        # That means for the example of a net wihh structure [2,3,1] there is 2 weights for
        # each neuron in the hidden layer and 3 weights for the neuron in the output layer
        # so overall [[2,2,2],3]. Again the weights are initilaized randomly similar to the 
        # biases
        self.weights = [np.random.randn(y, x) for x, y in zip(structure[:-1], structure[1:])]
        # store number of weigths for the hidden layers
        numOfHiddenLayers = self.numOfLayers-2 # minus input and output
        self.numOfWeights = sum([self.weights[i].size for i in range(numOfHiddenLayers)])
                
    def feedforward(self, input):
        '''Return the output of the network for a given input.'''
        for biases, weights in zip(self.biases, self.weights):
            # use result as new input for next cycle
            input = self.sigmoid(np.dot(weights,input)+biases)
        return input

    def sigmoid(self, x):
        '''The sigmoid function used as activation function for the neurons'''
        z = 1/(1 + np.exp(-x)) 
        return z