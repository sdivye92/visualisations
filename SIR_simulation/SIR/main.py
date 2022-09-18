from environment import Environment
from person import Person
from disease import Disease
import matplotlib.pyplot as plt

env = Environment(Person, 20, 1)
env.initiate(400)
disease = Disease(0.1, 0.2)

ticks = 50
for tick in range(ticks):
    if tick == 3:
        env.inject_disease(0.01, disease)
    else:
        env.simulate()
        env.show_population()
    if tick < ticks-1:
        plt.clf()
    else:
        plt.show()