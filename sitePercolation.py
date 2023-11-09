'''sitePercolation.py: Verify that site percolation is a second-order phase transition. 
Noah Chavez 11/7/2023
'''

#I am wondering how to use MC for this. I think i can get away with DFS and double for loop??

#Imports
import math
import random
import numpy as np
import matplotlib.pyplot as plt


p = 0.25
coords = []
#initalize a square lattice, *heavily* inspiried by Binder
def generate_lattice(size: int) -> list[list[int]]:
    lattice = np.zeros((size,size))
    for i in range(size):
        for j in range(size):
            #draw a random number
            num = random.uniform(0,1)
            if(p >= num):
                lattice[i][j] = 1
                coords.append((i,j))
            else:
                lattice[i][j] = 0
    return lattice

size = 10
testLattice = generate_lattice(size)
print(testLattice)



#plt.scatter([x[0] for x in coords], [y[1] for y in coords])
#plt.show()



#should i do bond? I guess im feeling lost on what to do. Not in terms of content difficulty but what i should be getting out of each thing?
#AN UNDIRECTED GRAPH IS A SYMMETRIC MATRIX
#TODO Then, DFS to find if any cluster spans the lattice. ISSUE: dfs in ternary tree? Then, average Ps for given p. Then, plot Ps vs p and determine pc. Should be smooth!

x = range(size)
y = range(size)