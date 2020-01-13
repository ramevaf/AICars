# AICars
A 2D game where the cars learn to drive through a course controlled by a neuronal network. For training of the network an evolutionary approach is used.

![alt text](https://raw.githubusercontent.com/ramevaf/AICars/master/AICars.jpg)

With each round a set of neuronal network driven cars is created which try to follow the track. If a car goes off the track it "dies". If all AICars are dead a new generation of AIcars is generated using the best cars of the former generation as parents. With each generation the cars are getting better and usually after 20-30 generations they are able to drive a whole lap.

The player is able to controll the blue car but so far there is no game mechanic added.

## Installation
Just clone the repository or download the *.zip file manually. The game itself is written in python and is using the pygame engine which is kinda slow unfortunately. Make sure you have the pygame and numpy packages installed. Usually it should work to run the following commands after you have installed python:
```
pip install numpy
pip install pygame
```
If everything is set up then simply execute the main.py file.
