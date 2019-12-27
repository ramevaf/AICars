'''
Created on 21.05.2019

@author: D.Ramonat
'''
class ParameterHandler:
    '''
    classdocs
    '''
    # gameScree
    GameScreen_Width = 600      # pixel
    GameScreen_Height  = 400    # pixel

    # gamecanvas
    GameCanvas_Width = 800      # pixel
    GameCanvas_Height  = 600    # pixel
    GameCanvas_Background = (255, 255, 255)
    GameCanvas_CircuitGrass = (1,157,1)
    
    # rar entity
    Car_SteeringAccel =     1200  # rad/s�
    Car_MaxSteeringSpeed =  200   # rad/s
    Car_ThrottleAccel =     200   # pixel/s�
    Car_BrakeAccel =        -500  # pixel/s�
    Car_AirRestAccel =      -50   # pixel/s�
    Car_MaxSpeed =          250   # pixel/s
    
    AICar_DTCAngles = [-90,-45,0,45,90]
    AICar_SteeringThreshold = 0.1
    
    NN_NumGenerations = 100
    NN_NumPopulationPerGen = 20
    NN_NetSize = [5,20,10,2]
    NN_mutationRate = 0.2
    NN_crossoverRate = 0.35
    NN_retainRateGood = 0.2
    NN_retainRateBad = 0.05
    
    
    
    def __init__(self):
        '''
        Constructor
        '''
        
