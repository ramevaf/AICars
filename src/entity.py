'''
This module contains the Entity class and its methods

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
    phi_p = 0        # degrees
    a_p   = 0        # pixels/s�
    v_p   = 0        # pixels/s
    
    isMovable = True # is entity movable?
    
    def __init__(self, sprite, s_xy, isMovable = True):
        '''
        Constructor

        :param sprite: the sprite which shall be assigned to this entity
        :param s_xy: inital position of the entity given as list or tupel
        :param isMovable: boolean value defining whether the entity is movable
        '''
        self.s_xy = np.asarray(s_xy)
        self.sprite = sprite
        self.isMovable = isMovable
        self.delta_s = 0
    
    def move(self, dt): 
        '''
        updates position depending on the entities acceleration and velocity. This
        function should be called once every game cycle

        :param dt: delta time between each call in ms
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
        sets the entities yaw rate

        :param  d_phi_p: yaw rate given in degrees/s
        '''
        self.d_phi_p = d_phi_p
        
    def setPhi_p(self, phi_p):
        '''
        sets the entities yaw angle

        :param  phi_p: yaw angle in degrees
        '''
        self.phi_p = phi_p
    
    def setAccel_p(self, a_p):
        '''
        sets the entities acceleration in polar coordinates

        :param  a_p: acceleration in polar coordinates give in pixel/s²
        '''
        self.a_p = a_p

    def setAccel_xy(self, a_xy):
        '''
        sets the entities acceleration in xy coordinates

        :param  a_xy: acceleration give as numpy array in xy coordinates
                      give in pixel/s²
        '''
        self.a_xy = a_xy

    def setVelocity_p(self, v_p):
        '''
        sets the entities velocity in moving direction (polar)

        :param v_p: velocity in pixel/s
        '''
        self.v_p = v_p
        
    def setVelocity_xy(self, v_xy):
        '''
        sets the entities velocity in xy coordintates

        :param v_p: velocity in pixel/s
        '''
        self.v_xy = v_xy
        
    def draw(self, gameCanvas):
        '''
        draws the entities Sprite at the Gamecanvas

        :param gameCanvas: GameCanvas object to draw on
        '''
        self.sprite.draw(gameCanvas, self.s_xy, self.phi_p)
        
    def getSprite(self):
        '''
        returns the sprite assigned to this entity

        :returns: MySprite object
        '''
        return self.sprite
    
       
        
        
        
        
    