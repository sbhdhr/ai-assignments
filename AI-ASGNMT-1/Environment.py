'''
Name : Subhashis Dhar
Roll No: 2019H1030023P
'''

import random
import copy
from Actions import Actions

class Environment():
    def __init__(self, action, n=10, vacCleanerX=0, vacCleanerY=0):
        self.n = n
        self.board = [[0 for x in range(n)] for j in range(n)]
        self.vacCleanerX = vacCleanerX
        self.vacCleanerY = vacCleanerY
        self.action = action

    def print(self):
        for x in self.board:
            print(x)

    def generateDirt(self, p=30):
        dirtyTiles = int(p/100*self.n*self.n)
        # print(dirtyTiles)
        c = 0
        while(c != dirtyTiles):
            x = random.randint(0, self.n-1)
            y = random.randint(0, self.n-1)
            #print("x: "+str(x)+"  y: "+str(y))
            # print(self.board[x][y])
            if(self.board[x][y] != 1):
                self.board[x][y] = 1
                c += 1

    def goalTest(self, env):
        # if(self.n != env.n or self.vacCleanerX!=env.vacCleanerX or self.vacCleanerY!=env.vacCleanerY):
        #     # print("here")
        #     return False

        for i in range(self.n):
            for j in range(self.n):
                if(self.board[i][j] != env.board[i][j]):
                    #print("self : "+str(self.board[i][j])+"  param: "+str(env.board[i][j]))
                    return False
        return True

    def cleanXY(self, x, y):
        self.board[x][y] = 0

    @staticmethod
    def nextState(currentState, action):
        t = copy.deepcopy(currentState)
        # print("Cleaner pos {} {} in method".format(state.cleaner.posx,state.cleaner.posy))

        if(action == Actions.MU):
            if(t.vacCleanerX-1 >= 0):
                t.vacCleanerX -= 1

        elif(action == Actions.MD):
            if(t.vacCleanerX+1 < t.n):
                t.vacCleanerX += 1

        elif(action == Actions.ML):
            if(t.vacCleanerY-1 >= 0):
                t.vacCleanerY -= 1

        elif(action == Actions.MR):
            if(t.vacCleanerY+1 < t.n):
                t.vacCleanerY += 1

        elif(action == Actions.S):
            t.cleanXY(t.vacCleanerX, t.vacCleanerY)

        elif(action == Actions.N):
            pass

        t.action = action
        return t

    def printState(self):
        for i in self.board:
            print(i)


    def compare(self,env):
        #print(x)
        if(self.vacCleanerX != env.vacCleanerX or self.vacCleanerY != env.vacCleanerY):
            return False
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] != env.board[i][j]:
                    #print("not same")
                    return False
        return True

if __name__ == "__main__":
    pass
