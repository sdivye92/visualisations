from pendulum import Pendulum
from plot import Plot
from utils import *

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

class Simulation:

    def __init__(self,l1,l2,m1,m2,theta1,theta2,time,dt):
        """
        Initialize the Simulation class
        
        l1 = Length of the first pendulum.
        l2 = Length of the second pendulum.
        m1 = Mass of the first pendulum.
        m2 = Mass of the second pendulum.
        theta1 = Angle of the first pendulum with respect to the vertical.
        theta2 = Angle of the second pendulum with respect to the first pendulum.
        time = Total length of the simulation.
        dt = Time between plot updates.
        """
        self.dt = dt
        self.tend = time
        self.b1 = Pendulum(l1,m1,theta1)
        self.b2 = Pendulum(l2,m2,theta2)
        self.b1, self.b2 = update_positions(self.b1, self.b2)
        self.b1, self.b2 = update_energies(self.b1, self.b2)
        self.b1.a, self.b2.a = get_acceleration(self.b1, self.b2)

    def __acc_callback(self, y0, t, b1, b2):
        """ This is a wrapper to the kick function"""
        
        b1.theta, b2.theta, b1.v, b2.v = y0
        a1,a2 = get_acceleration(b1, b2)
        res = np.array([b1.v, b2.v, a1, a2])
        return res

    def __pyode(self):
        """
        This is a wrapper to the odeint integrator.
        """
        y0 = np.array([self.b1.theta, self.b2.theta, self.b1.v, self.b2.v])
        
        res=odeint(self.__acc_callback, y0, [0, self.dt], args=(self.b1, self.b2))
        self.b1.theta, self.b2.theta, self.b1.v, self.b2.v = res[1]
        if self.b1.theta > np.pi:
            while self.b1.theta > np.pi:
                self.b1.theta -= 2*np.pi
        if self.b1.theta < -np.pi:
            while self.b1.theta < -np.pi:
                self.b1.theta += 2*np.pi
        if self.b2.theta > np.pi:
            while self.b2.theta > np.pi:
                self.b2.theta -= 2*np.pi
        if self.b2.theta < -np.pi:
            while self.b2.theta < -np.pi:
                self.b2.theta += 2*np.pi

    def run(self):
        """ Entry point for the simulation.
        
        """
        ploting = Plot(self.b1, self.b2)
        
        t = np.arange(int(self.tend/self.dt)+1)*self.dt
        
        
        i = 1
        for i,ti in enumerate(t[1:],start=1):
            self.__pyode()
            self.b1, self.b2 = update_positions(self.b1, self.b2)
            self.b1, self.b2 = update_energies(self.b1, self.b2)
            ploting.update_plots(self.b1, self.b2, ti)
        plt.show()
