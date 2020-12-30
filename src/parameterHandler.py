'''
This module contains the ParameterHandler class and its methods

Created on 21.05.2019

@author: D.Ramonat
'''
import os
dirname = os.path.dirname(__file__)

class ParameterHandler:
    '''
    stores a lot of game specific parameters
    '''
    # paths
    Path_CircuitSprite = os.path.join(dirname, '..\sprites\Circuit.png')
    Path_PlayerCarSprite = os.path.join(dirname, '..\sprites\PlayerCar.png')
    Path_ParentCarSprite = os.path.join(dirname, '..\sprites\Parentcar.png')
    Path_CarSprite = os.path.join(dirname, '..\sprites\Car.png')

    # gameScreen
    GameScreen_Width = 800      # pixel
    GameScreen_Height  = 600    # pixel

    # Camera
    Camera_Mode = 'FollowAI' # ['FollowAI', 'FollowPlayer']

    # Game Overall
    Game_MaxFramerate = 15

    # gamecanvas
    GameCanvas_Width = 2000      # pixel
    GameCanvas_Height  = 1500    # pixel
    GameCanvas_Background = (200, 200, 200) #color value of the track
    GameCanvas_StartingPoint = [1650.0,1350.0] #starting position of the cars
    # GameCanvas_StartingPoint = [1040.0,115.0] #starting position of the cars
    GameCanvas_StartingAngle = 95.0 # starting angle of the cars clockwise
    # GameCanvas_StartingAngle = 275.0 # starting angle of the cars counterclockwise
    
    # Car entity
    Car_SteeringAccel =     3000  # degrees/s^2
    Car_MaxSteeringSpeed =  200   # degrees/s
    Car_ThrottleAccel =     200   # pixel/s^2
    Car_BrakeAccel =        -200  # pixel/s^2
    Car_AirRestAccel =      -50   # pixel/s^2
    Car_MaxSpeed =          250   # pixel/s
    Car_OfftrackSpeed =     150   # pixel/s
    Car_DTCStepSize = 7
    
    AICar_AliveMinSpeedThreshold = 5 # pixel/s
    AICar_DTCAngles = [-90,-45,0,45,90]
    AICar_SteeringThreshold = 0.1
    AICar_Controlmode = '5DirSteer' # ['Simple2DirSteer', 'Simple3DirSteer', '4DirSteer', '5DirSteer']
    
    NN_NumGenerations = 99999
    NN_NumPopulationPerGen = 300
    NN_MaxBatchSize = 100
    NN_mutationRate = 0.15
    NN_crossoverRate = 0.4
    NN_retainRateGood = 0.05
    NN_retainRateBad = 0.01
    NN_NetSize = [0]
    
    # Override contolmode specific parameters
    if (AICar_Controlmode == 'Simple2DirSteer'):
        NN_NetSize = [5,4,2]
    if (AICar_Controlmode == 'Simple3DirSteer'):
        NN_NetSize = [5,4,3]
    if (AICar_Controlmode == '5DirSteer'):
        NN_NetSize = [13,30,10,6]
        Car_MaxSpeed = 500
    if (AICar_Controlmode == '4DirSteer'):
        NN_NetSize = [6,10,4]
        Car_MaxSpeed = 500
    
    
    def __init__(self):
        '''
        Constructor
        '''
        
