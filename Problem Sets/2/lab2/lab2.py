# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    from collections import deque
    father, path, expandedStates, frontier = dict(), [], set(), deque()
    frontier.append(start)
    curState = start

    while len(frontier) > 0:
        curState = frontier.popleft()
        if curState == goal:
            print "succ"
            break
        if curState in expandedStates: continue
        expandedStates.add(curState)
        succState = [x for x in graph.get_connected_nodes(curState) if x not in expandedStates]
        for s in succState:
            frontier.append(s)
            if not father.get(s):
                father[s] = curState

    while father.get(curState):
        path.append(curState)
        curState = father[curState]

    path.append(start)
    path.reverse()
    return path

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    from collections import deque
    father, path, expandedStates, frontier = dict(), [], set(), deque()
    frontier.append(start)
    curState = start

    while len(frontier) > 0:
        curState = frontier.pop()
        if curState == goal:
            print "succ"
            break
        if curState in expandedStates: continue
        expandedStates.add(curState)
        succState = [x for x in graph.get_connected_nodes(curState) if x not in expandedStates]
        for s in succState:
            frontier.append(s)
            if not father.get(s):
                father[s] = curState

    while father.get(curState):
        path.append(curState)
        curState = father[curState]

    path.append(start)
    path.reverse()
    return path



## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    from collections import deque
    father,path, frontier,pathExplored = dict(), [], deque(), set()
    frontier.append(start)

    import time
    while len(frontier) > 0:
        curState = frontier.pop()
        pathExplored.add(curState)
        if curState == goal:
            print "succ"
            break

        succState = [x for x in graph.get_connected_nodes(curState) if x not in pathExplored]
        sortedSucState = sorted(succState, key = lambda x: graph.get_heuristic(x, goal), reverse= True)
        for s in sortedSucState:
            frontier.append(s)
            father[s] = curState


    while father.get(goal):
        path.append(goal)
        goal = father[goal]

    path.append(start)
    path.reverse()
    return path

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    from collections import deque
    father, path, frontier, statesExpanded = dict(), [], deque(), set()
    frontier.append(start)

    while len(frontier) > 0 :
        curState = frontier.pop()
        if curState in statesExpanded : continue
        if curState == goal : break

        statesExpanded.add(curState)
        succStates = [x for x in graph.get_connected_nodes(curState) if x not in statesExpanded]
        for s in succStates:
            frontier.append(s)
            father[s] = curState

        sortedFrontier = sorted(frontier, key = lambda x: graph.get_heuristic(x, goal), reverse= True)
        if len(sortedFrontier) > beam_width:
            statesToRemove = sortedFrontier[:beam_width]
        else:
            statesToRemove = []

        newFrontier = deque()
        for state in frontier:
            if state not in statesToRemove:
                newFrontier.append(state)
        frontier = newFrontier

    while father.get(goal):
        path.append(goal)
        goal = father[goal]

    if len(path) > 0:
        path.append(start)

    path.reverse()
    return path

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    cost = 0
    if len(node_names) == 0:    return 0
    for i in range( len(node_names) -1):
        x = graph.get_edge(node_names[i], node_names[i+1])
        cost += x.length
    return cost

def branch_and_bound(graph, start, goal):

    a_path = [start]
    possiblePaths = []
    possiblePaths.append(a_path)
    while possiblePaths:
        curPath = possiblePaths[-1]
        headPath = curPath[-1]
        if headPath == goal: break
        del possiblePaths[-1]
        succ  = graph.get_connected_nodes(headPath)
        for s in succ:
            if s in curPath : continue
            newPath = curPath + [s]
            possiblePaths.append(newPath)
        possiblePaths = sorted(possiblePaths, key= lambda x: path_length(graph,x), reverse=True)

    return curPath


def a_star(graph, start, goal):
    from collections import deque
    father, path, frontier, statesExpanded = dict(), [], deque(), set()
    frontier.append(start)
    backwardCost = dict()
    totalCost = dict()
    backwardCost[start] = 0
    totalCost[start] = backwardCost[start] + graph.get_heuristic(start, goal)
    curState = ''
    while len(frontier) > 0:
        curState = frontier.pop()
        if curState in statesExpanded: continue
        if curState == goal: break

        statesExpanded.add(curState)
        succStates = [x for x in graph.get_connected_nodes(curState) if x not in statesExpanded]
        for s in succStates:
            if not backwardCost.get(s) or backwardCost[curState] + path_length(graph,[curState,s]) < backwardCost[s]:
                #frontier.remove(s)  scop didactic
                frontier.append(s)
                backwardCost[s] = backwardCost[curState] + path_length(graph,[curState,s])
                totalCost[s] = backwardCost[s] + graph.get_heuristic(s, goal)
                father[s] = curState

        sortedFrontier = sorted(frontier, key=lambda x: totalCost[x], reverse=True)
        frontier = sortedFrontier


    while father.get(curState):
        path.append(curState)
        curState = father[curState]

    if len(path) > 0:
        path.append(start)

    if start == goal:
        path.append(start)

    path.reverse()
    return path

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    for node in graph.nodes:
        heuristicCost =graph.get_heuristic(node,goal)
        actualCost = path_length(graph, branch_and_bound(graph, node, goal))
        if actualCost < heuristicCost:
            return False
    return True

def is_consistent(graph, goal):
    for node1 in graph.nodes:
        for node2 in graph.nodes:
            heuristicCost1 = graph.get_heuristic(node1, goal)
            heuristicCost2 = graph.get_heuristic(node2, goal)
            absHeuristicDiff = abs(heuristicCost1 - heuristicCost2)
            actualCost = path_length(graph, branch_and_bound(graph, node1, node2))
            if actualCost < absHeuristicDiff:
                return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '7'
WHAT_I_FOUND_INTERESTING = 'BEAM SEARCH'
WHAT_I_FOUND_BORING = 'ANYTHING ELSE'
