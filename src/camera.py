'''
This module contains the Entity class and its methods

Created on 14.12.2019

@author: D.Ramonat
'''
import numpy as np

class Camera:
    def __init__(self, totalGameCanvasSize, ScreenSize):
        '''
        Constructor

        :param totalGameCanvasSize: size of the game canvas (full track) as list of int
        :param ScreenSize: size of visual window as list of int
        '''
        self.totalGameCanvasSize = np.array(totalGameCanvasSize)
        self.ScreenSize = np.array(ScreenSize)
        self.halfScreenSize = self.ScreenSize/2
        initPos = self.totalGameCanvasSize/2
        self.position = initPos

    def update(self, newPos):
        '''
        sets the positions of the camera object in regards to the gameCanvas 

        :param newPos: list of int indicating the absolute position where the camera 
                       should direct to
        '''
        # limit the new position of the camera so if will be not outside of the gamecanvas
        # first calculate a helper array with the min and max values
        clipingVal = (self.halfScreenSize, self.totalGameCanvasSize-self.halfScreenSize)
        # apply values
        self.position[0] = np.clip(newPos[0], clipingVal[0][0], clipingVal[1][0])
        self.position[1] = np.clip(newPos[1], clipingVal[0][1], clipingVal[1][1])

        # offset = middle of screen - camera position
        self.screenOffset = self.halfScreenSize-np.array(self.position)

    def getScreenOffsetX(self):
        '''
        returns the offset between camera position and the middle of the gameCanvas 
        in x direction

        :returns: int in pixel
        '''
        return int(self.screenOffset[0])

    def getScreenOffsetY(self):
        '''
        returns the offset between camera position and the middle of the gameCanvas 
        in y direction

        :returns: int in pixel
        '''
        return int(self.screenOffset[1])