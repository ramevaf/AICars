'''
This module contains the AICar class and its methods

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
    isAlive = True
    distanceTraveled = 0.0
    isParent = False # AICar is a parent for others

    def __init__(self, netSize, isParent = False):
        '''
        Constructor, initializes the neuronal network

        :param netSize: list of int defining the structure of the neuronal net
        '''
        if (isParent == True):
            CarEntity.__init__(self, custSprite=PAR.Path_ParentCarSprite)
        else:
            CarEntity.__init__(self)

        self.netSize = netSize
        self.net = NeuronalNetwork(netSize)
        self.distanceTraveled = 0
        
    def run(self, gameCanvas, circuitSprite):
        '''
        makes the car driving with control of the neuronal network input of the 
        network are 5 distances measured towards the border of the drivable 
        corridor (DTC-distance to collision) in certain angles (default 90, 45,
        0 (driving direction), -45 and -90 degrees)

        :param gameCanvas: the GameCanvas object where the AICar is represented
        :param circuitSprite: the MySprite object defining the borders of the track
        '''
        if (self.isAlive == True):
            # create a vector with all DTCs
            x = np.array([])
            for DTCAngle in PAR.AICar_DTCAngles:
                x = np.append(x, self.getDTC(self.phi_p+DTCAngle, circuitSprite))
            
            # add own speed to input if acceleration shall be taken into account
            if (PAR.AICar_Controlmode == '5DirSteer'):
                x = np.append(x, self.v_p)

            # calculate feed forward path in the NN and return the output
            # since the network has two output neuron the return value consists
            # of only two values
            ffw = self.net.feedforward(x.reshape(-1,1))
            # which will be used as steering input of the vehilces
            self.control(ffw)#[0], ffw[1], ffw[2])
        else:
            self.stop()
        # count the traveled distance. Will be used as fitnes value    
        self.distanceTraveled += np.linalg.norm(self.delta_s)
            
    def control(self, netOutput):
        '''
        converts the output of the neuronal network to the driving comands
        of the cars
        
        in a first atempt the NN will only control the steering and the
        thotle will be pushed all the time

        :param first: fist input command
        :param second: second input command
        '''
        # convert into 1-dim array
        [netOutput] = netOutput.reshape(1,self.netSize[-1])

        if (PAR.AICar_Controlmode == 'Simple2DirSteer'):
            # 2 Output neurons required: 
            # : index 0 -> steer left
            # : index 1 -> steer rigth
            # : throttle always pressed, no brakes
            action = self.getIndexOfMax(netOutput)

            if(action == 0):
                self.steerLeft(PAR.Car_SteeringAccel*(netOutput[0]))
            elif(action == 1):
                self.steerRight(PAR.Car_SteeringAccel*(netOutput[1]))
            self.pushThrottle()
        if (PAR.AICar_Controlmode == 'Simple3DirSteer'):
            # 3 Output neurons required: 
            # : index 0 -> steer left
            # : index 1 -> no steering
            # : index 2 -> steer rigth
            # : throttle always pressed, no brakes
            action = self.getIndexOfMax(netOutput)

            if(action == 0):
                self.steerLeft(PAR.Car_SteeringAccel*(netOutput[0]))
            if(action == 1):
                self.stopSteering()
            elif(action == 2):
                self.steerRight(PAR.Car_SteeringAccel*(netOutput[2]))
            self.pushThrottle()
        if (PAR.AICar_Controlmode == '5DirSteer'):
            # 3 Output neurons required: 
            # : index 0 -> steer left
            # : index 1 -> no steering
            # : index 2 -> steer rigth
            # : index 3 -> throttle
            # : index 4 -> brake
            steerAction = self.getIndexOfMax(netOutput[:3])
            if(steerAction == 0):
                self.steerLeft(PAR.Car_SteeringAccel*(netOutput[0]))
            if(steerAction == 1):
                self.stopSteering()
            elif(steerAction == 2):
                self.steerRight(PAR.Car_SteeringAccel*(netOutput[2]))
            
            accelAction = self.getIndexOfMax(netOutput[3:5])
            if(accelAction == 0):
                self.pushThrottle()
            if(accelAction == 1):
                self.pushBrake()

    def getIndexOfMax(self, values):
        return np.argmax(values)
        
    def kill(self):
        '''
        kills the entity
        '''
        self.isAlive = False
        self.stop()
        
    def __str__(self):
        s = "\nAlive: " + str(self.isAlive)
        s += "\ndistanceTraveled: " + str(self.distanceTraveled)
        return s
