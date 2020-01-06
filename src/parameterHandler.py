'''
This module contains the ParameterHandler class and its methods

Created on 21.05.2019

@author: D.Ramonat
'''
class ParameterHandler:
    '''
    stores a lot of game specific parameters
    '''
    # gameScreen
    GameScreen_Width = 800      # pixel
    GameScreen_Height  = 600    # pixel

    # Camera
    Camera_Mode = 'FollowAI' # ['FollowAI', 'FollowPlayer']

    # gamecanvas
    GameCanvas_Width = 2000      # pixel
    GameCanvas_Height  = 1500    # pixel
    GameCanvas_Background = (200, 200, 200) #color value of the track
    GameCanvas_StartingPoint = [1650.0,1350.0] #starting position of the cars
    GameCanvas_StartingAngle = 95.0 # starting angle of the cars
    
    # rar entity
    Car_SteeringAccel =     3000  # degrees/s^2
    Car_MaxSteeringSpeed =  200   # degrees/s
    Car_ThrottleAccel =     200   # pixel/s^2
    Car_BrakeAccel =        -500  # pixel/s^2
    Car_AirRestAccel =      -50   # pixel/s^2
    Car_MaxSpeed =          250   # pixel/s
    Car_OfftrackSpeed =     150   # pixel/s
    Car_DTCStepSize = 7
    
    AICar_DTCAngles = [-90,-45,0,45,90]
    AICar_SteeringThreshold = 0.1
    AICar_Controlmode = 'Simple3DirSteer' # ['Simple2DirSteer', 'Simple3DirSteer', '5DirSteer']
    
    NN_NumGenerations = 100
    NN_NumPopulationPerGen = 50
    NN_mutationRate = 0.2
    NN_crossoverRate = 0.35
    NN_retainRateGood = 0.2
    NN_retainRateBad = 0.05
    NN_NetSize = [5,20,10,2]
    
    # Override contolmode specific parameters
    if (AICar_Controlmode == 'Simple3DirSteer'):
        NN_NetSize = [5,20,10,3]
    if (AICar_Controlmode == '5DirSteer'):
        NN_NetSize = [6,30,20,5]
        Car_MaxSpeed = 500
    
    
    def __init__(self):
        '''
        Constructor
        '''
        
