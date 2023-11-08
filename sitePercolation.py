'''sitePercolation.py: Verify that site percolation is a second-order phase transition. 
Noah Chavez 11/7/2023
'''

#I am wondering how to use MC for this. I think i can get away with DFS and double for loop??

#Imports
import math
import random
import numpy as np
import matplotlib.pyplot as plt


p = 0.1

#initalize a square lattice, *heavily* inspiried by Binder
def generate_lattice(size: int) -> list[list[int]]:
    lattice = [[0]*size]*size
    for i in range(size):
        for j in range(size):
            #draw a random number
            if(p >= random.uniform(0,1)): #its the same everytime?
                lattice[i][j] = 1
            else:
                lattice[i][j] = 0
    return lattice

size = 10
testLattice = generate_lattice(size)
print(testLattice)

#TODO print out 2d grid in pyplot. Then, DFS to find if any cluster spans the lattice. Then, average Ps for given p. Then, plot Ps vs p and determine pc. Should be smooth!

x = range(size)
y = range(size)