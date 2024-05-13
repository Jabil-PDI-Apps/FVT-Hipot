import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(250, 250)

        self.container = QFrame()
        self.layout = QVBoxLayout()
        self.container.setStyleSheet(
            "background-color:#fff"
        )
        self.progress = ToggleButton()

        self.layout.addWidget(self.progress)

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        self.timer = QTimer()
        self.show()
        self.timer.timeout.connect(self.callback)
        self.timer.start(5)

    def callback(self):
        self.timer.stop()
        if self.progress.value + 1 > 360:
            self.progress.value = 5
            self.progress.repaint()
        else:
            self.progress.value += 1
            self.progress.repaint()
        self.timer.start(1)

class ToggleButton(QCheckBox):

    def __init__(self):
        QCheckBox.__init__(self)
        self.status=True
        self.value=80
        self.width=52
        self.height=32

        self.bgInativo="#edeff3"
        self.bgAtivo="#005288"

        self.stateChanged.connect(self.Clicado)
        self.setFixedSize(self.width,self.height)
        self.setCursor(Qt.PointingHandCursor)
        self.repaint()

    def Clicado(self):

        return self.isChecked()

    def paintEvent(self, QPaintEvent):
        p=QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(Qt.NoPen)

        rect=QRect(0,0,self.width,self.height)
        if self.isChecked():
            p.setBrush(QColor(self.bgInativo))
            p.drawRoundedRect(0,0,rect.width(),self.height,self.height/2,self.height/2)
            p.setBrush(QColor("#ffffff"))
            p.drawEllipse(3, 1, 30, 30)
        else:
            p.setBrush(QColor(self.bgAtivo))
            p.drawRoundedRect(0, 0, rect.width(), self.height, self.height / 2, self.height / 2)
            p.setBrush(QColor("#ffffff"))
            p.drawEllipse(self.width-33, 1, 30, 30)

        p.end()

    def hitButton(self, pos:QPoint):
        return self.contentsRect().contains(pos)

    def callback(self):
        self.status=~self.status
if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    sys.exit(app.exec_())
