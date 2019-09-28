'''
Name : Subhashis Dhar
Roll No: 2019H1030023P
'''

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QDialog
from PyQt5.QtGui import QIcon


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random

class Graph(QDialog):

    def __init__(self,title,data):
        super().__init__()
        self.left = 50
        self.top = 50
        self.title = title
        self.width = 600
        self.height = 400
        self.data = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        m = PlotCanvas(self.title,self.data,parent=self, width=6, height=4)
        m.move(0,0)

        self.exec()


class PlotCanvas(FigureCanvas):

    def __init__(self,title,data, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.data=data
        self.title = title

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()


    def plot(self):

        ax = self.figure.add_subplot(111)
        ax.plot(self.data, 'r-')
        ax.set_title(self.title)
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = [random.random() for i in range(25)]
    ex = Graph('PyQt5 matplotlib ',data)
    sys.exit(app.exec_())