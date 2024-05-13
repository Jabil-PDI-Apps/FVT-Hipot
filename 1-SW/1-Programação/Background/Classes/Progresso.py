import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(250,250)

        self.container=QFrame()
        self.layout=QVBoxLayout()
        self.container.setStyleSheet(
            "background-color:#fff"
        )
        self.progress=CircularProgress()

        self.layout.addWidget(self.progress)
        
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        self.timer=QTimer()
        self.show()
        self.timer.timeout.connect(self.callback)
        self.timer.start(5)

    def callback(self):
        self.timer.stop()
        if self.progress.value+1>360:
            self.progress.value=5
            self.progress.repaint()
        else:
            self.progress.value+=1
            self.progress.repaint()
        self.timer.start(1)


class CircularProgress(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.value=80
        self.width=130
        self.height=130
        self.acc=40
        self.progress_width=10
        self.progress_rounded_cap=True
        self.progress_color=0x005288
        self.backProgressColor=0xf5f6f7
        self.corTexto=0x545e6b
        self.max_value=100
        self.animation_type="off"
        self.timer=QTimer()
        self.timer.timeout.connect(self.callback)

        self.resize(self.width,self.height)

    def paintEvent(self, QPaintEvent):
        #parametros de progresso

        width=self.width-self.progress_width
        height=self.height-self.progress_width
        margin=self.progress_width/2
        value=self.value


        paint=QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        paint.setFont(QFont("Times",20,QFont.Weight.Bold))
        rect=QRect(0,-10,self.width,self.height)
        rect2 = QRect(0, 15, self.width, self.height)
        paint.setPen(Qt.PenStyle.NoPen)


        #paint.drawRect(rect)

        pen=QPen()
        pen.setWidth(self.progress_width)
        pen.setColor(QColor(self.backProgressColor))
        paint.setPen(pen)

        # paint.drawArc(margin,margin,width,height,-90*16,-value*16)
        paint.drawArc(margin, margin, height, width, 0 * 16, 360 * 16)
        pen.setColor(QColor(self.progress_color))

        if self.animation_type=="load":

            paint.setPen(pen)
            paint.drawArc(margin, margin, width, height, value * 16, 40 * 16)

        elif self.animation_type=="completo":
            paint.setPen(pen)
            paint.drawArc(margin, margin, width, height, value * 16, 360 * 16)
        paint.setPen(QColor(self.corTexto))
        paint.drawText(rect,Qt.AlignCenter,"0.00")

        paint.setFont(QFont("Times", 10))
        paint.drawText(rect2, Qt.AlignCenter, "Volts")

        paint.end()

    def setType(self,tipo):

        self.animation_type=tipo
        if tipo=="load":
            self.timer.start(5)


    def callback(self):
        self.timer.stop()

        if self.value + 1 > 360:
            self.value = 5
            self.repaint()
        else:
            self.value += 1
            self.repaint()

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=MainWindow()
    sys.exit(app.exec_())