'''
Created on 28.05.2019

@author: D.Ramonat
'''
import numpy as np
import pygame

from carEntity import CarEntity
from neuronalNetwork import NeuronalNetwork
from parameterHandler import ParameterHandler as PAR


class AICar(CarEntity):
    '''
    a AIcar represents a AI controlled car in this game :)
    '''
    alive = True
    distanceTraveled = 0.0

    def __init__(self, netSize):
        '''
        Constructor, initializes the neuronal network
        '''
        CarEntity.__init__(self)
        self.net = NeuronalNetwork(netSize)
        self.distanceTraveled = 0
        
    def run(self, gameCanvas, circuitSprite):
        '''
        makes the car driving with control of the neuronal network input of the 
        network are 5 distances measured towards the border of the drivable 
        corridor (DTC-distance to collision) in certain angles (default 90, 45,
        0 (driving direction), -45 and -90 degrees)
        '''
        if (self.alive == True):
            # create a vector with all DTCs
            x = np.array([])
            for DTCAngle in PAR.AICar_DTCAngles:
                x = np.append(x, self.getDTC(self.phi_p+DTCAngle, circuitSprite))

            # calculate feed forward path in the NN and return the output
            # since the network has two output neuron the return value consists
            # of only two values
            ffw = self.net.feedforward(x.reshape(-1,1))
            # which will be used as steering input of the vehilces
            self.control(ffw[0], ffw[1])#, ffw[1])
        else:
            self.stop()
        # count the traveled distance. Will be used as fitnes value    
        self.distanceTraveled += np.linalg.norm(self.delta_s)
            
    def control(self, first, second = 0):
        '''
        converts the output of the neuronal network to the driving comands
        of the cars
        
        in a first atempt the NN will only control the steering and the
        thotle will be pushed all the time
        '''
       
        # Option 1: 
#         if (first[0] > second[0]):
#             if (first[0] > PAR.AICar_SteeringThreshold): #if input value crosses a threshold the car will steer
#                 self.steerLeft()
#         else:
#             if (second[0] > PAR.AICar_SteeringThreshold):
#                 self.steerRight()
#         self.pushThrottle()

        # Option 2:
        if (first[0] > second[0]):
            if (first[0] > PAR.AICar_SteeringThreshold):
                self.steerLeft(3000*(first[0]))
        else:
            if (second[0] > PAR.AICar_SteeringThreshold):
                self.steerRight(3000*(second[0]))
        self.pushThrottle()
        
        # Option 3:
#         self.steerLeft(3000*(first[0]-0.5))
#         if (second[0] > 0.1):
#             self.pushThrottle()

        
        
    def kill(self):
        '''
        kills the entity
        '''
        self.alive = False
        self.stop()
        
    def __str__(self):
        s = "\nAlive: " + str(self.alive)
        s += "\ndistanceTraveled: " + str(self.distanceTraveled)
        return s
