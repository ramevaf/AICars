'''
This module contains the CarEntity class which adds some car specific
commands to the Entity class

Created on 28.05.2019

@author: D.Ramonat
'''
import numpy as np
from entity import Entity
from mySprite import MySprite
from parameterHandler import ParameterHandler as PAR

class CarEntity(Entity):
    '''
    a carEntity represents a car in this game :)
    '''
    isSteering = 0
    steeringAccel = 0
    maxSpeed = PAR.Car_MaxSpeed

    def __init__(self, custSprite = 'sprites/car.png', isMovable = True):
        '''
        Constructor

        :param custSprite: a given MySprite object to be used to draw this object
        :param isMovable: boolean value allows to generate non movable cars because why not?
        '''
        self.s_xy = PAR.GameCanvas_StartingPoint
        self.phi_p = PAR.GameCanvas_StartingAngle       
        sprite = MySprite(custSprite)
        Entity.__init__(self, sprite, self.s_xy, isMovable = True)
        
    def steerLeft(self, steeraccel = PAR.Car_SteeringAccel):
        '''
        makes the car steer left

        :param steeraccel: steering acclereration given in degrees/s^2
        '''
        self.steeringAccel = steeraccel
        self.isSteering = True      
        
    def steerRight(self, steeraccel = PAR.Car_SteeringAccel):
        '''
        makes the car steer right

        :param steeraccel: steering acclereration given in degrees/s^2
        '''
        self.steeringAccel = -steeraccel     
        self.isSteering = True      

    def pushThrottle(self):
        '''
        makes the car accelerate
        '''
        self.isBraking = False
        self.a_p = PAR.Car_ThrottleAccel
    
    def pushBrake(self):
        '''
        brakes the car
        '''
        self.isBraking = True
        self.a_p = PAR.Car_BrakeAccel
        
    def roll(self):
        '''
        let the car roll with drag only
        '''
        self.isBraking = False
        self.a_p = PAR.Car_AirRestAccel
        
    def stopSteering(self):
        '''
        makes the car steer straight again
        '''
        if (self.d_phi_p > 0):
            self.steeringAccel = -PAR.Car_SteeringAccel
        else:
            self.steeringAccel = PAR.Car_SteeringAccel     
        self.isSteering = False
        
    def stop(self):
        '''
        sets velocity and steering to zero
        '''
        self.steeringAccel = 0
        self.v_p = 0
        self.a_p = 0
    
    def move(self, dt):
        '''
        move function is adapted to add a steering acceleration

        :param dt: delta time between each call in ms
        '''
        # process steering
        if (self.isSteering == False):
            # stop steering at 0 
            if (self.d_phi_p > 0):
                self.d_phi_p += self.steeringAccel*dt
                self.d_phi_p = np.clip(self.d_phi_p, 0, PAR.Car_MaxSteeringSpeed)
            else:
                self.d_phi_p += self.steeringAccel*dt
                self.d_phi_p = np.clip(self.d_phi_p, -PAR.Car_MaxSteeringSpeed, 0)
            
            if (self.d_phi_p == 0):
                self.steeringAccel = 0
                
        else:
            self.d_phi_p += self.steeringAccel*dt
            self.d_phi_p = np.clip(self.d_phi_p, -PAR.Car_MaxSteeringSpeed, PAR.Car_MaxSteeringSpeed)
        
        # calculte speed dependent steering
        steeringFac = self.v_p/(PAR.Car_MaxSpeed/3) # maximum steering at 1/3 of maxspeed
        steeringFac = np.clip(steeringFac, 0, 1)
        
        self.d_phi_p = self.d_phi_p*steeringFac 
        Entity.move(self, dt)
        
        # stop braking at standstill
        if (self.v_p < 0):
            self.v_p = 0
            self.a_p = 0
            
        self.v_p = np.clip(self.v_p, 0, self.maxSpeed)
        
    def getDTC(self, phi_p, circuitSprite):
        '''
        calculates the distance to collision starting at the current position and pointing
        towards the phi_p value

        :param phi_p: direction in which the collision shall be calculated given degrees 
                note: if the distance to collision in driving direction shall be calculated
                      phi_p must be given as absolute value  the acutal phi_p) and not to zero
        :param circuitSprite: MySprite object containing the borders of the driving course
        :returns: int value of distance to first collision in pixel
        '''
        # calculate step size for distance to collision calculation in xy coordinates
        d_s_xy = (-np.sin(np.deg2rad(phi_p)), -np.cos(np.deg2rad(phi_p)))
        # accelerate step size
        d_s_xy += np.multiply(d_s_xy, PAR.Car_DTCStepSize)
        new_s_xy = self.s_xy
        # calculate new step position, skip the first pixel to avoid that the car sprite itself will be detected
        
        
        # when there is no road anymore then start counting the distance to colission
        dtc = 0

        # prevent pixel acces out of range
        new_s_xy[0] = np.clip(new_s_xy[0], 1, PAR.GameCanvas_Width-1)
        new_s_xy[1] = np.clip(new_s_xy[1], 1, PAR.GameCanvas_Height-1)
        
        # ... and count as long as road mask is not set         
        while (True != circuitSprite.mask.get_at(new_s_xy.astype(int))):
            new_s_xy = new_s_xy + d_s_xy
            # prevent pixel acces out of range
            new_s_xy[0] = np.clip(new_s_xy[0], 1, PAR.GameCanvas_Width-1)
            new_s_xy[1] = np.clip(new_s_xy[1], 1, PAR.GameCanvas_Height-1)

            dtc+=1
        # print("dtc: " + str(dtc))
        return dtc
        
        
        