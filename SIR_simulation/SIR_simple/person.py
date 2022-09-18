import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from itertools import filterfalse

class Person:
    count = 0
    def __init__(self, state, position, pid=None):
        self.state = state
        self.x = position[0]
        self.y = position[1]
        self.infected_for_day = 0
        self.id = pid if pid is not None else Person.count
    
    def __clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)
    
    def move(self):
        self.x += np.round(np.random.normal(scale=0.5), 2)
        self.y += np.round(np.random.normal(scale=0.5), 2)
        self.x = self.__clamp(self.x, -10, 10)
        self.y = self.__clamp(self.y, -10, 10)
        
    def __person_dist(self, p1, p2):
        return np.sqrt(((p1.x - p2.x)**2) + ((p1.y - p2.y)**2))
    
    def __change_to_infected(self, population, effective_distance, infectiousness):
        nbr = list(filterfalse(lambda person: self.__person_dist(self, person) > effective_distance, population))
        nbr.remove(self)
        if len(nbr) > 0:
            infected_nbr = list(filterfalse(lambda person: person.state == 'Infected', nbr))
            infected_nbr_count = len(infected_nbr)
            if infected_nbr_count > 0:
                if np.random.rand() <= infectiousness:
                    self.state = 'Infected'
    
    def __change_to_recovered(self, recovery_rate):
        if np.random.rand() <= recovery_rate:
            self.state = 'Recovered'
    
    def update_state(self, population, effective_distance, disease):
        infectiousness = disease.infectiousness
        recovery_rate = disease.recovery_rate
        if self.state == 'Susceptible':
            self.__change_to_infected(population, effective_distance, infectiousness)
        if self.state == 'Infected':
            if self.infected_for_day > 2:
                self.__change_to_recovered(recovery_rate)
            self.infected_for_day += 1
                        
    def __repr__(self):
        return "person"+str(self.id)
    
    @classmethod
    def reset(cls):
        cls.count = 0
