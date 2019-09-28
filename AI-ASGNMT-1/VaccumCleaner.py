'''
Name : Subhashis Dhar
Roll No: 2019H1030023P
'''

import turtle
import time

class VaccumCleaner:

    def __init__(self, canvas, n,length,dotSize):
        self.vc = turtle.RawTurtle(canvas,shape="turtle")
        self.n = n
        self.length = length
        self.dotSize = dotSize
        self.l = [x-(n/2)+0.5 for x in range(self.n)]
        self.l2 = [(n/2)-0.5-x for x in range(self.n)]

    def forward(self, steps=100):
        self.vc.forward(steps)

    def backward(self, steps=100):
        self.vc.backward(steps)

    def left(self, angle=90):
        self.vc.left(angle)

    def right(self, angle=90):
        self.vc.right(angle)

    def moveToXY(self, x, y, drawPath=False):
        if(not drawPath):
            self.vc.penup()

        self.vc.goto(self.l[y]*self.length, self.l2[x]*self.length)
        self.vc.setheading(90)
        self.vc.pendown()

    def paintDot(self, color):
        self.vc.dot(self.dotSize, color)

    def goHome(self,drawPath=False):
        if(not drawPath):
            self.vc.penup()
        self.vc.goto(-self.length*self.n / 2+(self.length/2), self.length*self.n/2-(self.length/2))
        self.vc.setheading(90)
        self.vc.pendown()

    def drawGrid(self):
        self.vc.ht()
        self.vc.speed(0)
        self.vc._delay(0)
        self.vc.penup()
        self.vc.goto(-self.n * self.length/2, -self.n * self.length/2)
        self.vc.pendown()
        sign = 1
        for _ in range(2):
            for _ in range(self.n):
                self.vc.forward(self.length * self.n)
                self.vc.left(sign * 90)
                self.vc.forward(self.length)
                self.vc.left(sign * 90)
                sign = 0 - sign

            self.vc.forward(self.length * self.n)
            [self.vc.right,  self.vc.left][self.n % 2](90)
            sign = 0 - sign
        self.vc.st()

    def showState(self, env):
        self.vc.ht()
        self.vc.speed(0)
        self.vc._delay(0)
        self.vc._tracer(0, 0)
        self.reset()
        for r in range(env.n):
            for c in range(env.n):
                self.moveToXY(r, c)
                if env.board[r][c] == 0:
                    self.paintDot("white")
                else:
                    self.paintDot("red")
        
        self.moveToXY(env.vacCleanerX, env.vacCleanerY)
        self.vc.st()
        self.vc._update()
        self.vc._tracer(1,0)
        

    def reset(self):
        self.vc.turtlesize(1, 1, None)
        self.goHome()


    def goHomeAftCleaning(self,x,y,delay=0.5):
        
        while(x>0):
            x = x-1
            #print("X: {}".format(x))
            self.moveToXY(x,y,True)
            time.sleep(delay)
        while(y>0):
            y = y-1
            #print("Y: {}".format(y))
            self.moveToXY(x,y,True)
            time.sleep(delay)

    