import numpy as np

class Pendulum():
    """
    Class for holds all of pendulum variables.
    """
    def __init__(self,length, mass, initial_angle):
        self.l = length
        self.m = mass
        self.theta = initial_angle
        self.v = 0
        self.x = 0
        self.y = 0
        self.p = 0
        self.a = 0
        self.energy = 0
        self.ke = 0
        self.pe = 0

        
