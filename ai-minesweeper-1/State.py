'''
Name : Subhashis Dhar
Roll No: 2019H1030023P
'''

import random


class State:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.board = [[0 for i in range(self.col)] for j in range(self.row)]
        self.visited = [[0 for i in range(self.col)] for j in range(self.row)]
        self.htable1 = [[100 for i in range(self.col)] for j in range(self.row)]
        self.left = row * col
        self.repeatCount=0


    def printBoard(self):
        for i in self.board:
            print(i)

    def printVisited(self):
        for i in self.visited:
            print(i)

    def mineGenerator(self, mines):
        c = 0
        while c != mines:
            x = random.randint(0, self.row - 1)
            y = random.randint(0, self.col - 1)
            # print("x: "+str(x)+"  y: "+str(y))
            # print(self.board[x][y])
            if self.board[x][y] != 9:
                self.board[x][y] = 9
                c += 1

        self.calculateBoardNumbers()

    def getValue(self, x, y):
        q = -1
        # print("GOT X: {} Y: {}".format(x, y))
        if x < 0 or y < 0:
            return q
        try:
            q = self.board[x][y]
            # print("Got q: {}".format(q))
        except:
            pass
        return q

    def getVisited(self, x, y):
        q = 0
        # print("GOT X: {} Y: {}".format(x, y))
        if x < 0 or y < 0:
            return q
        try:
            q = self.visited[x][y]
            # print("Got q: {}".format(q))
        except:
            pass
        return q

    def getHeuristic(self, x, y):
        q = 100
        # print("GOT X: {} Y: {}".format(x, y))
        if x < 0 or y < 0:
            return q
        try:
            q = self.htable1[x][y]
            # print("Got q: {}".format(q))
        except:
            pass
        return q

    def setValue(self, x, y, k):
        q = self.getValue(x, y)
        if (q != -1):
            self.visited[x][y] = k
            return True
        return False

    def calcNeighbourMines(self, i, j):
        c = 0
        if self.getValue(i, j - 1) == 9:
            c += 1
        if self.getValue(i, j + 1) == 9:
            c += 1
        if self.getValue(i - 1, j - 1) == 9:
            c += 1
        if self.getValue(i - 1, j) == 9:
            c += 1
        if self.getValue(i - 1, j + 1) == 9:
            c += 1
        if self.getValue(i + 1, j - 1) == 9:
            c += 1
        if self.getValue(i + 1, j) == 9:
            c += 1
        if self.getValue(i + 1, j + 1) == 9:
            c += 1

        return c

    def calculateBoardNumbers(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.board[i][j] == 0:
                    self.board[i][j] = self.calcNeighbourMines(i, j)

    def firstClick(self):
        x = random.randint(0, self.row - 1)
        y = random.randint(0, self.col - 1)
        return (x, y)

    def randomHeuristic(self):
        x = random.randint(0, self.row - 1)
        y = random.randint(0, self.col - 1)
        while (self.visited[x][y] != 0):
            x = random.randint(0, self.row - 1)
            y = random.randint(0, self.col - 1)
        return (x, y)

    def heuristic1(self):
        total = self.col*self.row
        c=0
        for i in range(self.row):
            for j in range(self.col):
                c = 0
                if self.visited[i][j]==1 and self.board[i][j]!=0:
                    c += self.getVisited(i, j - 1)
                    c += self.getVisited(i, j + 1)
                    c += self.getVisited(i+1, j )
                    c += self.getVisited(i+1, j - 1)
                    c += self.getVisited(i+1, j + 1)
                    c += self.getVisited(i-1, j )
                    c += self.getVisited(i-1, j - 1)
                    c += self.getVisited(i-1, j + 1)
                    if c>0:
                        self.htable1[i][j] = c-self.board[i][j]/c


    def kbeamHillClimbing(self,i,j):

        l = []
        for i in range(self.row):
            for j in range(self.col):
                if self.visited[i][j] == 1 and self.board[i][j] != 0:
                    l.append((self.getHeuristic(i, j), i, j))


        m = random.randint(0, len(l) - 1)

        h, x, y = l[m]
        x += 1
        y += 1

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.row - 1:
            x = self.row - 1
        if y > self.col - 1:
            y = self.col - 1

        return (h, x, y)

    def stochasticHillClimbing(self):

        l = []
        m=100
        for i in range(self.row):
            for j in range(self.col):
                if self.visited[i][j]==1 and self.board[i][j]!=0:
                    m = min(m,self.getHeuristic(i, j))

        for i in range(self.row):
            for j in range(self.col):
                if self.visited[i][j] == 1 and self.board[i][j] != 0:
                    if self.getHeuristic(i, j)==m:
                        l.append((m,i,j))


        #print("len list "+str(len(l)))

        #print(l)
        m = random.randint(0, len(l)-1)

        h,x, y = l[m]
        x+=1
        y+=1

        if x<0:
            x=0
        if y<0:
            y=0
        if x>self.row-1:
            x = self.row-1
        if y>self.col-1:
            y = self.col-1

        return (h, x, y)

    def randomRestartHillClimbing(self, px,py,i,j):
        h,x,y = self.stochasticHillClimbing()
        if x==px and y==py:
            self.repeatCount+=1

        if self.repeatCount==3:
            print("Restarting Randomly")
            x,y = self.randomHeuristic()
            self.repeatCount=0

        return (h,x,y)


    def SimAnThreshold(self, i, j):
        print("Not yet implemented")
        pass

    def SimAn(self, i, j):
        print("Not yet implemented")
        pass

    def nextState(self, x, y):
        #
        l = []
        c = self.row * self.col // 3
        l.append((x, y))

        while c > 4 and len(l) > 0:

            i, j = l.pop(0)
            try:
                if self.visited[i][j] != 1 and self.getValue(i, j) != 9:
                    if self.setValue(i, j, 1):
                        c -= 1
                        self.left -= 1

                    if self.getValue(i, j) == 0:
                        l.append((i, j - 1))
                        l.append((i, j + 1))
                        l.append((i - 1, j - 1))
                        l.append((i - 1, j))
                        l.append((i - 1, j + 1))
                        l.append((i + 1, j - 1))
                        l.append((i + 1, j))
                        l.append((i + 1, j + 1))

            except:
                pass
        # print(c)


if __name__ == '__main__':
    s = State(9, 12)
    s.mineGenerator(10)
    s.printBoard()

    x, y = s.firstClick()
    print("X: {} Y:{}".format(x, y))
    s.nextState(x, y)
    s.printVisited()
