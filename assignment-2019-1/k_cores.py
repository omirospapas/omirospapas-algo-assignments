#Created by Omiros Papadopoulos // assignment-2019-1
import sys

pairs = []    # Initialize list pair
nodes = set() # Create a set to keep the unique node numbers
adjlist = {}  # Create the adjacent list

# sys.argv[1]
# Open and Read file
with open(sys.argv[1], 'r') as graph:
    # Read each line of the file and recognize the pairs of nodes
    for line in graph:
        temp_line = line.strip('\n').split(' ')
        # temp_line is a list with 2 elements. E.g. ['a', 'b']
        for node in temp_line:
            # By adding node as int() the nodes set is sorted in ASC order
            nodes.add(int(node))
            # Initialize the adjacent list for each node
            adjlist[node] = []
        # pair = [temp_line[0], temp_line[1]]
        pairs.append([temp_line[0], temp_line[1]])

# Creating the adjacent list by checking all the pairs of nodes
# EG: {'0': ['1', '3', '7'],'1':['2', '3', '6']}
for p in pairs:
    adjlist[p[0]].append(p[1])
    adjlist[p[1]].append(p[0])

# ===================================================================================
#              CREATE THE HEAP ALGORITHM MANUALLY AS PER
# https://nbviewer.jupyter.org/urls/louridas.github.io/rwa/notebooks/chapter_03.ipynb

# We create a priority queue by creating an empty list:
def create_pq():
    return []

# Add element at the end of the list
def add_last(pq, c):
    pq.append(c)

# HELPER FUNCTIONS
# function that returns the position of the root - always 0
def root(pq):
    return 0
# function that assigns an element to the root of a non-empty queue
# If empty 0> nothing
def set_root(pq, c):
    if len(pq) != 0:
        pq[0] = c

# function that will return the data stored at a specified position in the queue
def get_data(pq, p):
    return pq[p]

# function that returns the children of a node in the queue.
def children(pq, p):
    if 2*p + 2 < len(pq):
        return [2*p + 1, 2*p + 2]
    else:
        return [2*p + 1]

# Conversely, the parent of a node at position c is at position ⌊(c−1)⌋/2
def parent(p):
    return (p - 1) // 2

# Swap elements in the queue
def exchange(pq, p1, p2):
    pq[p1], pq[p2] = pq[p2], pq[p1]

#Insert element in Priority queue
def insert_in_pq(pq, c):
    add_last(pq, c)
    i = len(pq) - 1
    while i != root(pq) and get_data(pq, i) < get_data(pq, parent(i)):
        p = parent(i)
        exchange(pq, i, p)
        i = p

# --- EXTRACTION ---
# To do that, we must use a helper function that will extract the last element of the queue
def extract_last_from_pq(pq):
    return pq.pop()

# function that will determine whether a given node has children
# Remember that a node p may have children at positions 2p+1 and 2p+2.
# Therefore we only need to check whether position 2p+1 is a valid position in the list.
def has_children(pq, p):
    return 2*p + 1 < len(pq)

# Element extraction function
def extract_min_from_pq(pq):
    c = pq[root(pq)]
    set_root(pq, extract_last_from_pq(pq))
    i = root(pq)
    while has_children(pq, i):
        # Use the data stored at each child as the comparison key
        # for finding the minimum.
        j = min(children(pq, i), key=lambda x: get_data(pq, x))
        if get_data(pq, i) < get_data(pq, j):
            return c
        exchange(pq, i, j)
        i = j
    return c

#                               end of HEAP algorithm
# ===================================================================================

min_queue = create_pq() # Initialize heap with minimums
degree = {}  # Initialize dictionary with the degree of each node
p_core = {}  # Initialize dictionary with potential core for each node
core = {}    # Initialize core number of each node after calculation

# Initiate values
for node in nodes:
    # Degree is equal to the No of neighbors
    degree[str(node)] = len(adjlist[str(node)])
    # Potential core number (p_core) = degree of node
    p_core[str(node)] = degree[str(node)]
    core[str(node)] = 0
    p_node = [int(p_core[str(node)]), str(node)] # [neighbors, node number]
    # Create a heap structure to store the node number and its degree number
    insert_in_pq(min_queue, p_node)


opn = {} # Initialise old potential node dictionary
npn = {} # Initialise new potential node dictionary

while len(min_queue) > 0:
    # Extract the min item from the heap (min_queue)
    t = extract_min_from_pq(min_queue)
    # print("T: ",t)
    core[t[1]] = t[0]
    if len(min_queue) != 0:
        for n in adjlist[t[1]]:
            # For each of the neighbor
            degree[n] -= 1
            # Store the neighbor's OLD potential core number
            opn[n] = [p_core[n], n]
            # Update the neighbor's core number. Max of (core number of current node t[0] OR updated degree of neighbor)
            p_core[n] = max(t[0], degree[n])
            # New potential node
            npn[n] = [p_core[n], n]
             # Update the heap
            for item in min_queue:
                if item[1] == str(n):
                    # Update opn with npd in the heap
                    item[0] = p_core[n]


# Check how it works
for i in range(len(core)):
    print(i, core[str(i)])
