'''sitePercolation.py: Verify that site percolation is a second-order phase transition. 
Noah Chavez 11/7/2023
Developed the union-find algorithm with the help of Andy Arrigoni
'''

#I am wondering how to use MC for this. I think i can get away with DFS and double for loop??

#Imports
import math
import random
import numpy as np
import matplotlib.pyplot as plt

#size is the number of sites in the cluster
size = {}
#bound keeps track of the top and bottom of the cluster
bounds = {}
#initalize the parent and size arrays
parent = {}

parentToCoords = {}

coords = []  

#initalize a square lattice, *heavily* inspiried by Binder
def generate_lattice(size: int, p: float) -> list[list[int]]:
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

#Run union-find on the lattice, keeping the bound in height, 
#so that we can figure out the proportion of clusters that run from top to bottom.
#Keeping in mind that every site is connected to its neighbors, including diagonals. (Every node has 8 neighbors)

#Find gets the root of the tree that i is in
def find(i):
    #If i is the root, return i
    if parent[i] == i:
        return i
    #Otherwise, run find on the parent of i
    return find(parent[i])

#Union joins the trees that i and j are in
def union(i,j):
    rooti = find(i)
    rootj = find(j)
    #If they are already in the same tree, do nothing
    if rooti == rootj:
        return
    #Otherwise, join the smaller tree to the larger tree, updating the bounds
    if size[rooti] < size[rootj]:
        parent[rooti] = rootj
        size[rootj] += size[rooti]
        bounds[rootj] = (min(bounds[rootj][0],bounds[rooti][0]),max(bounds[rootj][1],bounds[rooti][1]))

        parentToCoords[rootj].append(parentToCoords[rooti])
        del parentToCoords[rooti]
    else:
        parent[rootj] = rooti
        size[rooti] += size[rootj]
        bounds[rooti] = (min(bounds[rootj][0],bounds[rooti][0]),max(bounds[rootj][1],bounds[rooti][1]))

        parentToCoords[rooti].append(parentToCoords[rootj])
        del parentToCoords[rootj]


#Get all clusters
def getClusters(graph):

    visited = set()
    
    #Visit every node in the graph, running union-find on it. At the end, return the number of clusters, and the
    #Number of clusters that run from top to bottom.

    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == 1:
                #If it is not in the visited set, add it to the parent, size, and bounds arrays
                if (i,j) not in visited:

                    parent[(i,j)] = (i,j)
                    size[(i,j)] = 1
                    bounds[(i,j)] = (i,i)
                    parentToCoords[(i,j)] = [(i,j)]
                    #If it is in the visited set, run union-find on it
                    if (i,j-1) in visited:
                        union((i,j),(i,j-1))
                    if (i-1,j) in visited:
                        union((i,j),(i-1,j))
                    if (i-1,j-1) in visited:
                        union((i,j),(i-1,j-1))
                    if (i-1,j+1) in visited:
                        union((i,j),(i-1,j+1))
                    if (i+1,j-1) in visited:
                        union((i,j),(i+1,j-1))
                    if (i+1,j) in visited:
                        union((i,j),(i+1,j))
                    if (i+1,j+1) in visited:
                        union((i,j),(i+1,j+1))
                    if (i,j+1) in visited:
                        union((i,j),(i,j+1))
                    visited.add((i,j))


#Probability of a site being occupied
#p = 0.4

#Size of the lattice (Currently a square)
#latticeSize = 10
#testLattice = generate_lattice(latticeSize)

#print(testLattice)

def analyze_lattice(lattice, latticeSize):
    getClusters(lattice)

    parentset = set()

    for i in parent.keys():
        parentset.add(find(i))

    numberClusters = len(parentset)

    #print("Parents of clusters: ", parentset)

    #Comment in to see the clusters
    # for i in parentToCoords.keys():
    #    print("Cluster parent: ", i)
    #    print("Cluster: ", parentToCoords[i])
    #    print("Cluster bounds: ", bounds[i])

    #print("Number of clusters: ", numberClusters)

    numberTopToBottom = 0

    for bound in bounds.keys():
        if bounds[bound][0] == 0 and bounds[bound][1] == latticeSize-1:
            numberTopToBottom += 1
    #print("Number of clusters that run from top to bottom: ", numberTopToBottom)

    #print("Fraction of clusters that run from top to bottom: ", numberTopToBottom/numberClusters)
    #print("(p,Ps): (%s,%s)" % (p,numberTopToBottom/numberClusters))
    if(numberClusters == 0):
        return 0
    else:
        return(numberTopToBottom/numberClusters) #return Ps

def average_Ps(latticeSize, p, trials):
    Ps_sum = 0
    for run in range(trials):
        test_lattice = generate_lattice(latticeSize, p)
        run_Ps = analyze_lattice(test_lattice, latticeSize)
        Ps_sum += run_Ps
        # print()
        # print(run_Ps)
        # print(Ps_sum)
    #print(Ps_sum/trials)
    return(Ps_sum/trials)

#print(average_Ps(10,0.4,1000))


p_list = np.linspace(0.0001,1,100).tolist()
Ps = [average_Ps(10,p,5000) for p in p_list]
print(p_list)
print(Ps)
plt.xlabel("p")
plt.ylabel("Ps")
plt.title("Ps vs p")
plt.plot(p_list,Ps)
plt.show()

