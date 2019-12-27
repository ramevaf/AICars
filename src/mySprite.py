'''
Created on 21.05.2019

@author: D.Ramonat
'''
import pygame
import numpy as np

class MySprite(pygame.sprite.Sprite):
    '''
    this class represents a sprite. A sprite is like an image which can be displayed at
    a specified positon on the game canvas and can be rotated etc.
    '''

    def __init__(self, path2Image):
        '''
        Constructor
        '''
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = pygame.image.load(path2Image).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
    def getWidth(self):
        '''
        returns sprite width in pixel
        '''
        size = self.image.get_size()
        return size[0]
    
    def getHeight(self):
        '''
        returns sprite height in pixel
        '''
        size = self.image.get_size()
        return size[1]

    def getImage(self):
        '''
        returns image
        '''
        return self.image
    
    def getRotatedImage(self, phi):
        '''
        rotates image by a given angle phi (in rad) and returns rotated image
        '''
        return (pygame.transform.rotate(self.image, phi))
    
#     def scaleImage(self, factor):
#         '''
#         scales image by a given factor and returns scaled iage
#         '''
#         newSize = ( np.int(self.getWidth()*factor), np.int(self.getHeight()*factor) )
#         return (pygame.transform.scale(self.__image, (100,100)))
        
        
    def draw(self, gameCanvas, s_xy, phi = 0):
        '''
        draws the sprite on the gameCanvas at position s_xy and at angle phi
        '''
        # rotate image
        rotImg = self.getRotatedImage(phi)
        # get rotated image size
        rotImgSize = rotImg.get_size()
        # correct image coordinates to drav image centered about s_xy
        corr_s_xy = np.array(s_xy)-np.divide(rotImgSize, 2)
        # update sprit rect        
        self.rect = pygame.Rect(corr_s_xy[0], corr_s_xy[1], rotImgSize[0], rotImgSize[1])
        # update mask
        self.mask = pygame.mask.from_surface(rotImg) 
        
        gameCanvas.blit(rotImg, corr_s_xy)
