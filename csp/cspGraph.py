'''
Name : Subhashis Dhar
Roll No: 2019H1030023P
'''

import sys
import time

from Node import Node
import itertools

Group = [
    [],
    [3, 5, 8, 9, 12, 18, 19],
    [8, 9, 12, 19, 2],
    [3, 5, 4, 16, 8, 9, 19],
    [8, 9, 12, 15],
    [15, 16, 17, 18, 19, 20],
    [3, 5, 7, 11, 14, 20],
    [3, 5, 12, 2, 18, 19, 20, 1],
    [3, 5, 8, 9, 10, 18, 19, 20],
    [3, 13, 8, 9, 7, 19, 20],
    [1, 8, 9, 13, 20],
    [18, 19, 20],
    [3, 11, 8, 18, 19, 20],
    [3, 8, 10, 12, 4, 20],
    [3, 5, 11, 9, 10, 17, 19, 20],
    [2, 8, 12, 18, 19, 20]
]

Nodes = []
Nodes.append(Node(1, list((2, 5, 7))))
Nodes.append(Node(2, list(((1, 4, 6, 2)))))
Nodes.append(Node(3, list(((2, 5, 6, 1)))))
Nodes.append(Node(4, list(((2, 4, 6, 8)))))
Nodes.append(Node(5, list(((2, 6, 5)))))
Nodes.append(Node(6, list(((1, 5, 3)))))
Nodes.append(Node(7, list(((2, 4, 6, 1, 8)))))
Nodes.append(Node(8, list(((1, 3, 4)))))
Nodes.append(Node(9, list(((4, 1, 5, 8, 6)))))
Nodes.append(Node(10, list(((8,)))))
Nodes.append(Node(11, list(((2, 3)))))
Nodes.append(Node(12, list(((1, 2, 3, 4, 7)))))
Nodes.append(Node(13, list(((7, 1, 8)))))
Nodes.append(Node(14, list(((5, 3, 6, 1)))))
Nodes.append(Node(15, list(((2, 5)))))
Nodes.append(Node(16, list(((2, 5, 1, 4)))))
Nodes.append(Node(17, list(((1, 4, 5, 6)))))
Nodes.append(Node(18, list(((5, 4)))))
Nodes.append(Node(19, list(((1, 3, 6, 8)))))
Nodes.append(Node(20, list(((6,)))))

CSPGraph = None
nodesGen = 0

def checkOverlappingDomain(l1, l2):
    res = False
    for x in l1:
        if x in l2:
            res = True
            break

    return res


def constructCSPGraph(m, Group):
    CSPGraph = [[0 for i in range(m + 1)] for j in range(m + 1)]
    grpLen = len(Group)

    for i in range(1, grpLen):
        subList = Group[i]
        subList = list(itertools.combinations(subList, 2))

        for x, y in subList:
            # print("Checking: {} :: {} - {} :: {}".format(x, Nodes[x - 1].domain, y, Nodes[y - 1].domain))
            if checkOverlappingDomain(Nodes[x - 1].domain, Nodes[y - 1].domain):
                CSPGraph[x][y] = 1

    return CSPGraph


def printCSPGraph(CSPGraph):
    m = len(CSPGraph)

    for i in range(0, m):
        if i == 0:
            print('{:3}'.format(" "), end='  ')
        else:
            print('{:3}'.format(i), end='  ')
    print()

    for i in range(0, m):
        if i == 0:
            print('{:3}'.format(" "), end='  ')
        else:
            print('---', end='  ')

    print()

    for i in range(1, m):
        for j in range(0, m):
            if j == 0:
                print('{:3}'.format(str(i) + '|'), end='  ')
            elif i == j:
                print('{:3}'.format('---'), end='  ')
            elif i < j:
                print('{:3}'.format(CSPGraph[i][j]), end='  ')
            else:
                print('{:3}'.format('   '), end='  ')
        print()


def isSafe(v, grp, assignment, t):
    global CSPGraph
    size = len(grp)
    node = grp[v]
    for i in range(1, size + 1):
        if (CSPGraph[node][i] == 1 or CSPGraph[i][node] == 1) and (t in assignment):
            return False
    return True


def DFSBacktrackingUtil(assignment, grp, v):
    global nodesGen
    if v == len(grp):
        return True

    node = grp[v]
    # print("Node : {} :: {}".format(node, Nodes[node-1].domain))

    for c in Nodes[node - 1].domain:
        nodesGen+=1
        if isSafe(v, grp, assignment, c):
            # print("Assigning {} -> {}".format(grp[v], c))
            assignment[v] = c
            if DFSBacktrackingUtil(assignment, grp, v + 1):
                return True
            # print("Clearing Assignment {} ".format(v))
            assignment[v] = 0


def DFSBacktracking(i):
    size = len(Group[i])
    assignment = [0] * size
    if DFSBacktrackingUtil(assignment, Group[i], 0) is None:
        print("Partial Assignment : Group#{:2} :  =============================".format(i))
        print(" No Solution")
        print("================================================================")
        return False

    # Print the solution
    print("Partial Assignment : Group#{:2} :  =============================".format(i))
    for c in assignment:
        print(c, end="\t")
    print()
    print("================================================================")
    return True


def main():
    global CSPGraph
    m = 20

    CSPGraph = constructCSPGraph(m, Group)

    print("Constraint Graph Represented as Adjacency matrix: ")
    print("==================================================\n")
    printCSPGraph(CSPGraph)

    startTime = time.time()


    for i in range(1, len(Group)):
        time.sleep(1)
        DFSBacktracking(i)

    endTime = time.time()

    # print(Nodes)
    print("\nAnalysis: ")
    print("==========\n")
    print("R1. Number of nodes generated: {}".format(nodesGen))
    print("R2. Memory allocated to one Node: {}".format(sys.getsizeof(Nodes)/len(Nodes)))
    #here
    s=0
    for i in range(1,16):
        s+=len(Group[i])
    print("R3. Avg Length of explicit recursion depth: {}".format(s/15))
    print("R4. Time taken to compute the nodes: {}".format(endTime-startTime-15))


if __name__ == "__main__":
    main()
