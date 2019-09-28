'''
Name : Subhashis Dhar
Roll No: 2019H1030023P
'''

from Environment import Environment
from Actions import Actions
from Node import Node

def hashState(env):
    hashVal = 0
    for i in range(env.n):
        for j in range(env.n):
            hashVal = (hashVal * 32 + env.board[i][j]) % 10000007
    hashVal = (hashVal * 32 + env.vacCleanerX) % 10000007
    hashVal = (hashVal * 32 + env.vacCleanerY) % 10000007
    return hashVal

hashed = []

def BFS(rootNode,goalState,path,queueSize):
    q = []
    
    q.append(rootNode)
    #print(rootNode.env.n)
    #print(rootNode.env.print())

    while(len(q) != 0):
        n = q.pop(0)
        h = hashState(n.env)
        #print(h)
        if h not in hashed:
            hashed.append(h)
            if(n.env.goalTest(goalState)):
                print("Goal state reached")
                p=n
                while(p.parent != None):
                    path.append((p.env.vacCleanerX,p.env.vacCleanerY,p.env.action))
                    p = p.parent
                    
                return n

            for x in Actions:
                state = Environment.nextState(n.env, x)
                nextNode = Node(state, n)
                q.append(nextNode)
        # else:
        #     print("Duplicate state. Ignored!")
        print("Queue Size: {}".format(len(q)))
        queueSize.append(len(q))
    return None

def getQueueSize():
    return len(hashed)