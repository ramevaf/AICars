'''
Created on 29.09.2019

@author: D.Ramonat
'''
import random
import copy
from aiCar import AICar
from parameterHandler import ParameterHandler as PAR

        
def evolveGeneration(generation):
    # sort generation list by traveled distance descending 
    generation.sort(key=lambda x: x.distanceTraveled, reverse=True)
    #parentList = sorted(generation, key=lambda x: x.distanceTraveled, reverse=True)
    
    # calculate how many to keep as parents for the next gen depending on the retain rate
    numToKeep = int(PAR.NN_NumPopulationPerGen*PAR.NN_retainRateGood)
    # keep only the best ones as parents
    parentList = generation[:numToKeep]
        
    # keep also a random number of loosers to make sure we don't optimize for a local minimum
    maxNumOfLoosersToKeep = int(PAR.NN_NumPopulationPerGen*PAR.NN_retainRateBad)
    for _ in range(random.randint(0, maxNumOfLoosersToKeep)):
        parentList.append(random.choice(generation[numToKeep:]))
    
    # our parents will be the fist of the new generation
    nextGen = []
    for i in parentList:
        newAICar = AICar(PAR.NN_NetSize)
        newAICar.net = i.net
        nextGen.append(newAICar)
#         print ("  par" + str(i.net))
    print ("  kept " + str(len(nextGen)) + "entities as parents")
    
    
    # breed new childs as long as current population is less than the population size
    while len(nextGen) < PAR.NN_NumPopulationPerGen:
        # select father and mother
        father = random.choice(nextGen)
        mother = random.choice(nextGen)
        # no inbreeding
        if father != mother:
            child = crossover(father, mother)
            child = mutation(child)
            nextGen.append(child)
    
    # make sure aive bits from parents are reset to True
    for i in nextGen:
        i.alive = True 
        
    
#     for i in nextGen:
#         print ("  nex" + str(i.net))     
    return nextGen

def crossover(father, mother):
    '''
    @father = neural-net object representing father
    @mother = neural-net object representing mother
    @returns = new child based on father/mother genetic information
    '''
 
    # make a copy of father 'genetic' weights & biases information
    nn = copy.deepcopy(father.net)

    # cross-over bias
    for _ in range(father.net.numOfBiases):
        # get some random points
        layer, point = getRandomPoint(father.net, 'bias')
        # replace genetic (bias) with mother's value
        if random.uniform(0, 1) < PAR.NN_crossoverRate:
            nn.biases[layer][point] = mother.net.biases[layer][point]
 
    # cross-over weight
    for _ in range(father.net.numOfWeights):
        # get some random points
        layer, point = getRandomPoint(father.net, 'weight')
        # replace genetic (weight) with mother's value
        if random.uniform(0, 1) < PAR.NN_crossoverRate:
            nn.weights[layer][point] = mother.net.weights[layer][point]
    
    # generate a new AICar as child
    child = AICar(PAR.NN_NetSize)
    # apply crossed net to child
    child.net = nn

    return child


def mutation(child):
    '''
    @returns = new child based on father/mother genetic information
    '''

#     print("child before mutation: " + str(child.net))

    # mutate bias
    for _ in range(child.net.numOfBiases):
        # get some random points
        layer, point = getRandomPoint(child.net, 'bias')
        # add some random value between -0.5 and 0.5
        if random.uniform(0,1) < PAR.NN_mutationRate:
            child.net.biases[layer][point] += random.uniform(-0.5, 0.5)

    # cross-over weight
    for _ in range(child.net.numOfWeights):
        # get some random points
        layer, point = getRandomPoint(child.net, 'weight')
        # add some random value between -0.5 and 0.5
        if random.uniform(0,1) < PAR.NN_mutationRate:
            child.net.weights[layer][point[0], point[1]] += random.uniform(-0.5, 0.5)
    
#     print("child after mutation: " + str(child.net))
    return child

def getRandomPoint(net, type):
 
    '''
    @type = either 'weight' or 'bias'
    @returns tuple (layer_index, point_index)
        note: if type is set to 'weight', point_index will return (row_index, col_index)
    '''
    
    layer_index, point_index = random.randint(0, net.numOfLayers-2), 0
    if type == 'weight':
        row = random.randint(0,net.weights[layer_index].shape[0]-1)
        col = random.randint(0,net.weights[layer_index].shape[1]-1)
        point_index = (row, col)
    elif type == 'bias':
        point_index = random.randint(0,net.biases[layer_index].size-1)
    return (layer_index, point_index)