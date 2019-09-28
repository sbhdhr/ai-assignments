'''
Name : Subhashis Dhar
Roll No: 2019H1030023P
'''

import random
import sys
import time

from PyQt5.QtCore import QRect, Qt, QSize, QPoint
from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QFont, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QGroupBox, QVBoxLayout, QRadioButton, \
    QHBoxLayout, QComboBox, QGridLayout, QDialog, QMessageBox

from Graph import Graph
from State import State


class Window(QMainWindow):
    def __init__(self, width, height, initState):
        super().__init__()
        self.title = "MineSweeper"
        self.top = 200
        self.left = 200
        self.height = height
        self.width = width
        self.sq = 50
        self.currX = 0
        self.currY = 0
        self.steps = 0
        self.prevX = self.currX
        self.prevY = self.currY
        self.startTime = time.time()
        self.endTime = time.time()

        self.iconName = "minesweeper.png"
        self.drawType = 1
        self.initState = initState
        # self.visitedBoard = [[0 for i in range(self.initState.col)] for j in range(self.initState.row)]
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QIcon(self.iconName))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.UiComponents()

        self.show()

    def UiComponents(self):
        initTop = 45
        initLeft = 990

        btnWidth = 300
        btnHeight = 50
        marginTop = 30

        self.topLabel = QLabel("MineSweeper Simulation : ", self)
        self.topLabel.setFont(QFont("Sanserif", 12))
        self.topLabel.setGeometry(10, 5, initLeft, 20)

        self.btmLabel = QLabel("Status Bar : ", self)
        self.btmLabel.setFont(QFont("Sanserif", 10))
        self.btmLabel.setGeometry(10, initTop + (11 * 60) + marginTop, initLeft, 20)

        self.buttons = []

        for i in range(4):
            self.buttons.append(QPushButton("", self))
            self.buttons[i].setGeometry(QRect(initLeft, initTop + (i * (btnHeight + marginTop)), btnWidth, btnHeight))
            self.buttons[i].setIconSize(QSize(50, 50))

        self.buttons[0].setText("Start Game")
        self.buttons[0].setIcon(QIcon("start.png"))
        self.buttons[0].clicked.connect(self.startBtnClick)

        self.buttons[1].setText("Next Step")
        self.buttons[1].setIcon(QIcon("next.png"))
        self.buttons[1].clicked.connect(self.nextBtnClick)
        self.buttons[1].setDisabled(True)

        self.buttons[2].setText("Stop")
        self.buttons[2].setIcon(QIcon("stop.png"))
        self.buttons[2].clicked.connect(self.stopBtnClick)
        self.buttons[2].setDisabled(True)

        self.buttons[3].setText("Analysis Module")
        self.buttons[3].setIcon(QIcon("ana.png"))
        self.buttons[3].clicked.connect(self.openAnalysisWindows)

        self.groupBox = QGroupBox("Select Algorithm : ", self)
        vbox = QGridLayout(self)

        self.rad1 = QRadioButton("Hill Climbing")
        self.rad1.setChecked(True)
        vbox.addWidget(self.rad1, 0, 0)
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Stochastic")
        self.comboBox.addItem("Random Restart")
        self.comboBox.addItem("Local Beam Search")
        vbox.addWidget(self.comboBox, 0, 1)

        self.rad2 = QRadioButton("Simulated Annealing")
        vbox.addWidget(self.rad2, 1, 0)
        self.comboBox2 = QComboBox(self)
        self.comboBox2.addItem("With Threshold")
        self.comboBox2.addItem("Without Threshold")

        vbox.addWidget(self.comboBox2, 1, 1)

        self.groupBox.setLayout(vbox)
        self.groupBox.setFont(QFont("Sanserif", 10))
        self.groupBox.setGeometry(initLeft - 60, initTop + (6 * btnHeight) + marginTop, btnWidth + 100, 200)

        label2 = QLabel("Choose number of mines: ", self)
        label2.setFont(QFont("Sanserif", 10))
        label2.setGeometry(initLeft - 60, initTop + (6 * btnHeight) + 230 + marginTop, 250, 30)

        self.comboBox3 = QComboBox(self)
        self.comboBox3.setFont(QFont("Sanserif", 10))
        self.comboBox3.setGeometry(initLeft - 60 + 270, initTop + (6 * btnHeight) + 230 + marginTop, 80, 30)
        for i in range(30):
            self.comboBox3.addItem(str(i + 1), i + 1)
        self.comboBox3.setCurrentIndex(14)

        label3 = QLabel("Choose Heuristic: ", self)
        label3.setFont(QFont("Sanserif", 10))
        label3.setGeometry(initLeft - 60, initTop + (6 * btnHeight) + 300 + marginTop, 250, 30)

        self.comboBox4 = QComboBox(self)
        self.comboBox4.setFont(QFont("Sanserif", 10))
        self.comboBox4.setGeometry(initLeft - 60 + 270, initTop + (6 * btnHeight) + 300 + marginTop, 120, 30)
        self.comboBox4.addItem("Heuristic 1")
        self.comboBox4.addItem("Heuristic 2")

        self.drawType = 1
        self.update()

    def startBtnClick(self):
        self.drawType = 2
        self.initState.visited = [[0 for i in range(self.initState.col)] for j in range(self.initState.row)]
        self.initState.board = [[0 for i in range(self.initState.col)] for j in range(self.initState.row)]
        self.initState.htable1 = [[100 for i in range(self.initState.col)] for j in range(self.initState.row)]
        self.mines = int(str(self.comboBox3.currentText()))
        self.initState.left = self.initState.row * self.initState.col
        self.initState.mineGenerator(self.mines)
        self.buttons[0].setDisabled(True)
        self.buttons[2].setEnabled(True)
        self.buttons[1].setEnabled(True)
        self.steps=0
        self.steps+=1

        self.startTime = time.time()
        self.endTime = time.time()

        self.currX, self.currY = self.initState.firstClick()

        # get which algo we are using for sim and update top bar
        self.heur = self.comboBox4.currentIndex()
        # print(self.heur)
        if self.rad1.isChecked():
            self.algo = (1, self.comboBox.currentIndex())
            self.topLabel.setText("MineSweeper Simulation : Hill Climbing"
                                  + "  "
                                  + self.comboBox.currentText()
                                  + "  "
                                  + self.comboBox4.currentText())

        else:
            self.algo = (2, self.comboBox2.currentIndex())
            self.topLabel.setText(
                "MineSweeper Simulation : Simulated Annealing  "
                + self.comboBox2.currentText() + "  " + self.comboBox4.currentText())
        print(self.algo)

        self.btmLabel.setText("Status Bar: ")

        self.initState.nextState(self.currX, self.currY)
        # self.initState.printVisited()
        self.update()

        # time.sleep(0.5)

        self.checkMine()

    def createMessageBox(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("Minesweeper")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setModal(True)

        retval = msg.exec()
        return retval

    def checkMine(self):
        # s = "Choose grid no: {},{}".format(self.currX, self.currY)
        # self.btmLabel.setText(s)
        self.drawType = 2
        s = self.btmLabel.text()

        if self.initState.board[self.currX][self.currY] == 9:
            print("Game over")
            self.drawType = 3
            self.buttons[0].setEnabled(True)
            self.buttons[2].setDisabled(True)
            self.buttons[1].setDisabled(True)
            self.topLabel.setText("MineSweeper Simulation : Game Over !!")
            self.btmLabel.setText(s + " You hit a mine")
            self.createMessageBox("Game over")
            self.endTime = time.time()
            self.drawType = 1

        self.update()

    def stopBtnClick(self):

        self.initState.visited = [[0 for i in range(self.initState.col)] for j in range(self.initState.row)]
        self.buttons[2].setDisabled(True)
        self.buttons[0].setEnabled(True)
        self.buttons[1].setDisabled(True)
        self.topLabel.setText("MineSweeper Simulation : ")
        self.btmLabel.setText("Status Bar: ")
        self.drawType = 3
        self.update()
        self.createMessageBox("You stopped the game.")
        self.drawType = 1
        self.update()
        self.endTime = time.time()

        #

    def nextBtnClick(self):
        self.steps+=1
        self.prevX =self.currX
        self.prevY = self.currY

        if self.heur == 0:
            self.initState.heuristic1()
        else:
            self.initState.heuristic1()

        if self.algo[0] == 1 and self.algo[1] == 0:
            h, self.currX, self.currY = self.initState.stochasticHillClimbing()
        if self.algo[0] == 1 and self.algo[1] == 1:
            h, self.currX, self.currY = self.initState.randomRestartHillClimbing(self.prevX,self.prevY,self.currX, self.currY)
        if self.algo[0] == 1 and self.algo[1] == 2:
            h, self.currX, self.currY = self.initState.kbeamHillClimbing(self.currX, self.currY)
        if self.algo[0] == 2 and self.algo[1] == 0:
            h, self.currX, self.currY = self.initState.SimAnThreshold(self.currX, self.currY)
        if self.algo[0] == 2 and self.algo[1] == 1:
            h, self.currX, self.currY = self.initState.SimAn(self.currX, self.currY)

        s = "Choose grid no: {},{} Heuristic Value: {}".format(self.currX, self.currY, h)
        self.btmLabel.setText(s)
        self.drawType = 2
        self.initState.nextState(self.currX, self.currY)
        self.checkMine()

        print("left {} mines {}".format(self.initState.left, self.mines))
        if self.initState.left == self.mines:
            self.createMessageBox("You Won!!")
            self.endTime = time.time()

    def openAnalysisWindows(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Analysis Module")
        self.dialog.setGeometry(self.top + 50, self.left + 50, 600, 400)
        self.dialog.setModal(True)
        self.dialog.setWindowIcon(QIcon("ana.png"))
        self.InitAnalysisDialog()
        self.dialog.exec()

    def InitAnalysisDialog(self):
        initTop = 50
        initLeft = 50

        btnWidth = 200
        btnHeight = 90

        topLabel = QLabel("Analysis Module : ", self.dialog)
        topLabel.setFont(QFont("Sanserif", 14))
        topLabel.setGeometry(40, 40, 400, 50)

        self.hillClimbingBtn = QPushButton("Hill Climbing", self.dialog)
        self.hillClimbingBtn.setGeometry(QRect(initLeft, initTop + 100, btnWidth, btnHeight))
        self.hillClimbingBtn.clicked.connect(self.openHillClimbingAna)

        self.simAnBtn = QPushButton("Simulated Annealing", self.dialog)
        self.simAnBtn.setGeometry(QRect(initLeft + btnWidth + 40, initTop + 100, btnWidth, btnHeight))
        self.simAnBtn.clicked.connect(self.openSimAnAna)

    def openHillClimbingAna(self):
        self.dialog2 = QDialog()
        self.dialog2.setWindowTitle("Hill Climbing Analysis Module")
        self.dialog2.setGeometry(self.top + 50, self.left + 50, self.width, self.height)
        self.dialog2.setModal(True)
        self.dialog2.setWindowIcon(QIcon("ana.png"))
        self.InitAnalysisDialogHC()
        self.dialog2.exec()

    def InitAnalysisDialogHC(self):
        initTop = 45
        initLeft = 45

        btnWidth = 400
        btnHeight = 60
        marginTop = 80
        labelWidth = 600
        labelHeight = 50

        topLabel = QLabel("Analysis : ", self.dialog2)
        topLabel.setFont(QFont("Sanserif", 16))
        topLabel.setGeometry(10, 5, initLeft, 60)

        label1 = QLabel("R1) Memory : ", self.dialog2)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(10, 5 + marginTop, labelWidth, labelHeight)
        label1 = QLabel("", self.dialog2)
        # self.initState.row*self.initState.col*3  : for 3 2d arrays
        # 4: x,y pointers for current and prev
        # 4: sizeof int
        mem = self.initState.row*self.initState.col*3  \
              +4 \
              * 4
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(10 + labelWidth + 30, 5 + marginTop, labelWidth, labelHeight)
        label1.setText(str(mem))

        label2 = QLabel("R2) Time : ", self.dialog2)
        label2.setFont(QFont("Sanserif", 12))
        label2.setGeometry(10, 5 + marginTop + labelHeight, labelWidth, labelHeight)
        label2 = QLabel("", self.dialog2)
        label2.setText(str(self.endTime-self.startTime))
        label2.setFont(QFont("Sanserif", 12))
        label2.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight, labelWidth, labelHeight)

        label3 = QLabel("R3) Local Optimal Solution : ", self.dialog2)
        label3.setFont(QFont("Sanserif", 12))
        label3.setGeometry(10, 5 + marginTop + labelHeight * 2, labelWidth, labelHeight)
        label3 = QLabel("", self.dialog2)
        s = "Last Local Optimal Solution X: {} Y: {}".format(self.prevX, self.prevY)
        label3.setFont(QFont("Sanserif", 12))
        label3.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 2, labelWidth, labelHeight)
        label3.setText(s)

        label4 = QLabel("R4) Behaviour of Stochastic Hill Climbing with H1 : ", self.dialog2)
        label4.setFont(QFont("Sanserif", 12))
        label4.setGeometry(10, 5 + marginTop + labelHeight * 3, labelWidth, labelHeight)
        label4 = QLabel("Precomputed Value: For {}X{} grid - {} mines: 23 steps".format(self.initState.row,
                                                                                        self.initState.col,
                                                                                        15)
                        , self.dialog2)
        label4.setFont(QFont("Sanserif", 12))
        label4.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 3, labelWidth, labelHeight)

        label5 = QLabel("R5) Behaviour of Stochastic Hill Climbing with H2 : ", self.dialog2)
        label5.setFont(QFont("Sanserif", 12))
        label5.setGeometry(10, 5 + marginTop + labelHeight * 4, labelWidth, labelHeight)
        label5 = QLabel("Not implemented", self.dialog2)
        label5.setFont(QFont("Sanserif", 12))
        label5.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 4, labelWidth, labelHeight)

        label6 = QLabel("R6) Number of steps : ", self.dialog2)
        label6.setFont(QFont("Sanserif", 12))
        label6.setGeometry(10, 5 + marginTop + labelHeight * 5, labelWidth, labelHeight)
        label6 = QLabel(str(self.steps), self.dialog2)
        label6.setFont(QFont("Sanserif", 12))
        label6.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 5, labelWidth, labelHeight)

        label7 = QLabel("R7) Behaviour of Random Restart Hill Climbing with H1 : ", self.dialog2)
        label7.setFont(QFont("Sanserif", 12))
        label7.setGeometry(10, 5 + marginTop + labelHeight * 6, labelWidth, labelHeight)
        label7 = QLabel("Precomputed Value: For {}X{} grid - {} mines: 31 steps".format(self.initState.row,
                                                                                        self.initState.col,
                                                                                        15)
                        , self.dialog2)
        label7.setFont(QFont("Sanserif", 12))
        label7.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 6, labelWidth, labelHeight)

        label8 = QLabel("R8) Behaviour of Random Restart Hill Climbing with H2 : ", self.dialog2)
        label8.setFont(QFont("Sanserif", 12))
        label8.setGeometry(10, 5 + marginTop + labelHeight * 7, labelWidth, labelHeight)
        label8 = QLabel("Not Implemented ", self.dialog2)
        label8.setFont(QFont("Sanserif", 12))
        label8.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 7, labelWidth, labelHeight)

        label9 = QLabel("R9) Behaviour of local beam search with H1 : ", self.dialog2)
        label9.setFont(QFont("Sanserif", 12))
        label9.setGeometry(10, 5 + marginTop + labelHeight * 8, labelWidth, labelHeight)
        label9 = QLabel("Precomputed Value: For {}X{} grid - {} mines: 29 steps".format(self.initState.row,
                                                                                        self.initState.col,
                                                                                        15)
                        , self.dialog2)
        label9.setFont(QFont("Sanserif", 12))
        label9.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 8, labelWidth, labelHeight)

        label10 = QLabel("R10) Behaviour of local beam search with H2 :  ", self.dialog2)
        label10.setFont(QFont("Sanserif", 12))
        label10.setGeometry(10, 5 + marginTop + labelHeight * 9, labelWidth, labelHeight)
        label10 = QLabel("Not Implemented ", self.dialog2)
        label10.setFont(QFont("Sanserif", 12))
        label10.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 9, labelWidth, labelHeight)

        self.g2Btn = QPushButton("G2. Landscape", self.dialog2)
        self.g2Btn.setGeometry(QRect(initLeft, 650, btnWidth, btnHeight))
        self.g2Btn.clicked.connect(self.showG2)

        self.g4Btn = QPushButton("G4. Effect of size of war field", self.dialog2)
        self.g4Btn.setGeometry(QRect(initLeft+ btnWidth+marginTop,650 , btnWidth, btnHeight))
        self.g4Btn.clicked.connect(self.showG4)

    def showG2(self):

        data = []
        for i in range(self.initState.row):
            for j in range(self.initState.col):
                data.append(self.initState.htable1[i][j])

        ex = Graph('Landscape at current time ', data)


    def showG4(self):
        data = [5,12,18,29,37,48] #average number of steps taken if varying field size with constant mine size
        ex = Graph('Precomputed Value: Effect of field size with constant mine size', data)
        pass

    def openSimAnAna(self):
        self.dialog3 = QDialog()
        self.dialog3.setWindowTitle("Simulated Annealing Analysis Module")
        self.dialog3.setGeometry(self.top + 50, self.left + 50, self.width, self.height)
        self.dialog3.setModal(True)
        self.dialog3.setWindowIcon(QIcon("ana.png"))
        self.InitAnalysisDialogSA()
        self.dialog3.exec()

    def InitAnalysisDialogSA(self):
        initTop = 45
        initLeft = 800

        btnWidth = 400
        btnHeight = 60
        marginTop = 80
        labelWidth = 500
        labelHeight = 50

        topLabel = QLabel("Analysis : ", self.dialog3)
        topLabel.setFont(QFont("Sanserif", 16))
        topLabel.setGeometry(10, 5, initLeft, 60)

        label1 = QLabel("R11) Memory : ", self.dialog3)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(10, 5 + marginTop, labelWidth, labelHeight)
        # self.initState.row*self.initState.col*3  : for 3 2d arrays
        # 4: x,y pointers for current and prev
        # 4: sizeof int
        mem = self.initState.row * self.initState.col * 3 \
              + 4 \
              * 4
        label1 = QLabel(str(mem), self.dialog3)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(10 + labelWidth + 30, 5 + marginTop, labelWidth, labelHeight)

        label2 = QLabel("R12) Time : ", self.dialog3)
        label2.setFont(QFont("Sanserif", 12))
        label2.setGeometry(10, 5 + marginTop + labelHeight, labelWidth, labelHeight)
        label2 = QLabel(" ", self.dialog3)
        label2.setText(str(self.endTime - self.startTime))
        label2.setFont(QFont("Sanserif", 12))
        label2.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight, labelWidth, labelHeight)

        label3 = QLabel("R13) Local Optimal Solution : ", self.dialog3)
        label3.setFont(QFont("Sanserif", 12))
        label3.setGeometry(10, 5 + marginTop + labelHeight * 2, labelWidth, labelHeight)
        s = "Last Local Optimal Solution X: {} Y: {}".format(self.prevX, self.prevY)
        label3 = QLabel(s, self.dialog3)
        label3.setFont(QFont("Sanserif", 12))
        label3.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 2, labelWidth, labelHeight)

        label4 = QLabel("R14) Behaviour of Simulated Annealing with H1 : ", self.dialog3)
        label4.setFont(QFont("Sanserif", 12))
        label4.setGeometry(10, 5 + marginTop + labelHeight * 3, labelWidth, labelHeight)
        label4 = QLabel("R1. Memory : ", self.dialog3)
        label4.setFont(QFont("Sanserif", 12))
        label4.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 3, labelWidth, labelHeight)

        label5 = QLabel("R15) Behaviour of Simulated Annealing with H2 : ", self.dialog3)
        label5.setFont(QFont("Sanserif", 12))
        label5.setGeometry(10, 5 + marginTop + labelHeight * 4, labelWidth, labelHeight)
        label5 = QLabel("Not implemented", self.dialog3)
        label5.setFont(QFont("Sanserif", 12))
        label5.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 4, labelWidth, labelHeight)

        self.g6Btn = QPushButton("G6. Landscape", self.dialog3)
        self.g6Btn.setGeometry(QRect(initLeft, initTop + 100, btnWidth, btnHeight))
        self.g6Btn.clicked.connect(self.showG6)

        self.g7Btn = QPushButton("G7. Temperature range", self.dialog3)
        self.g7Btn.setGeometry(QRect(initLeft, initTop + 150 + btnHeight, btnWidth, btnHeight))
        self.g7Btn.clicked.connect(self.showG7)

    def showG6(self):
        print("show graph")
        pass

    def showG7(self):
        print("show graph")
        pass

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        if self.drawType == 1:
            self.DrawInitGrid(qp)
        if self.drawType == 2:
            self.DrawGridRevealingSquares(qp)
        if self.drawType == 3:
            self.DrawGridRevealingMines(qp)
        qp.end()
        # print(e)

    def DrawInitGrid(self, qp):
        initTop = 55
        initLeft = 40

        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.gray, Qt.SolidPattern))

        font = QFont()
        font.setPointSize(16)
        qp.setFont(font)

        #

        for i in range(self.initState.row):
            for j in range(self.initState.col):
                x = initLeft + (j * self.sq)
                y = initTop + (i * self.sq)

                # print("x: {} y: {}".format(x,y))

                qp.drawRect(x, y, self.sq, self.sq)

    def DrawGridRevealingMines(self, qp):
        initTop = 55
        initLeft = 40

        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))

        font = QFont()
        font.setPointSize(16)
        qp.setFont(font)

        for i in range(self.initState.row):
            for j in range(self.initState.col):
                x = initLeft + (j * self.sq)
                y = initTop + (i * self.sq)

                if self.initState.board[i][j] == 9:
                    qp.setBrush(QBrush(QColor(255, 0, 0, 127), Qt.SolidPattern))
                    qp.drawRect(x, y, self.sq, self.sq)

                elif self.initState.board[i][j] == 0:
                    qp.setBrush(QBrush(QColor(0, 255, 0, 127), Qt.SolidPattern))
                    qp.drawRect(x, y, self.sq, self.sq)
                else:
                    qp.setBrush(QBrush(QColor(0, 255, 0, 127), Qt.SolidPattern))
                    qp.drawRect(x, y, self.sq, self.sq)
                    qp.drawText(QPoint(x + 25, y + 35), str(self.initState.board[i][j]))

    def DrawGridRevealingSquares(self, qp):
        initTop = 55
        initLeft = 40

        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))

        font = QFont()
        font.setPointSize(16)
        qp.setFont(font)

        for i in range(self.initState.row):
            for j in range(self.initState.col):
                x = initLeft + (j * self.sq)
                y = initTop + (i * self.sq)

                if self.initState.visited[i][j] == 1 and self.initState.board[i][j] == 0:
                    qp.setBrush(QBrush(QColor(0, 255, 0, 127), Qt.SolidPattern))
                    qp.drawRect(x, y, self.sq, self.sq)
                elif self.initState.visited[i][j] == 1:
                    qp.setBrush(QBrush(QColor(0, 255, 0, 127), Qt.SolidPattern))
                    qp.drawRect(x, y, self.sq, self.sq)
                    qp.drawText(QPoint(x + 25, y + 35), str(self.initState.board[i][j]))
                else:
                    qp.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
                    qp.drawRect(x, y, self.sq, self.sq)

                if i == self.currX and j == self.currY:
                    qp.setBrush(QBrush(QColor(30, 63, 161), Qt.SolidPattern))
                    qp.drawRect(x, y, self.sq, self.sq)
                    if self.initState.board[i][j] != 0:
                        qp.drawText(QPoint(x + 25, y + 35), str(self.initState.board[i][j]))


def main():
    App = QApplication(sys.argv)
    initState = State(13, 17)

    window = Window(1366, 768, initState)
    sys.exit(App.exec())


if __name__ == '__main__':
    main()
