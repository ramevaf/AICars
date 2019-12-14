'''
Created on 21.05.2019

@author: D.Ramonat
'''
import numpy as np
import pygame
import logging
from mySprite import MySprite

class Entity:
    '''
    an Entity represents a movable or non movable 2D object
    '''
    # varables in x,y coordinates
    a_xy = (0,0)     # pixels/s�
    v_xy = (0,0)     # pixels/s
    s_xy = (0,0)   # pixels
    # variables is polar coordinates
    d_phi_p = 0      # radial speed
    phi_p = 0        # rad
    a_p   = 0        # pixels/s�
    v_p   = 0        # pixels/s
    
    isMovable = True # is entity movable?
    
    def __init__(self, sprite, s_xy, isMovable = True):
        '''
        Constructor
        '''
        self.s_xy = np.asarray(s_xy)
        self.sprite = sprite
        self.isMovable = isMovable
        self.delta_s = 0
    
    def move(self, dt): 
        '''
        updates position variables depending on the entities acceleration and velocity. This
        function should be called once every game cycle
        '''
        if(self.isMovable):
            # update angle
            self.phi_p += self.d_phi_p*dt
            # update velocity in polar coorinates
            self.v_p  += self.a_p*dt # v = v0 + a * dt     
            # calculate xy component from polar velocity
            d_v_xy = (-np.sin(self.phi_p*np.pi/180)*self.v_p, -np.cos(self.phi_p*np.pi/180)*self.v_p)       
            
            # calculate velocity from accerlariton in xy coordinates
            self.v_xy += np.multiply(self.a_xy,dt) # v = v0 + a * dt
                   
            # calculate overall speed from polar and xy components in xy coordinates
            overallSpeed_xy = self.v_xy + d_v_xy
            # calculate new xy coordinates
            self.delta_s = np.multiply(overallSpeed_xy,dt)
            self.s_xy += self.delta_s # s = s0 + v * dt
        else:
            logging.warning("tried to move an unmovable object")
    
    def setdPhi_p(self, d_phi_p):
        '''
        sets the entities yaw rate at rad/s
        '''
        self.d_phi_p = d_phi_p
        
    def setPhi_p(self, phi_p):
        '''
        sets the entities yaw angle in rad
        '''
        self.phi_p = phi_p
    
    def setAccel_p(self, a_p):
        self.a_p = a_p

    def setAccel_xy(self, a_xy):
        '''
        sets the entities acceleration in x,y components
        '''
        self.a_xy = a_xy

    def setAccel_x(self, a_x):
        '''
        sets the entities acceleration x component
        '''
        self.a_xy[0] = a_x

    def setAccel_y(self, a_y):
        '''
        sets the entities acceleration y component
        '''
        self.a_xy[1] = a_y
        
    def setVelocity_p(self, v_p):
        '''
        sets the entities velocity in moving direction (polar)
        '''
        self.v_p = v_p
        
    def setVelocity_xy(self, v_xy):
        '''
        sets the entities velocity in x,y components
        '''
        self.v_xy = v_xy
        
    def setVelocity_x(self, v_x):
        '''
        sets the entities velocity x component
        '''
        self.v_xy[0] = v_x

    def setVelocity_y(self, v_y):
        '''
        sets the entities velocity y component
        '''
        self.v_xy[1] = v_y
        
    def draw(self, gameCanvas):
        '''
        draws the entities mySprite at the game canvas. This method should be called
        once every game cycle
        '''
        
        #self.sprite.rect.draw()

        self.sprite.draw(gameCanvas, self.s_xy, self.phi_p)
        
    def getSprite(self):
        '''
        returns the sprite assigned to this entity
        '''
        return self.sprite
    
       
        
        
        
        
    