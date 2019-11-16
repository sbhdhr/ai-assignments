import copy
import math
import random
import sys
import time

from PyQt5.QtCore import QRect, Qt, QSize, QPoint
from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QFont, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QGroupBox, QVBoxLayout, QRadioButton, \
    QHBoxLayout, QComboBox, QGridLayout, QDialog, QMessageBox, QStyle


class Window(QMainWindow):
    def __init__(self, width, height):
        super().__init__()
        self.title = "Connect 3"
        self.top = 200
        self.left = 200
        self.height = height
        self.width = width
        self.sq = 150
        self.iconName = "logo.png"

        self.board = [[0 for i in range(4)] for j in range(4)]
        self.HUMAN = 1
        self.AI = 2
        self.turn = self.AI
        self.row = 0
        self.col = 0
        self.algoToUse = 0
        self.recursionDepth = 6

        # Analysis variables
        self.startTime = 0
        self.endTime = 0
        self.humanTime = 0
        self.aiTime = 0
        self.humanTime2 = 0
        self.aiTime2 = 0
        self.nodes = 0
        self.nodesAB = 0
        self.algo1TimesPlayed = 0
        self.algo2TimesPlayed = 0
        self.algo3TimesPlayed = 0
        self.tempBoardSize = 0
        self.algo1Win=0
        self.algo2Win = 0

        self.InitWindow()

    # ============================= UI ============================================
    def InitWindow(self):
        self.setWindowIcon(QIcon(self.iconName))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.UiComponents()

        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.DrawGrid(qp)
        qp.end()
        # print(e)

    def DrawGrid(self, qp):
        initTop = 50
        initLeft = 60

        font = QFont()
        font.setPointSize(16)
        qp.setFont(font)

        qp.setPen(QPen(Qt.red, 14, Qt.SolidLine))
        qp.drawLine(initLeft - 30, initTop, 700, initTop)

        initTop = 85
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.gray, Qt.SolidPattern))

        for i in range(4):
            for j in range(4):
                x = initLeft + (j * self.sq)
                y = initTop + (i * self.sq)

                qp.drawRect(x, y, self.sq, self.sq)
                if self.board[i][j] == self.HUMAN:
                    qp.setBrush(QBrush(QColor(255, 0, 0, 127), Qt.SolidPattern))
                    qp.drawEllipse(x + 5, y + 5, self.sq - 10, self.sq - 10)
                    qp.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
                if self.board[i][j] == self.AI:
                    qp.setBrush(QBrush(QColor(0, 0, 255, 127), Qt.SolidPattern))
                    qp.drawEllipse(x + 5, y + 5, self.sq - 10, self.sq - 10)
                    qp.setBrush(QBrush(Qt.gray, Qt.SolidPattern))

        initLeft = 750
        qp.setPen(QPen(Qt.black, 8, Qt.SolidLine))
        qp.drawLine(initLeft, 30, initLeft, self.height - 30)

        qp.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        qp.setBrush(QBrush(QColor(255, 0, 0, 127), Qt.SolidPattern))
        qp.drawEllipse(initLeft + 50, 600, 50, 50)
        qp.drawText(QPoint(initLeft + 150, 630), "Human")
        qp.setBrush(QBrush(QColor(0, 0, 255, 127), Qt.SolidPattern))
        qp.drawEllipse(initLeft + 50, 680, 50, 50)
        qp.drawText(QPoint(initLeft + 150, 710), "AI")

    def UiComponents(self):
        initTop = 65
        initLeft = 820

        btnWidth = 300
        btnHeight = 50
        marginTop = 30

        self.startBtn = QPushButton("Start", self)
        self.startBtn.setGeometry(QRect(initLeft, initTop + (0 * (btnHeight + marginTop)), btnWidth, btnHeight))
        self.startBtn.setIcon(QIcon("start.png"))
        self.startBtn.clicked.connect(self.startBtnClick)
        self.startBtn.setIconSize(QSize(50, 50))

        self.analysisBtn = QPushButton("Analysis Module", self)
        self.analysisBtn.setGeometry(QRect(initLeft, initTop + (1 * (btnHeight + marginTop)), btnWidth, btnHeight))
        self.analysisBtn.setIcon(QIcon("ana.png"))
        self.analysisBtn.clicked.connect(self.openAnalysisWindows)
        self.analysisBtn.setIconSize(QSize(50, 50))

        self.colBtns = []

        btnWidth = 77

        for i in range(1, 5):
            self.colBtns.append(QPushButton("Col-" + str(i), self))
            self.colBtns[i - 1].setGeometry(QRect(initLeft - 40 + ((btnWidth + 30) * (i - 1)),
                                                  initTop + (2.5 * (btnHeight + marginTop)), btnWidth, btnHeight))
            self.colBtns[i - 1].setDisabled(True)

        self.colBtns[0].clicked.connect(self.colBtn1)
        self.colBtns[1].clicked.connect(self.colBtn2)
        self.colBtns[2].clicked.connect(self.colBtn3)
        self.colBtns[3].clicked.connect(self.colBtn4)

        self.comboBox = QComboBox(self)
        self.comboBox.setFont(QFont("Sanserif", 10))
        self.comboBox.setGeometry(QRect(initLeft + 40, initTop + (4 * (btnHeight + marginTop)), 250, 50))
        self.comboBox.addItem("Algorithm : Minimax")
        self.comboBox.addItem("Algorithm : Alpha Beta Prune")
        self.comboBox.addItem("Algorithm : Random Selection")

    def startBtnClick(self):
        self.analysisBtn.setDisabled(True)
        self.startBtn.setDisabled(True)

        # self.board[0][3] = self.HUMAN
        # self.board[0][1] = self.AI

        self.algo = self.comboBox.currentIndex()
        print("Using algo : {}".format(self.algo))

        self.playAI()

    def colBtn1(self):
        self.col = 0
        self.playHuman()
        pass

    def colBtn2(self):
        self.col = 1
        self.playHuman()
        pass

    def colBtn3(self):
        self.col = 2
        self.playHuman()
        pass

    def colBtn4(self):
        self.col = 3
        self.playHuman()
        pass

    def createMessageBox(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setWindowTitle("Connect3")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setModal(True)

        retval = msg.exec()
        return retval

    def reset(self):
        self.board = [[0 for i in range(4)] for j in range(4)]
        self.turn = self.AI
        if self.algo == 0:
            self.algo1TimesPlayed += 1
        elif self.algo == 1:
            self.algo2TimesPlayed += 1
        elif self.algo == 2:
            self.algo3TimesPlayed += 1

        self.startBtn.setEnabled(True)
        self.analysisBtn.setEnabled(True)
        for x in self.colBtns:
            x.setDisabled(True)


    # ============================= UI ============================================

    # ============================= Algorithm ============================================
    def playHuman(self):

        r = self.openRow(self.board, self.col)
        if (r == 4):
            self.createMessageBox("Invalid Move")
        else:
            self.placeToken(self.board, r, self.col, self.HUMAN)
            self.turn = self.AI
            self.update()

            term = self.terminalState(self.board, self.HUMAN)
            if term:
                self.createMessageBox("Human Won")
                self.reset()
            else:
                # time.sleep(2)
                self.endTime = time.time()

                if self.algo == 0:
                    self.humanTime = (self.endTime - self.startTime)
                    #print("human1 time: {}".format(self.humanTime))
                elif self.algo == 1:
                    self.humanTime2 = (self.endTime - self.startTime)
                    #print("human2 time: {}".format(self.humanTime2))
                self.playAI()




    def playAI(self):
        self.startTime = time.time()
        #print(self.startTime)
        #
        if self.algo == 0:
            c, score = self.minimax(self.board, self.recursionDepth, True)
            print(score)
        elif self.algo == 1:
            c, score = self.alphaBetaPrune(self.board, self.recursionDepth, -math.inf, math.inf, True)
            print(score)
        elif self.algo == 2:
            c = random.randint(0, 3)

        r = self.openRow(self.board, c)
        if r == 4:
            c = random.randint(0, 3)
            r = self.openRow(self.board, c)

        self.placeToken(self.board, r, c, self.AI)

        self.update()
        self.turn = self.HUMAN
        # time.sleep(0.5)
        term = self.terminalState(self.board, self.AI)
        if term:
            self.createMessageBox("AI Won")
            if self.algo == 0:
                self.algo1Win+=1
            elif self.algo == 1:
                self.algo2Win+=1
            self.reset()
        else:
            for x in self.colBtns:
                x.setEnabled(True)

        self.endTime = time.time()
        if self.algo == 0:
            self.aiTime += (self.endTime - self.startTime)
        elif self.algo == 1:
            self.aiTime2 += (self.endTime - self.startTime)

        self.startTime = time.time()

    def validlocation(self, board, col):
        return board[3][col] == 0

    def getValidLocations(self, board):
        validLocations = []
        for c in range(4):
            if self.validlocation(board, c):
                validLocations.append(c)
        return validLocations

    def placeToken(self, board, r, c, piece):
        if r < 4:
            board[r][c] = piece
            self.row = r
            self.col = c

    def openRow(self, board, c):
        # print("C: {}".format(c))
        for r in range(0, 4):
            if board[r][c] == 0:
                return r
        else:
            return 4

    def getValue(self, board, x, y):
        q = 0
        if x < 0 or y < 0:
            return q
        try:
            q = board[x][y]
        except:
            pass
        return q

    def terminalState(self, board, piece):
        # left horizontal
        lh = True
        for i in range(3):
            if self.getValue(board, self.row, self.col - i) != piece:
                lh = False
                break
        # right horizontal
        rh = True
        for i in range(3):
            if self.getValue(board, self.row, self.col + i) != piece:
                rh = False
                break

        # horizontal middle
        hm = False
        if self.getValue(board, self.row, self.col - 1) == piece \
                and self.getValue(board, self.row, self.col) == piece \
                and self.getValue(board, self.row, self.col + 1) == piece:
            hm = True

        # vertical
        v = True
        for i in range(3):
            if self.getValue(board, self.row - i, self.col) != piece:
                v = False
                break

        # left upper diagonal
        lud = True
        for i in range(3):
            if self.getValue(board, self.row - i, self.col - i) != piece:
                lud = False
                break

        # right upper diagonal
        rud = True
        for i in range(3):
            if self.getValue(board, self.row - i, self.col + i) != piece:
                rud = False
                break

        # left lower diagonal
        lld = True
        for i in range(3):
            if self.getValue(board, self.row + i, self.col - i) != piece:
                lld = False
                break

        # right lower diagonal
        rld = True
        for i in range(3):
            if self.getValue(board, self.row + i, self.col + i) != piece:
                rld = False
                break

        # left diag middle
        ldm = False
        if self.getValue(board, self.row - 1, self.col - 1) == piece \
                and self.getValue(board, self.row, self.col) == piece \
                and self.getValue(board, self.row + 1, self.col + 1) == piece:
            ldm = True

        # right diag middle
        rdm = False
        # l = []
        # l.append(self.getValue(board, self.row - 1, self.col + 1))
        # l.append(self.getValue(board, self.row, self.col))
        # l.append(self.getValue(board, self.row + 1, self.col - 1))
        # print("L in rdm: {}".format(str(l)))

        if self.getValue(board, self.row - 1, self.col + 1) == piece \
                and self.getValue(board, self.row, self.col) == piece \
                and self.getValue(board, self.row + 1, self.col - 1) == piece:
            rdm = True

        # board is full
        full = True
        for i in board:
            if 0 in i:
                # print(i)
                full = False
                break

        return lh or rh or v or lud or rud or lld or rld or full or hm or ldm or rdm

    def windowUtilityValue(self, window, piece):
        score = 0

        oppPiece = self.HUMAN
        if piece == self.HUMAN:
            oppPiece = self.AI

        if window.count(piece) == 3:
            score += 100
        elif window.count(piece) == 2 and window.count(0) == 1:
            score += 5

        if window.count(oppPiece) == 2 and window.count(0) == 1:
            score -= 40

        return score

    def utilityValue(self, board, piece):
        # Horizontal
        score = 0
        for x in board:
            for c in range(0, 2):
                window = x[c:c + 3]
                score += self.windowUtilityValue(window, piece)

        # print("Board: ")
        # for x in board:
        #     print(x)
        #
        # print("")

        # Vertical
        for c in range(4):
            # print("Col = {}".format(c))
            cols = []
            for r in range(4):
                cols.append(board[r][c])
            # print(cols)

            for r in range(2):
                window = cols[r:r + 3]
                score += self.windowUtilityValue(window, piece)

        # Diagonal 1
        for r in range(2):
            for c in range(2):
                window = [board[r + i][c + i] for i in range(3)]
                score += self.windowUtilityValue(window, piece)

        # Diagonal 2
        for r in range(2):
            for c in range(2):
                window = [board[r + 2 - i][c + i] for i in range(3)]
                score += self.windowUtilityValue(window, piece)
        return score

    def minimax(self, board, depth, maxPlayer):
        termAI = self.terminalState(board, self.AI)
        termHuman = self.terminalState(board, self.HUMAN)

        if depth == 0 or termAI or termHuman or len(self.getValidLocations(board)) == 0:
            if termAI or termHuman or len(self.getValidLocations(board)) == 0:
                if termAI:
                    return None, 10000
                elif termHuman:
                    return None, -10000
                else:
                    return None, 0
            else:
                return None, self.utilityValue(board, self.AI)

        if maxPlayer:
            val = -math.inf
            validLoc = self.getValidLocations(board)
            column = random.choice(validLoc)
            for col in validLoc:
                self.nodes += 1
                r = self.openRow(board, col)
                tempBoard = copy.deepcopy(board)
                self.tempBoardSize = sys.getsizeof(tempBoard)
                self.placeToken(tempBoard, r, col, self.AI)
                _, newScore = self.minimax(tempBoard, depth - 1, False)
                if newScore > val:
                    val = newScore
                    column = col
            return column, val

        else:
            val = math.inf
            validLoc = self.getValidLocations(board)
            column = random.choice(validLoc)
            for col in self.getValidLocations(board):
                self.nodes += 1
                r = self.openRow(board, col)
                tempBoard = copy.deepcopy(board)
                self.placeToken(tempBoard, r, col, self.HUMAN)
                _, newScore = self.minimax(tempBoard, depth - 1, True)
                if newScore < val:
                    val = newScore
                    column = col
            return column, val

    def alphaBetaPrune(self, board, depth, alpha, beta, maxPlayer):
        termAI = self.terminalState(board, self.AI)
        termHuman = self.terminalState(board, self.HUMAN)

        if depth == 0 or termAI or termHuman or len(self.getValidLocations(board)) == 0:
            if termAI or termHuman or len(self.getValidLocations(board)) == 0:
                if termAI:
                    return None, 10000
                elif termHuman:
                    return None, -10000
                else:
                    return None, 0
            else:
                return None, self.utilityValue(board, self.AI)

        if maxPlayer:
            val = -math.inf
            validLoc = self.getValidLocations(board)
            column = random.choice(validLoc)
            for col in validLoc:
                self.nodesAB += 1
                r = self.openRow(board, col)
                tempBoard = copy.deepcopy(board)
                self.placeToken(tempBoard, r, col, self.AI)
                _, newScore = self.minimax(tempBoard, depth - 1, False)
                if newScore > val:
                    val = newScore
                    column = col
                alpha = max(val, alpha)
                if alpha >= beta:
                    break
            return column, val

        else:
            val = math.inf
            validLoc = self.getValidLocations(board)
            column = random.choice(validLoc)
            for col in self.getValidLocations(board):
                self.nodesAB += 1
                r = self.openRow(board, col)
                tempBoard = copy.deepcopy(board)
                self.placeToken(tempBoard, r, col, self.HUMAN)
                _, newScore = self.minimax(tempBoard, depth - 1, True)
                if newScore < val:
                    val = newScore
                    column = col
                beta = min(val, beta)
                if alpha >= beta:
                    break
            return column, val

    # ============================= Algorithm ============================================

    # ============================= Analysis Part ============================================
    def openAnalysisWindows(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Analysis Module")
        self.dialog.setGeometry(self.top + 50, self.left + 50, 1366, 768)
        self.dialog.setModal(True)
        self.dialog.setWindowIcon(QIcon("ana.png"))
        self.InitAnalysisDialog()
        self.dialog.exec()

    def InitAnalysisDialog(self):
        initTop = 45
        initLeft = 45

        btnWidth = 400
        btnHeight = 60
        marginTop = 130
        labelWidth = 300
        labelHeight = 50

        col = 30
        col2 = 450
        col3 = 900

        topLabel = QLabel("Analysis : Minimax", self.dialog)
        topLabel.setFont(QFont("Sanserif", 20))
        topLabel.setGeometry(col, 10, 350, 40)
        topLabel.setStyleSheet("text-decoration: underline;")

        topLabel = QLabel("Analysis : Alpha Beta", self.dialog)
        topLabel.setFont(QFont("Sanserif", 20))
        topLabel.setGeometry(col2, 10, 350, 40)
        topLabel.setStyleSheet("text-decoration: underline;")

        topLabel = QLabel("Comparative", self.dialog)
        topLabel.setFont(QFont("Sanserif", 20))
        topLabel.setGeometry(col3, 10, 350, 40)
        topLabel.setStyleSheet("text-decoration: underline;")

        label1 = QLabel("For {} games : ".format(self.algo1TimesPlayed), self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col, 60, labelWidth, labelHeight)
        label1.setStyleSheet("text-decoration: underline;")

        label1 = QLabel("For {} games : ".format(self.algo2TimesPlayed), self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col2, 60, labelWidth, labelHeight)
        label1.setStyleSheet("text-decoration: underline;")



        label1 = QLabel("R1) Nodes Generated : " + str(self.nodes), self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col, (0 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("R2) Memory per node: " + str(self.tempBoardSize) + " bytes", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col, (1 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("R3) Max Recursion Depth: Limited to " + str(self.recursionDepth), self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col, (2 * labelHeight) + marginTop, labelWidth, labelHeight)
        label1.setWordWrap(True)

        label1 = QLabel("R4) Time to play game: ", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col, (4 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("R4.a) Human Time: " + str(round(self.humanTime,7)) + " ms", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col + 30, (5 * labelHeight) + marginTop, labelWidth, labelHeight)
        label1 = QLabel("R4.b) AI Time: " + str(round(self.aiTime,7)) + " ms", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col + 30, (6 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("Total Time: " + str(round((self.aiTime + self.humanTime),7))+ " ms", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col + 40, (7 * labelHeight) + marginTop, labelWidth, labelHeight)

        if self.aiTime != 0:
            nodePerMSec = self.nodes / self.aiTime
        else:
            nodePerMSec = 0
        label1 = QLabel("R5) Number of Nodes created per micro sec = (R1/time taken by AI): "
                        + str(round(nodePerMSec,7)),
                        self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col, (8 * labelHeight) + marginTop, labelWidth, labelHeight * 2)
        label1.setWordWrap(True)

        label1 = QLabel("R6) Nodes generated: " + str(self.nodesAB), self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col2, (0 * labelHeight) + marginTop, labelWidth, labelHeight)

        if self.nodesAB != 0:
            ratio = (self.nodes - self.nodesAB) / self.nodesAB
        else:
            ratio = 0
        label1 = QLabel("R7) Save Ratio: " + str(int(ratio)), self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col2, (1 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("R8) Time to play game: ", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col2, (2 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("R8.a) Human Time: " + str(round(self.humanTime2,7)) + " ms", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col2 + 30, (3 * labelHeight) + marginTop, labelWidth, labelHeight)
        label1 = QLabel("R8.b) AI Time: " + str(round(self.aiTime2,7)) + " ms", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col2 + 30, (4 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("Total Time: " + str(round((self.aiTime2 + self.humanTime2),7)) + " ms", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col2 + 40, (5 * labelHeight) + marginTop, labelWidth, labelHeight)

        labelWidth = 400
        marginTop = 70
        label1 = QLabel("R9) Memory: ", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3, (0 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("R9.a) Minimax: " + str(self.nodes * self.tempBoardSize) + " bytes", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3 + 30, (1 * labelHeight) + marginTop, labelWidth, labelHeight)
        label1 = QLabel("R9.b) Alpha Beta: " + str(self.nodesAB * self.tempBoardSize) + " bytes", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3 + 30, (2 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("R10) Average time taken in 10 Games: ", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3, (3 * labelHeight) + marginTop, labelWidth, labelHeight)

        if self.algo1TimesPlayed !=0:
            avg = (self.aiTime+self.humanTime)/self.algo1TimesPlayed *10
            avg = round(avg,7)
        else:
            avg = 0
        label1 = QLabel("R10.a) Minimax: " + str(avg)+" ms", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3 + 30, (4 * labelHeight) + marginTop, labelWidth, labelHeight)
        if self.algo2TimesPlayed != 0:
            avg = (self.aiTime2 + self.humanTime2) / self.algo2TimesPlayed*10
            avg = round(avg, 7)
        else:
            avg = 0
        label1 = QLabel("R10.b) Alpha Beta: " + str(avg)+" ms", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3 + 30, (5 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("R11) Number of times M wins in 10 Games: ", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3, (6 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("R11.a) Minimax: " + str("Precomputed: 10"), self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3 + 30, (7 * labelHeight) + marginTop, labelWidth, labelHeight)
        label1 = QLabel("Current: {}/{}".format(self.algo1Win,self.algo1TimesPlayed), self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3 + 60, (8 * labelHeight) + marginTop, labelWidth, labelHeight)
        label1 = QLabel("R11.b) Alpha Beta: " + str("Precomputed: 10"), self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3 + 30, (9 * labelHeight) + marginTop, labelWidth, labelHeight)
        label1 = QLabel("Current: {}/{}".format(self.algo2Win, self.algo2TimesPlayed), self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3 + 60, (10 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("R12) Number of times M wins in 10 Games Repeated 20 times: ", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3, (11 * labelHeight) + marginTop, labelWidth, labelHeight)
        label1.setWordWrap(True)

        label1 = QLabel("R11.a) Minimax: " + str("Precomputed: 10"), self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3 + 30, (12 * labelHeight) + marginTop, labelWidth, labelHeight)

        label1 = QLabel("R11.b) Alpha Beta: " + str("Precomputed: 10"), self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(col3 + 30, (13 * labelHeight) + marginTop, labelWidth, labelHeight)
    # ============================= Analysis Part ============================================


def main():
    App = QApplication(sys.argv)

    window = Window(1200, 768)
    sys.exit(App.exec())


if __name__ == '__main__':
    main()

'''

    
        
        
    def InitAnalysisDialogHC(self):
        initTop = 45
        initLeft = 45

        btnWidth = 400
        btnHeight = 60
        marginTop = 80
        labelWidth = 600
        labelHeight = 50

        topLabel = QLabel("Analysis : ", self.dialog)
        topLabel.setFont(QFont("Sanserif", 16))
        topLabel.setGeometry(10, 5, initLeft, 60)

        label1 = QLabel("R1) Memory : ", self.dialog)
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(10, 5 + marginTop, labelWidth, labelHeight)
        label1 = QLabel("", self.dialog)
        # self.initState.row*self.initState.col*3  : for 3 2d arrays
        # 4: x,y pointers for current and prev
        # 4: sizeof int
        mem = self.initState.row * self.initState.col * 3 \
              + 4 \
              * 4
        label1.setFont(QFont("Sanserif", 12))
        label1.setGeometry(10 + labelWidth + 30, 5 + marginTop, labelWidth, labelHeight)
        label1.setText(str(mem))

        label2 = QLabel("R2) Time : ", self.dialog)
        label2.setFont(QFont("Sanserif", 12))
        label2.setGeometry(10, 5 + marginTop + labelHeight, labelWidth, labelHeight)
        label2 = QLabel("", self.dialog)
        label2.setText(str(self.endTime - self.startTime))
        label2.setFont(QFont("Sanserif", 12))
        label2.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight, labelWidth, labelHeight)

        label3 = QLabel("R3) Local Optimal Solution : ", self.dialog)
        label3.setFont(QFont("Sanserif", 12))
        label3.setGeometry(10, 5 + marginTop + labelHeight * 2, labelWidth, labelHeight)
        label3 = QLabel("", self.dialog)
        s = "Last Local Optimal Solution X: {} Y: {}".format(self.prevX, self.prevY)
        label3.setFont(QFont("Sanserif", 12))
        label3.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 2, labelWidth, labelHeight)
        label3.setText(s)

        label4 = QLabel("R4) Behaviour of Stochastic Hill Climbing with H1 : ", self.dialog)
        label4.setFont(QFont("Sanserif", 12))
        label4.setGeometry(10, 5 + marginTop + labelHeight * 3, labelWidth, labelHeight)
        label4 = QLabel("Precomputed Value: For {}X{} grid - {} mines: 23 steps".format(self.initState.row,
                                                                                        self.initState.col,
                                                                                        15)
                        , self.dialog)
        label4.setFont(QFont("Sanserif", 12))
        label4.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 3, labelWidth, labelHeight)

        label5 = QLabel("R5) Behaviour of Stochastic Hill Climbing with H2 : ", self.dialog)
        label5.setFont(QFont("Sanserif", 12))
        label5.setGeometry(10, 5 + marginTop + labelHeight * 4, labelWidth, labelHeight)
        label5 = QLabel("Not implemented", self.dialog)
        label5.setFont(QFont("Sanserif", 12))
        label5.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 4, labelWidth, labelHeight)

        label6 = QLabel("R6) Number of steps : ", self.dialog)
        label6.setFont(QFont("Sanserif", 12))
        label6.setGeometry(10, 5 + marginTop + labelHeight * 5, labelWidth, labelHeight)
        label6 = QLabel(str(self.steps), self.dialog)
        label6.setFont(QFont("Sanserif", 12))
        label6.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 5, labelWidth, labelHeight)

        label7 = QLabel("R7) Behaviour of Random Restart Hill Climbing with H1 : ", self.dialog)
        label7.setFont(QFont("Sanserif", 12))
        label7.setGeometry(10, 5 + marginTop + labelHeight * 6, labelWidth, labelHeight)
        label7 = QLabel("Precomputed Value: For {}X{} grid - {} mines: 31 steps".format(self.initState.row,
                                                                                        self.initState.col,
                                                                                        15)
                        , self.dialog)
        label7.setFont(QFont("Sanserif", 12))
        label7.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 6, labelWidth, labelHeight)

        label8 = QLabel("R8) Behaviour of Random Restart Hill Climbing with H2 : ", self.dialog)
        label8.setFont(QFont("Sanserif", 12))
        label8.setGeometry(10, 5 + marginTop + labelHeight * 7, labelWidth, labelHeight)
        label8 = QLabel("Not Implemented ", self.dialog)
        label8.setFont(QFont("Sanserif", 12))
        label8.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 7, labelWidth, labelHeight)

        label9 = QLabel("R9) Behaviour of local beam search with H1 : ", self.dialog)
        label9.setFont(QFont("Sanserif", 12))
        label9.setGeometry(10, 5 + marginTop + labelHeight * 8, labelWidth, labelHeight)
        label9 = QLabel("Precomputed Value: For {}X{} grid - {} mines: 29 steps".format(self.initState.row,
                                                                                        self.initState.col,
                                                                                        15)
                        , self.dialog)
        label9.setFont(QFont("Sanserif", 12))
        label9.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 8, labelWidth, labelHeight)

        label10 = QLabel("R10) Behaviour of local beam search with H2 :  ", self.dialog)
        label10.setFont(QFont("Sanserif", 12))
        label10.setGeometry(10, 5 + marginTop + labelHeight * 9, labelWidth, labelHeight)
        label10 = QLabel("Not Implemented ", self.dialog)
        label10.setFont(QFont("Sanserif", 12))
        label10.setGeometry(10 + labelWidth + 30, 5 + marginTop + labelHeight * 9, labelWidth, labelHeight)

        self.g2Btn = QPushButton("G2. Landscape", self.dialog)
        self.g2Btn.setGeometry(QRect(initLeft, 650, btnWidth, btnHeight))
        self.g2Btn.clicked.connect(self.showG2)

        self.g4Btn = QPushButton("G4. Effect of size of war field", self.dialog)
        self.g4Btn.setGeometry(QRect(initLeft + btnWidth + marginTop, 650, btnWidth, btnHeight))
        self.g4Btn.clicked.connect(self.showG4)

    def showG2(self):

        data = []
        for i in range(self.initState.row):
            for j in range(self.initState.col):
                data.append(self.initState.htable1[i][j])

        ex = Graph('Landscape at current time ', data)

    def showG4(self):
        data = [5, 12, 18, 29, 37, 48]  # average number of steps taken if varying field size with constant mine size
        ex = Graph('Precomputed Value: Effect of field size with constant mine size', data)
        pass

'''
