'''
This module contains the GameLauncher class and its methods

Created on 21.05.2019

@author: D.Ramonat
'''
import pygame

from mySprite import MySprite
from carEntity import CarEntity
from parameterHandler import ParameterHandler as PAR
from aiCar import AICar
from camera import Camera
import evolution
import numpy as np

global endOfGame

class GameLauncher:
    '''
    the GameLauncher handles the gameplay logic for this game and the drawing o screen
    '''
    # setup gameScreen which is the window shown
    screen = pygame.display.set_mode((PAR.GameScreen_Width, PAR.GameScreen_Height))
    # setup gameCanvas which represents the total size of the course
    gameCanvas = pygame.Surface((PAR.GameCanvas_Width, PAR.GameCanvas_Height))
    # setup clock
    clock = pygame.time.Clock()

    circuitSprite = MySprite(PAR.Path_CircuitSprite)
    
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
         # init pygame.font used for displaying text onto the gamescreen
        pygame.font.init()
        # init game camera
        self.camera = Camera([PAR.GameCanvas_Width, PAR.GameCanvas_Height], [PAR.GameScreen_Width, PAR.GameScreen_Height])
        # init players car
        self.playerCar = CarEntity(PAR.Path_PlayerCarSprite)
        # fill canvas with solid white
        self.gameCanvas.fill(PAR.GameCanvas_Background)

        self.cars = []
        
        
    def runGenerations(self):
        '''
        creates generations of neuronal network drven cars until NN_NumGenerations is 
        reached. For each generation runGame is called as long as one AICar is alive
        ''' 
        # first generation of AIcars
        AIcarGen = [AICar(PAR.NN_NetSize) for i in range(PAR.NN_NumPopulationPerGen)]
        
        for genIdx in range(PAR.NN_NumGenerations):
            self.genIdx = genIdx
            
            print("starting generation " + str(genIdx))
            
            # for i in AIcarGen:
            #     print("ID: " + str(id(i)))
            
            
            AIcarBatches = self.splitListIntoBatch(AIcarGen, PAR.NN_MaxBatchSize)
            AIcarGen = []
            for batchIdx, batch in enumerate(AIcarBatches):
                self.batchIdx = batchIdx
                print("batch no: " + str(batchIdx))
                self.simulateBatch(batch)
                AIcarGen = AIcarGen + batch
            # for i in AIcarGen:
            #     print("dist: " + str(i.distanceTraveled))

            print("all of entities dead! evolving...")
            AIcarGen = evolution.evolveGeneration(AIcarGen)
            self.nextgen == False
            
        print("final generation reached. End of Game")
            
    def splitListIntoBatch(self, flist, batchSize):
        '''
        splits a list (of AIcars) into several smaller lists (=batches)
        '''
        arrs = []
        while len(flist) > batchSize:
            batch = flist[:batchSize]
            arrs.append(batch)
            flist = flist[batchSize:]
        arrs.append(flist)
        return arrs

    def simulateBatch(self, AIcarsBatch):
        '''
        simulates a batch of AIcars until all cars have died
        '''
        aliveStsList = [True]
        
        while (any(item == True for item in aliveStsList)):
            # as long as anyone is alive run game loop
            self.runGame(AIcarsBatch)
            # update list of alive flags
            aliveStsList = []
            for i in AIcarsBatch:
                # car is alive if alive bit is set and is not standing
                if (i.isAlive and (i.v_p > PAR.AICar_AliveMinSpeedThreshold)):
                    aliveStsList.append(True)
                else:
                    aliveStsList.append(False)
                
            if (self.nextgen == True):
                aliveStsList = [False]

    def runGame(self, AIcarsList):
        ''' 
        calculates the objects of the game for one cycle and handles drawing on screen
        '''
        # get difference time in s
        dt = self.clock.get_time()/1000.0

        # process user input
        self.runEventHandler()
        # fill canvas with racetrack color
        self.gameCanvas.fill(PAR.GameCanvas_Background)
        # draw circuit on canvas
        self.circuitSprite.draw(self.gameCanvas, (PAR.GameCanvas_Width/2, PAR.GameCanvas_Height/2), 0)
        # calculate car instances
        if(dt > 0.0):
            for i in AIcarsList:
                i.draw(self.gameCanvas)
                if (i.isAlive == True):
                    i.run(self.gameCanvas, self.circuitSprite)
                    # run simulation with a fixed speed because using a dynamic one (dt) messes up the simulation at every lag on my slow pc 
                    i.move(1.0/PAR.Game_MaxFramerate) 
                    

                    if (pygame.sprite.collide_mask(i.getSprite(), self.circuitSprite)):
                        # i.penalizeFitness()
                        i.kill()
                
            # slow down player car if off track
            if (pygame.sprite.collide_mask(self.playerCar.getSprite(), self.circuitSprite)):
                self.playerCar.maxSpeed = PAR.Car_OfftrackSpeed
            else:
                self.playerCar.maxSpeed = PAR.Car_MaxSpeed
            # calculate new position of players car entity
            self.playerCar.move(dt)
        
        # limit framerate
        # self.clock.tick(PAR.Game_MaxFramerate)
        self.clock.tick()
        # draw car on canvas
        self.playerCar.draw(self.gameCanvas)
        
        if (PAR.Camera_Mode == 'FollowAI'):
            # sort cars by traveled distance
            AIcarsList.sort(key=lambda x: x.fitness, reverse=True)
            # follow the first car which is alive
            for i in AIcarsList:
                if(i.isAlive == True):
                    # update camera position so it follows the best car
                    self.camera.update(i.s_xy)
                    break
        else:
            # update camera position so it follows players car
            self.camera.update(self.playerCar.s_xy)

        # scroll gamecanvas to apply camera offset
        self.gameCanvas.scroll(self.camera.getScreenOffsetX(), self.camera.getScreenOffsetY())
        # display gamecanvas on screen
        self.screen.blit(self.gameCanvas, (0,0))
        self.drawInfoBox()

        # update canvas and show on screen
        pygame.display.update()

    def drawInfoBox(self):
        # create textSurface for displaying some addtional information
        self.myfont = pygame.font.SysFont('Verdana', 10)
        color = (255, 255, 255)

        string = "Framerate:       " + str(self.getFrameRate())
        textSurface = self.myfont.render(string, False, color)
        self.screen.blit(textSurface,(10,10))
        
        string = "Generation No: " + str(self.genIdx)
        textSurface = self.myfont.render(string, False, color)
        self.screen.blit(textSurface,(10,20))
        
        string = "Batch No:         " + str(self.batchIdx+1) + "/" + str(int(np.ceil(PAR.NN_NumPopulationPerGen/PAR.NN_MaxBatchSize)))
        textSurface = self.myfont.render(string, False, color)
        self.screen.blit(textSurface,(10,30))

        
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
    
    def getFrameRate(self):
        '''
        returns the frame rate

        :returns: int in frames/second
        '''
        dt = self.clock.get_time()/1000
        frames = int(np.divide(1,dt))
        return frames