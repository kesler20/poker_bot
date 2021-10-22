import numpy as np
from numpy.core.fromnumeric import argmax
import pandas as pd
from matplotlib import pyplot as plt

P = 10 # number of players
A = 3 # number of possible actions 
x0 = np.linspace(0,100)
y0 = np.linspace(0,1)
f = lambda x,y: (x/(x*y + y - 1))*((P - 1) + 1)
action_space = (P**A)*f(x0,y0)

def arg_max(action_space):
    max_value = 0
    for value in action_space:
        if value > max_value:
            max_value = value
        else:
            pass
    return max_value

x = arg_max(action_space)

plt.plot(action_space)
plt.show()
print(x) # answer: 712209.3023255827