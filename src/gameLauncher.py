'''
Created on 21.05.2019

@author: D.Ramonat
'''
import pygame

from mySprite import MySprite
from carEntity import CarEntity
from parameterHandler import ParameterHandler as PAR
from aiCar import AICar
import evolution

global endOfGame

class GameLauncher:
    '''
    classdocs
    '''
    gameCanvas = pygame.display.set_mode((PAR.GameCanvas_Width,PAR.GameCanvas_Height))
    clock = pygame.time.Clock()
    circuitSprite = MySprite('sprites/Racetrack.png')
    
    leftPressed = False
    rightPressed = False
    upPressed = False
    downPressed = False
    numGen = 0
    
    nextgen = False
    start = False
    
    def __init__(self):
        '''
        Constructor
        '''
        # setup pygame window
        pygame.init()
        pygame.display.set_caption('AICars')
        # init players car
        self.playerCar = CarEntity('Sprites/PlayerCar.png')
        # fill canvas with solid white
        self.gameCanvas.fill(PAR.GameCanvas_Background)
        # draw circuit on canvas
        self.circuitSprite.draw(self.gameCanvas, (PAR.GameCanvas_Width/2, PAR.GameCanvas_Height/2), 0)
        
        
    def runGenerations(self):
         '''
        creates generations of neuronal network drven cars until NN_NumGenerations is 
        reached. For each generation runGame is called as long as one AICar is alive
        '''        
        self.cars = [AICar(PAR.NN_NetSize) for i in range(PAR.NN_NumPopulationPerGen)]

        #input("Press Enter to continue...")
             
        for generation in range(PAR.NN_NumGenerations):
            self.numGen = generation
            
            print("starting generation " + str(generation))
            
            # create a new generation            
            # initialize list to indicate generation is alive
            anyoneAlive = [True]
            
            while (any(item == True for item in anyoneAlive)):
                # as long as anyone is alive run game loop
                self.runGame()
                # update list of alive flags
                anyoneAlive = []
                for i in self.cars:
                    # car is alive if alive bit is set and is not standing
                    if (i.alive and (i.v_p > 0.1)):
                        anyoneAlive.append(True)
                    else:
                        anyoneAlive.append(False)
                    
                if (self.nextgen == True):
                    anyoneAlive = [False]
                
            print("all of entities dead! evolving...")
            
            self.cars = evolution.evolveGeneration(self.cars)                    
            self.nextgen == False
            
        print("final generation reached. End of Game")
            

    def runGame(self):
        ''' 
        calculates the objects of the game for one cycle
        '''
        # get difference time in s
        dt = self.clock.get_time()/1000
        # process user input
        self.runEventHandler()
        # fill canvas with solid white
        self.gameCanvas.fill(PAR.GameCanvas_Background)
        # draw circuit on canvas
        self.circuitSprite.draw(self.gameCanvas, (PAR.GameCanvas_Width/2, PAR.GameCanvas_Height/2), 0)
        # calculate car instances
        for i in self.cars:
            if (i.alive == True):
                i.run(self.gameCanvas)
                i.move(dt)
                i.draw(self.gameCanvas)
                    
                if (pygame.sprite.collide_mask(i.getSprite(), self.circuitSprite)):
                    i.kill()
                    i.draw(self.gameCanvas)
        
        self.clock.tick(30)
            
        # calculate new position of players car entity
        self.playerCar.move(dt)
        # draw car on canvas
        self.playerCar.draw(self.gameCanvas)
        # update canvas and show on screen
        pygame.display.update()         
        
    def runEventHandler(self):
        ''' 
        handles the inputs from the player to control the players car
        '''    
        for event in pygame.event.get():
            # user pressed the 'x'
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # process user controls via arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.leftPressed = True
                    self.playerCar.steerLeft()
                if event.key == pygame.K_RIGHT:
                    self.rightPressed = True
                    self.playerCar.steerRight()
                if event.key == pygame.K_UP:
                    self.upPressed = True
                    self.playerCar.pushThrottle()
                if event.key == pygame.K_DOWN:
                    self.downPressed = True
                    self.playerCar.pushBrake()   
                if event.key == pygame.K_0:
                    self.nextgen = True
                    self.start = True      
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.leftPressed = False
                    if (self.rightPressed == False):
                        self.playerCar.stopSteering()
                if event.key == pygame.K_RIGHT:
                    self.rightPressed = False
                    if (self.leftPressed == False):
                        self.playerCar.stopSteering()
                if event.key == pygame.K_UP:
                    self.upPressed = False
                    if (self.downPressed == False):
                        self.playerCar.roll()
                if event.key == pygame.K_DOWN:
                    self.downPressed = False
                    if (self.upPressed == False):
                        self.playerCar.roll()
                if event.key == pygame.K_0:
                    self.nextgen = False  
                    self.start = True    
        return
    