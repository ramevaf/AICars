'''
main module. just runs the gameLauncher

Created on 21.05.2019

@author: D.Ramonat
'''
from gameLauncher import GameLauncher

if __name__ == '__main__':
    GL = GameLauncher()
    GL.runGenerations()
    #TODO run game even after last generation has died
    while(True):
        GL.runGame()