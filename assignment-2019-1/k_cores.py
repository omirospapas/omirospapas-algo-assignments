#Created by Omiros Papadopoulos // assignment-2019-1
import sys
from heapq import heappush, heappop

pairs = []
nodes = set() # Create a set to keep the unique node numbers
adjlist = {}  # Craete the adjacent list

# Open and Read file
with open(sys.argv[1], 'r') as graph:
	# Read each line of the file and recognize the pairs of nodes
    for line in graph:
        temp_line = line.strip('\n').split(' ')
        # temp_line is a list with 2 elements. E.g. ['a', 'b']
        for node in temp_line:
            nodes.add(node)
            # Initialize the adjacent list for each node
            adjlist[node] = []
        # Create pairs as tuples. E.g. ('a','b')
        pair = (temp_line[1], temp_line[0])
        pairs.append(pair)

# Creating the adjacent list by checking all the pairs of nodes
for p in pairs:
    adjlist[p[0]].append(p[1])
    adjlist[p[1]].append(p[0])

mh = []  	 # Initialize heap with minimums
degree = {}  # Initialize dictionary with the degree of each node
p_core = {}  # Initialize dictionary with potential core for each node
core = {}    # Initialize core number of each node after calculation

# Initiate values
for node in nodes:
    # Degree is equal to the No of neighbors
    degree[node] = len(adjlist[node])
    # Potential core number (p_core) = degree of node
    p_core[node] = degree[node]
    core[node] = 0
    p_node = [p_core[node],node] # [neighbors, node number]
    # Create a heap structure to store the node number and its degree number
    heappush(mh,p_node)


opn = {} # Initialise old potential node dictionary
npn = {} # Initialise new potential node dictionary

while len(mh) > 0:
    # Extract the min item from the heap (mh)
    t = heappop(mh)
    core[t[1]] = t[0]
    if len(mh) != 0:
        for n in adjlist[t[1]]:
            # For each of the neighbor
            degree[n] -=1
            # Store the neighbors OLD potential core number
            opn[n] = [p_core[n],n]
            # Upate the neighbor's core number. Max of (core number of current node t[0] -OR- updated degree of neighbor)
            p_core[n] = max(t[0], degree[n])
            # New potential node
            npn[n] = [p_core[n], n]
            # Update the heap
            for item in mh:
                if item[1] == str(n):
                    # Update opn with npd in the heap
                    item[0] = p_core[n]

# Print the core dictionary in ascending order
for i in range(len(core)):
    print(i, core[str(i)])
