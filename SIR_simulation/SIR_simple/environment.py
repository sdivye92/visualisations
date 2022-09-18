import numpy as np
from disease import Disease
from collections import Counter
import matplotlib.pyplot as plt
from itertools import filterfalse

col_mapping = {
    'Susceptible': 'xkcd:blue',
    'Infected': 'xkcd:red',
    'Recovered': 'xkcd:green'
}

class Environment:
    def __init__(self, Person, population_count, effective_distance=0.1):
        self.person_class = Person
        self.disease = None
        self.effective_distance = effective_distance
        self.population_count = population_count
        self.population = []
        self.cencus = {
            'Total': 0,
            'Susceptible': 0,
            'Infected': 0,
            'Recovered': 0
        }
        self.tick_wise_state_count = {
            'Susceptible': [],
            'Infected': [],
            'Recovered': []
        }
        self.__figure_created = False
    
    def __create_person(self, init_infection_ratio):
        state = 'Susceptible'
        pos = tuple(np.round(np.random.uniform(-10, 10, 2), 2))
        person = self.person_class(state, pos)
        self.person_class.count += 1
        return person
    
    def inject_disease(self, init_infection_ratio=0.2, disease=None):
        if isinstance(disease, Disease):
            self.disease = disease
            infected_people_count = int(np.ceil(self.population_count*init_infection_ratio))
            infected_people = np.random.randint(0, self.population_count, infected_people_count)
            for i in infected_people:
                self.population[i].state = 'Infected'
            self.update_cencus()
    
    def update_cencus(self):
        self.cencus.update(Counter(getattr(person, 'state') for person in self.population))
        for state in self.tick_wise_state_count.keys():
            self.tick_wise_state_count[state].append(self.cencus[state])
        
    def show_population(self):
        if not self.__figure_created:
            plt.figure(figsize=(10,5))
            self.__figure_created = True
        attr = np.array([[getattr(person, 'x'), getattr(person, 'y'), col_mapping[getattr(person, 'state')]] 
                    for person in self.population])
        
        plt.subplot(121)
        plt.scatter(attr[:,0].astype(float), attr[:,1].astype(float), c=attr[:,2])
        ax = plt.gca()
        #plt.xlim(-10,10)
        #plt.ylim(-10,10)
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        
        plt.subplot(122)
        for state in self.tick_wise_state_count.keys():
            plt.plot(self.tick_wise_state_count[state], c=col_mapping[state], label=state)
        plt.legend(loc='center right')
        plt.xlabel("days")
        plt.ylabel("Number of people")
        plt.pause(.0001)
    
    def simulate(self):
        print(self.cencus)
        for person in self.population:
            person.move()
            if self.disease is not None:
                person.update_state(self.population, self.effective_distance, self.disease)

        self.update_cencus()
        #self.show_population()
    
    def initiate(self, population_count=None, disease=None, init_infection_ratio=0.2):
        if population_count is not None:
            self.population_count = population_count
        
        self.population = [self.__create_person(init_infection_ratio) for _ in range(self.population_count)]
        self.inject_disease(init_infection_ratio, disease)
        self.cencus['Total'] = len(self.population)
        self.update_cencus()
