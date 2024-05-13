import time

from PyQt5 import QtCore, QtGui, QtWidgets

from functools import partial
from collections import defaultdict
from datetime import datetime

from Classes.Banco import BancoDeDados

from Classes.Progresso import CircularProgress
from Classes.Toggle import ToggleButton

from datetime import datetime,timedelta

from threading import Timer
import threading

import random

import urllib.request

#self.historicoModeloCombo = CheckableComboBox(self.filtroJanela)
#self.toggleHIPOT_2 = ToggleButton()

class ProgramThread(QtCore.QThread):

    update_data=QtCore.pyqtSignal(int)

    def run(self):

        self.lista=defaultdict(list)
        self.lista["status"]=[ui.statusTeste1,ui.statusTeste1_2,ui.statusTeste1_3]

        self.ct=0
        teste=0

class ErrosThread(QtCore.QThread):
    update_data = QtCore.pyqtSignal(int)

    def run(self):
        res=ui.modelos.conectaBanco()
        ui.notificacoes.erroBanco = not res

class Notificacoes():

    def __init__(self):

        self.erroLogin=False

        self.erroBanco=False
        self.erroConexao=False


    def callbackNotificacao(self):

        if self.erroConexao:
            self.checkNetwork('https://www.google.com/')

        if self.erroConexao:
            ui.WidgetPopUp.setFixedWidth(1371)
            ui.tituloPopUp.setText("Erro de Conexão")
            ui.descricaoPopUp.setText("Computador está offline, por favor contate o time de TI.")
            ui.erroLogin.setText("Sem conexão com a rede")

        elif self.erroBanco:
            ui.WidgetPopUp.setFixedWidth(1371)
            ui.tituloPopUp.setText("Erro de Conexão")
            ui.descricaoPopUp.setText("Sem conexão com o banco de dados, por favor contate o time de TI.")
            ui.erroLogin.setText("Sem conexão com bando de dados")

        elif self.erroLogin:
            ui.erroLogin.setText("Controle e/ou senha inválidos")
        else:
            ui.WidgetPopUp.setFixedWidth(0)
            ui.erroLogin.setText("")


    def isfloat(self,num):
        try:
            float(num)
            return True
        except ValueError:
            return False


    def checkNetwork(self,host):
        try:
            urllib.request.urlopen(host,timeout=2)  # Python 3.x
            self.erroConexao=False
        except Exception as e:
            print(e)
            self.erroConexao=True



class CheckableComboBox(QtWidgets.QComboBox):

    def addItem(self, item):
        super(CheckableComboBox, self).addItem(item)
        item = self.model().item(self.count()-1,0)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Checked)

    def TodosChecked(self):

        item = self.model().item(0,0)

        if item.checkState() == QtCore.Qt.Checked:

            for i in range(self.count()):
                item = self.model().item(i,0)
                item.setCheckState(QtCore.Qt.Checked)
        else:
            for i in range(self.count()):
                item = self.model().item(i,0)
                item.setCheckState(QtCore.Qt.Unchecked)

    def itemChecked(self, index):
        item = self.model().item(index,0)

        return item.checkState() == QtCore.Qt.Checked

    def handle_item_pressed(self, index):
        item = self.model().item(index,0)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

    def CustomEdit(self):

        selecionados=[]
        for i in range(self.count()):
            item = self.model().item(i,0)
            if item.checkState() == QtCore.Qt.Checked:
                selecionados.append(self.itemText(i))
        return selecionados


class Ui_MainWindow(object):

    def __init__(self):

        self.Evento=ProgramThread()
        self.ErroThread=ErrosThread()

        self.Testando=False
        self.TestandoIndex=-1


        self.filtroModelos=""

        self.usuario=""

        self.chamaTeste=QtCore.QTimer()
        self.chamaTeste.timeout.connect(self.startTestSimulated)

        self.valor=0
        self.min=[0,0,0]
        self.max=[0,0,0]

        self.data=datetime.now()

        self.visaIsConnected=False
        self.serialIsConnected=False

        self.lista=defaultdict(list)

        self.selecionadoStyle="QToolButton {\n	spacing:10px;\n    border-bottom: 1px solid gray;\n     border-top: 1px solid gray;\n    /* 16px width + 4px for border = 20px allocated above */\n    \n	background-color: rgb(0, 82, 136);\n	\n	color: rgb(255, 255, 255);\n	padding-top:15px;\n	padding-bottom:15px;\n}"
        self.naoSelecionadoStyle="QToolButton {\n	spacing:10px;\n    border-bottom: 1px solid rgb(230, 230, 230);\n     border-top: 1px solid rgb(230, 230, 230);\n    /* 16px width + 4px for border = 20px allocated above */\n    \n	background-color:white;\n	\n	color: rgb(0, 82, 136);\n	padding-top:15px;\n	padding-bottom:15px;\n}"



        self.modeloEscolhido="Nenhum"
        self.modeloEdicao=""
        self.usuarioEdicao=""

        self.horaAtualizada=datetime.now()

        self.caminhos=defaultdict(list)
        self.caminhos["nomes"]=["Status","Historico","Modelos","Usuarios","Hipot"]
        self.caminhos["local"]=["../Icones/icon-status.svg","../Icones/icon-historico.svg","../Icones/outdoor.svg","../Icones/usuarioMenu.svg","../Icones/Hipot_Icon.svg"]

        self.totalChecked=True

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1283, 858)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget_2 = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget_2.setGeometry(QtCore.QRect(0, 0, 1280, 861))
        self.stackedWidget_2.setObjectName("stackedWidget_2")
        self.generalPage = QtWidgets.QWidget()
        self.generalPage.setObjectName("generalPage")
        self.widget_9 = QtWidgets.QWidget(self.generalPage)
        self.widget_9.setGeometry(QtCore.QRect(0, 790, 1371, 68))
        self.widget_9.setStyleSheet("background-color: rgb(0, 82, 136);")
        self.widget_9.setObjectName("widget_9")
        self.label_17 = QtWidgets.QLabel(self.widget_9)
        self.label_17.setGeometry(QtCore.QRect(567, 28, 83, 15))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(8)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.widget_9)
        self.label_18.setGeometry(QtCore.QRect(654, 28, 45, 15))
        self.label_18.setText("")
        self.label_18.setPixmap(QtGui.QPixmap("../Icones/brand-indt.png"))
        self.label_18.setScaledContents(True)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.widget_9)
        self.label_19.setGeometry(QtCore.QRect(700, 28, 127, 15))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(8)
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_19.setObjectName("label_19")
        self.label_28 = QtWidgets.QLabel(self.widget_9)
        self.label_28.setGeometry(QtCore.QRect(1100, 20, 125, 20))
        self.label_28.setText("")
        self.label_28.setPixmap(QtGui.QPixmap("../Icones/logo_inferior.svg"))
        self.label_28.setObjectName("label_28")
        self.pushButton = QtWidgets.QPushButton(self.generalPage)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 90, 80))
        self.pushButton.setStyleSheet("color: rgb(0, 82, 136);\n"
                                      "border:None;\n"
                                      "background-color: rgb(255, 255, 255);")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Icones/icon-menu.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(24, 19))
        self.pushButton.setObjectName("pushButton")
        self.widget = QtWidgets.QWidget(self.generalPage)
        self.widget.setGeometry(QtCore.QRect(0, 80, 90, 710))
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget.setObjectName("widget")
        self.historicoBotao = QtWidgets.QToolButton(self.widget)
        self.historicoBotao.setGeometry(QtCore.QRect(0, 0, 90, 90))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        self.historicoBotao.setFont(font)
        self.historicoBotao.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.historicoBotao.setStyleSheet("QToolButton {\n"
                                          "    spacing:10px;\n"
                                          "    border-bottom: 1px solid rgb(230, 230, 230);\n"
                                          "     border-top: 1px solid rgb(230, 230, 230);\n"
                                          "    /* 16px width + 4px for border = 20px allocated above */\n"
                                          "    \n"
                                          "    background-color:white;\n"
                                          "    \n"
                                          "    color: rgb(0, 82, 136);\n"
                                          "    padding-top:15px;\n"
                                          "    padding-bottom:15px;\n"
                                          "}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Icones/log-icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.historicoBotao.setIcon(icon1)
        self.historicoBotao.setIconSize(QtCore.QSize(27, 27))
        self.historicoBotao.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.historicoBotao.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.historicoBotao.setAutoRaise(False)
        self.historicoBotao.setArrowType(QtCore.Qt.NoArrow)
        self.historicoBotao.setObjectName("historicoBotao")
        self.usuarioBotao = QtWidgets.QToolButton(self.widget)
        self.usuarioBotao.setGeometry(QtCore.QRect(0, 180, 90, 90))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        self.usuarioBotao.setFont(font)
        self.usuarioBotao.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.usuarioBotao.setStyleSheet("QToolButton {\n"
                                        "    spacing:10px;\n"
                                        "    border-bottom: 1px solid rgb(230, 230, 230);\n"
                                        "     border-top: 1px solid rgb(230, 230, 230);\n"
                                        "    /* 16px width + 4px for border = 20px allocated above */\n"
                                        "    \n"
                                        "    background-color:white;\n"
                                        "    \n"
                                        "    color: rgb(0, 82, 136);\n"
                                        "    padding-top:15px;\n"
                                        "    padding-bottom:15px;\n"
                                        "}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../Icones/local_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.usuarioBotao.setIcon(icon2)
        self.usuarioBotao.setIconSize(QtCore.QSize(27, 27))
        self.usuarioBotao.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.usuarioBotao.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.usuarioBotao.setAutoRaise(False)
        self.usuarioBotao.setArrowType(QtCore.Qt.NoArrow)
        self.usuarioBotao.setObjectName("usuarioBotao")
        self.modeloBotao = QtWidgets.QToolButton(self.widget)
        self.modeloBotao.setGeometry(QtCore.QRect(0, 90, 90, 90))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        self.modeloBotao.setFont(font)
        self.modeloBotao.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.modeloBotao.setStyleSheet("QToolButton {\n"
                                       "    spacing:10px;\n"
                                       "    border-bottom: 1px solid rgb(230, 230, 230);\n"
                                       "     border-top: 1px solid rgb(230, 230, 230);\n"
                                       "    /* 16px width + 4px for border = 20px allocated above */\n"
                                       "    \n"
                                       "    background-color:white;\n"
                                       "    \n"
                                       "    color: rgb(0, 82, 136);\n"
                                       "    padding-top:15px;\n"
                                       "    padding-bottom:15px;\n"
                                       "}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../Icones/server_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.modeloBotao.setIcon(icon3)
        self.modeloBotao.setIconSize(QtCore.QSize(37, 27))
        self.modeloBotao.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.modeloBotao.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.modeloBotao.setAutoRaise(False)
        self.modeloBotao.setArrowType(QtCore.Qt.NoArrow)
        self.modeloBotao.setObjectName("modeloBotao")
        self.label_27 = QtWidgets.QLabel(self.generalPage)
        self.label_27.setGeometry(QtCore.QRect(150, 29, 164, 27))
        self.label_27.setText("")
        self.label_27.setPixmap(QtGui.QPixmap("../Icones/logo_superior.svg"))
        self.label_27.setObjectName("label_27")
        self.label_25 = QtWidgets.QLabel(self.generalPage)
        self.label_25.setGeometry(QtCore.QRect(322, 23, 3, 40))
        self.label_25.setStyleSheet("background-color: rgb(84, 192, 232);")
        self.label_25.setText("")
        self.label_25.setObjectName("label_25")
        self.label_24 = QtWidgets.QLabel(self.generalPage)
        self.label_24.setGeometry(QtCore.QRect(340, 11, 251, 61))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setStyleSheet("color: rgb(0, 82, 136);")
        self.label_24.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.stackedWidget = QtWidgets.QStackedWidget(self.generalPage)
        self.stackedWidget.setGeometry(QtCore.QRect(90, 80, 1274, 710))
        self.stackedWidget.setObjectName("stackedWidget")
        self.StatusPage = QtWidgets.QWidget()
        self.StatusPage.setObjectName("StatusPage")
        self.StatusOption = QtWidgets.QWidget(self.StatusPage)
        self.StatusOption.setEnabled(True)
        self.StatusOption.setGeometry(QtCore.QRect(0, 0, 1274, 710))
        self.StatusOption.setStyleSheet("background-color: rgb(243, 246, 249);\n"
                                        " padding:5px;\n"
                                        "\n"
                                        "")
        self.StatusOption.setObjectName("StatusOption")
        self.verticalWidget = QtWidgets.QWidget(self.StatusOption)
        self.verticalWidget.setGeometry(QtCore.QRect(11, 260, 158, 308))
        self.verticalWidget.setStyleSheet("")
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Titulo_1 = QtWidgets.QLabel(self.verticalWidget)
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Titulo_1.setFont(font)
        self.Titulo_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Titulo_1.setStyleSheet("border-top-right-radius:7px;\n"
                                    "border-top-left-radius:7px;\n"
                                    "background-color: rgb(255, 255, 255);\n"
                                    "color: rgb(0, 82, 136);")
        self.Titulo_1.setAlignment(QtCore.Qt.AlignCenter)
        self.Titulo_1.setWordWrap(True)
        self.Titulo_1.setObjectName("Titulo_1")
        self.verticalLayout_3.addWidget(self.Titulo_1)
        self.Meio = QtWidgets.QWidget(self.verticalWidget)
        self.Meio.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Meio.setObjectName("Meio")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.Meio)
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label_4 = QtWidgets.QLabel(self.Meio)
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("../Icones/Aguardando.svg"))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_3.addWidget(self.Meio)
        self.statusTeste1 = QtWidgets.QLabel(self.verticalWidget)
        self.statusTeste1.setMaximumSize(QtCore.QSize(240, 92))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.statusTeste1.setFont(font)
        self.statusTeste1.setStyleSheet("color: rgb(84, 94, 107);\n"
                                        "background-color: rgb(224, 224, 224);\n"
                                        "border-bottom-right-radius: 7px; \n"
                                        "border-bottom-left-radius: 7px; \n"
                                        "")
        self.statusTeste1.setText("AGUARDANDO")
        self.statusTeste1.setTextFormat(QtCore.Qt.RichText)
        self.statusTeste1.setScaledContents(False)
        self.statusTeste1.setAlignment(QtCore.Qt.AlignCenter)
        self.statusTeste1.setObjectName("statusTeste1")
        self.verticalLayout_3.addWidget(self.statusTeste1)
        self.widget_4 = QtWidgets.QWidget(self.StatusOption)
        self.widget_4.setGeometry(QtCore.QRect(10, 149, 496, 100))
        self.widget_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                    "border-radius:7px;\n"
                                    "")
        self.widget_4.setObjectName("widget_4")
        self.widget_5 = QtWidgets.QWidget(self.widget_4)
        self.widget_5.setGeometry(QtCore.QRect(134, 49, 328, 31))
        self.widget_5.setStyleSheet("background-color: rgb(245, 246, 247);")
        self.widget_5.setObjectName("widget_5")
        self.label_6 = QtWidgets.QLabel(self.widget_5)
        self.label_6.setGeometry(QtCore.QRect(34, 0, 50, 30))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(84, 94, 107);")
        self.label_6.setObjectName("label_6")
        self.label_9 = QtWidgets.QLabel(self.widget_5)
        self.label_9.setGeometry(QtCore.QRect(80, 0, 220, 30))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: rgb(84, 94, 107);")
        self.label_9.setObjectName("label_9")
        self.label_7 = QtWidgets.QLabel(self.widget_4)
        self.label_7.setGeometry(QtCore.QRect(24, 18, 85, 62))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("../Icones/outdoormaior.svg"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.label = QtWidgets.QLabel(self.widget_4)
        self.label.setGeometry(QtCore.QRect(170, 10, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 82, 136);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.statusGeral = QtWidgets.QLabel(self.StatusOption)
        self.statusGeral.setGeometry(QtCore.QRect(12, 591, 495, 55))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.statusGeral.setFont(font)
        self.statusGeral.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                       "border-radius: 7px;\n"
                                       "color: rgb(84, 94, 107);")
        self.statusGeral.setAlignment(QtCore.Qt.AlignCenter)
        self.statusGeral.setObjectName("statusGeral")
        self.verticalWidget_2 = QtWidgets.QWidget(self.StatusOption)
        self.verticalWidget_2.setGeometry(QtCore.QRect(180, 260, 158, 308))
        self.verticalWidget_2.setStyleSheet("")
        self.verticalWidget_2.setObjectName("verticalWidget_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalWidget_2)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Titulo_2 = QtWidgets.QLabel(self.verticalWidget_2)
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Titulo_2.setFont(font)
        self.Titulo_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Titulo_2.setStyleSheet("border-top-right-radius:7px;\n"
                                    "border-top-left-radius:7px;\n"
                                    "background-color: rgb(255, 255, 255);\n"
                                    "color: rgb(0, 82, 136);")
        self.Titulo_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Titulo_2.setWordWrap(True)
        self.Titulo_2.setObjectName("Titulo_2")
        self.verticalLayout_4.addWidget(self.Titulo_2)
        self.Meio_2 = QtWidgets.QWidget(self.verticalWidget_2)
        self.Meio_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Meio_2.setObjectName("Meio_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.Meio_2)
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.label_5 = QtWidgets.QLabel(self.Meio_2)
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("../Icones/AprovadoMaior.svg"))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_4.addWidget(self.label_5)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_4.addWidget(self.Meio_2)
        self.statusTeste1_2 = QtWidgets.QLabel(self.verticalWidget_2)
        self.statusTeste1_2.setMaximumSize(QtCore.QSize(240, 92))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.statusTeste1_2.setFont(font)
        self.statusTeste1_2.setStyleSheet("color: rgb(84, 94, 107);\n"
                                          "background-color: rgb(224, 224, 224);\n"
                                          "border-bottom-right-radius: 7px; \n"
                                          "border-bottom-left-radius: 7px; \n"
                                          "")
        self.statusTeste1_2.setText("AGUARDANDO")
        self.statusTeste1_2.setTextFormat(QtCore.Qt.RichText)
        self.statusTeste1_2.setScaledContents(False)
        self.statusTeste1_2.setAlignment(QtCore.Qt.AlignCenter)
        self.statusTeste1_2.setObjectName("statusTeste1_2")
        self.verticalLayout_4.addWidget(self.statusTeste1_2)
        self.label_35 = QtWidgets.QLabel(self.StatusOption)
        self.label_35.setGeometry(QtCore.QRect(22, 30, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.label_35.setFont(font)
        self.label_35.setStyleSheet("color: rgb(0, 82, 136);\n"
                                    "margin:-5px;\n"
                                    "")
        self.label_35.setObjectName("label_35")
        self.label_2 = QtWidgets.QLabel(self.StatusOption)
        self.label_2.setGeometry(QtCore.QRect(20, 69, 167, 3))
        self.label_2.setStyleSheet("background-color: rgb(84, 192, 232);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.verticalWidget_3 = QtWidgets.QWidget(self.StatusOption)
        self.verticalWidget_3.setGeometry(QtCore.QRect(350, 260, 158, 308))
        self.verticalWidget_3.setStyleSheet("")
        self.verticalWidget_3.setObjectName("verticalWidget_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalWidget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.Titulo_3 = QtWidgets.QLabel(self.verticalWidget_3)
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Titulo_3.setFont(font)
        self.Titulo_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Titulo_3.setStyleSheet("border-top-right-radius:7px;\n"
                                    "border-top-left-radius:7px;\n"
                                    "background-color: rgb(255, 255, 255);\n"
                                    "color: rgb(0, 82, 136);")
        self.Titulo_3.setAlignment(QtCore.Qt.AlignCenter)
        self.Titulo_3.setWordWrap(True)
        self.Titulo_3.setObjectName("Titulo_3")
        self.verticalLayout_5.addWidget(self.Titulo_3)
        self.Meio_3 = QtWidgets.QWidget(self.verticalWidget_3)
        self.Meio_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.Meio_3.setObjectName("Meio_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.Meio_3)
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.label_8 = QtWidgets.QLabel(self.Meio_3)
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("../Icones/ReprovadoMaior.svg"))
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_5.addWidget(self.label_8)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.verticalLayout_5.addWidget(self.Meio_3)
        self.statusTeste1_3 = QtWidgets.QLabel(self.verticalWidget_3)
        self.statusTeste1_3.setMaximumSize(QtCore.QSize(240, 92))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.statusTeste1_3.setFont(font)
        self.statusTeste1_3.setStyleSheet("color: rgb(84, 94, 107);\n"
                                          "background-color: rgb(224, 224, 224);\n"
                                          "border-bottom-right-radius: 7px; \n"
                                          "border-bottom-left-radius: 7px; \n"
                                          "")
        self.statusTeste1_3.setText("AGUARDANDO")
        self.statusTeste1_3.setTextFormat(QtCore.Qt.RichText)
        self.statusTeste1_3.setScaledContents(False)
        self.statusTeste1_3.setAlignment(QtCore.Qt.AlignCenter)
        self.statusTeste1_3.setObjectName("statusTeste1_3")
        self.verticalLayout_5.addWidget(self.statusTeste1_3)
        self.label_20 = QtWidgets.QLabel(self.StatusOption)
        self.label_20.setGeometry(QtCore.QRect(44, 86, 44, 44))
        self.label_20.setText("")
        self.label_20.setPixmap(QtGui.QPixmap("../../../../Jabil_HIPOT/3-SW/Saída/Icones/refreshTeste.svg"))
        self.label_20.setScaledContents(True)
        self.label_20.setObjectName("label_20")
        self.tableWidget = QtWidgets.QTableWidget(self.StatusOption)
        self.tableWidget.setGeometry(QtCore.QRect(510, 145, 681, 491))
        font = QtGui.QFont()
        font.setFamily("Lato")
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("QTableWidget {\n"
                                       "    border: None;\n"
                                       "    border-radius: 7px;\n"
                                       "    background-color:;\n"
                                       "    background-color: rgb(243, 246, 249);\n"
                                       "}\n"
                                       "\n"
                                       "QTableWidget::item {\n"
                                       "    \n"
                                       "    background-color: white;\n"
                                       "    color:rgb(84, 94, 107);\n"
                                       "    max-height:40px;\n"
                                       "    border:None;\n"
                                       "    margin-bottom:3px;\n"
                                       "    \n"
                                       "}\n"
                                       "\n"
                                       "QHeaderView::section{\n"
                                       "    Background-color:rgb(0, 82, 136);\n"
                                       "   border-radius:7px;\n"
                                       "    color:white;\n"
                                       "    height:40px;\n"
                                       "    text-align: center;\n"
                                       "}\n"
                                       "\n"
                                       "QHeaderView{\n"
                                       "     border-top-right-radius:7px;\n"
                                       "    border-top-left-radius:7px;\n"
                                       "    Background-color:rgb(0, 82, 136);\n"
                                       "}\n"
                                       "\n"
                                       "QTableCornerButton::section{\n"
                                       "           \n"
                                       "            border-left:0px solid #D8D8D8;\n"
                                       "           \n"
                                       "           background-color:black;}")
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setAlternatingRowColors(False)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Lato")
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Lato")
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Lato")
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Lato")
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Lato")
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Lato")
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(113)
        self.tableWidget.horizontalHeader().setHighlightSections(False)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(37)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(52)
        self.tableWidget.verticalHeader().setMinimumSectionSize(52)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.acionaFiltro = QtWidgets.QPushButton(self.StatusOption)
        self.acionaFiltro.setGeometry(QtCore.QRect(1036, 90, 136, 38))
        self.acionaFiltro.setStyleSheet("QPushButton{\n"
                                        "background-color: rgb(0, 82, 136);\n"
                                        "border-radius:19px;\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "font: 12pt \"Lato\";\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "background-color: rgb(1, 110, 181);\n"
                                        "}")
        self.acionaFiltro.setObjectName("acionaFiltro")
        self.label_21 = QtWidgets.QLabel(self.StatusOption)
        self.label_21.setGeometry(QtCore.QRect(1010, 9, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("color: rgb(0, 82, 136);\n"
                                    "margin:-5px;\n"
                                    "")
        self.label_21.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing)
        self.label_21.setObjectName("label_21")
        self.filtroJanela = QtWidgets.QWidget(self.StatusOption)
        self.filtroJanela.setGeometry(QtCore.QRect(320, 130, 0, 361))
        self.filtroJanela.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                        "border-radius:5px;")
        self.filtroJanela.setObjectName("filtroJanela")
        self.label_36 = QtWidgets.QLabel(self.filtroJanela)
        self.label_36.setGeometry(QtCore.QRect(24, 31, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setStyleSheet("color: rgb(0, 82, 136);\n"
                                    "margin:-5px;\n"
                                    "")
        self.label_36.setObjectName("label_36")
        self.label_3 = QtWidgets.QLabel(self.filtroJanela)
        self.label_3.setGeometry(QtCore.QRect(25, 52, 51, 3))
        self.label_3.setStyleSheet("background-color: rgb(84, 192, 232);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.historicoModeloCombo = CheckableComboBox(self.filtroJanela)
        self.historicoModeloCombo.setGeometry(QtCore.QRect(25, 110, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.historicoModeloCombo.setFont(font)
        self.historicoModeloCombo.setStyleSheet("QComboBox {\n"
                                                "    \n"
                                                "    border-radius: 3px;\n"
                                                "    border-width:1px;\n"
                                                "    border-style:solid;\n"
                                                "    border-color:rgb(243, 241, 241);\n"
                                                "    padding: 1px 18px 1px 8px;\n"
                                                "    \n"
                                                "    color: rgb(82, 94, 108);\n"
                                                "    background: white;\n"
                                                "    \n"
                                                "}\n"
                                                "\n"
                                                "QComboBox:editable {\n"
                                                "    background: white;\n"
                                                "}\n"
                                                "\n"
                                                "QComboBox::drop-down {\n"
                                                "    subcontrol-origin: padding;\n"
                                                "    subcontrol-position: top right;\n"
                                                "    width: 36px;\n"
                                                "    \n"
                                                "    background-color: rgb(0, 82, 136);\n"
                                                "    border-left-width: 1px;\n"
                                                "    border-left-color: pink;\n"
                                                "    border-left-style: solid; /* just a single line */\n"
                                                "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                                "    border-bottom-right-radius: 3px;\n"
                                                "}\n"
                                                "\n"
                                                "QComboBox::down-arrow {\n"
                                                "   image:url(:/newPrefix/arrow3.png)\n"
                                                "}")
        self.historicoModeloCombo.setEditable(False)
        self.historicoModeloCombo.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.historicoModeloCombo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.historicoModeloCombo.setIconSize(QtCore.QSize(26, 26))
        self.historicoModeloCombo.setDuplicatesEnabled(False)
        self.historicoModeloCombo.setModelColumn(0)
        self.historicoModeloCombo.setObjectName("historicoModeloCombo")
        self.historicoModeloCombo.addItem("")
        self.label_22 = QtWidgets.QLabel(self.filtroJanela)
        self.label_22.setGeometry(QtCore.QRect(25, 80, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("color: rgb(0, 82, 136);\n"
                                    "margin:-5px;\n"
                                    "")
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.filtroJanela)
        self.label_23.setGeometry(QtCore.QRect(300, 80, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("color: rgb(0, 82, 136);\n"
                                    "margin:-5px;\n"
                                    "")
        self.label_23.setObjectName("label_23")
        self.statusCombBox = QtWidgets.QComboBox(self.filtroJanela)
        self.statusCombBox.setGeometry(QtCore.QRect(300, 110, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.statusCombBox.setFont(font)
        self.statusCombBox.setStyleSheet("QComboBox {\n"
                                         "    \n"
                                         "    border-radius: 3px;\n"
                                         "    border-width:1px;\n"
                                         "    border-style:solid;\n"
                                         "    border-color:rgb(243, 241, 241);\n"
                                         "    padding: 1px 18px 1px 8px;\n"
                                         "    \n"
                                         "    color: rgb(82, 94, 108);\n"
                                         "    background: white;\n"
                                         "    \n"
                                         "}\n"
                                         "\n"
                                         "QComboBox:editable {\n"
                                         "    background: white;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox::drop-down {\n"
                                         "    subcontrol-origin: padding;\n"
                                         "    subcontrol-position: top right;\n"
                                         "    width: 36px;\n"
                                         "    \n"
                                         "    background-color: rgb(0, 82, 136);\n"
                                         "    border-left-width: 1px;\n"
                                         "    border-left-color: pink;\n"
                                         "    border-left-style: solid; /* just a single line */\n"
                                         "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                         "    border-bottom-right-radius: 3px;\n"
                                         "}\n"
                                         "\n"
                                         "QComboBox::down-arrow {\n"
                                         "   image:url(:/newPrefix/arrow3.png)\n"
                                         "}")
        self.statusCombBox.setEditable(False)
        self.statusCombBox.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.statusCombBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        self.statusCombBox.setIconSize(QtCore.QSize(26, 26))
        self.statusCombBox.setDuplicatesEnabled(False)
        self.statusCombBox.setModelColumn(0)
        self.statusCombBox.setObjectName("statusCombBox")
        self.statusCombBox.addItem("")
        self.statusCombBox.addItem("")
        self.statusCombBox.addItem("")
        self.label_26 = QtWidgets.QLabel(self.filtroJanela)
        self.label_26.setGeometry(QtCore.QRect(25, 190, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_26.setFont(font)
        self.label_26.setStyleSheet("color: rgb(0, 82, 136);\n"
                                    "margin:-5px;\n"
                                    "")
        self.label_26.setObjectName("label_26")
        self.label_31 = QtWidgets.QLabel(self.filtroJanela)
        self.label_31.setGeometry(QtCore.QRect(300, 190, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_31.setFont(font)
        self.label_31.setStyleSheet("color: rgb(0, 82, 136);\n"
                                    "margin:-5px;\n"
                                    "")
        self.label_31.setObjectName("label_31")
        self.limpaTela = QtWidgets.QPushButton(self.filtroJanela)
        self.limpaTela.setGeometry(QtCore.QRect(80, 300, 170, 50))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.limpaTela.setFont(font)
        self.limpaTela.setStyleSheet("QPushButton{\n"
                                     "border:1px solid rgb(0, 82, 136);\n"
                                     "color: rgb(0, 82, 136);\n"
                                     "border-radius:25px;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover{\n"
                                     "background-color: rgb(0, 82, 136);\n"
                                     "    color: rgb(255, 255, 255);\n"
                                     "}")
        self.limpaTela.setObjectName("limpaTela")
        self.buscarButton = QtWidgets.QPushButton(self.filtroJanela)
        self.buscarButton.setGeometry(QtCore.QRect(270, 300, 170, 50))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.buscarButton.setFont(font)
        self.buscarButton.setStyleSheet("QPushButton{\n"
                                        "border:1px solid rgb(0, 82, 136);\n"
                                        "color: white;\n"
                                        "background-color: rgb(0, 82, 136);\n"
                                        "border-radius:25px;\n"
                                        "}\n"
                                        "QPushButton:hover{\n"
                                        "background-color: rgb(1, 110, 181);\n"
                                        "}")
        self.buscarButton.setObjectName("buscarButton")
        self.dataInicio = QtWidgets.QDateEdit(self.filtroJanela)
        self.dataInicio.setGeometry(QtCore.QRect(25, 220, 171, 31))
        self.dataInicio.setStyleSheet("QDateEdit {\n"
                                      "    \n"
                                      "    border-radius: 3px;\n"
                                      "    padding: 1px 18px 1px 8px;\n"
                                      "    border-width:1px;\n"
                                      "    border-style:solid;\n"
                                      "    border-color:rgb(243, 241, 241);\n"
                                      "    color: rgb(82, 94, 108);\n"
                                      "    background: white;\n"
                                      "    \n"
                                      "}\n"
                                      "\n"
                                      "\n"
                                      "QDateEdit::drop-down {\n"
                                      "    subcontrol-origin: padding;\n"
                                      "    subcontrol-position: top right;\n"
                                      "    width: 36px;\n"
                                      "    \n"
                                      "    background-color: rgb(0, 82, 136);\n"
                                      "    border-left-width: 1px;\n"
                                      "    border-left-color: pink;\n"
                                      "    border-left-style: solid; /* just a single line */\n"
                                      "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                      "    border-bottom-right-radius: 3px;\n"
                                      "}\n"
                                      "\n"
                                      "QDateEdit::down-arrow {\n"
                                      "   image:url(:/newPrefix/arrow3.png)\n"
                                      "}\n"
                                      "\n"
                                      "QCalendarWidget QToolButton {\n"
                                      "      height: 20px;\n"
                                      "      width: 60px;\n"
                                      "      color: rgb(0, 82, 136);\n"
                                      "      font-size: 12px;\n"
                                      "      icon-size: 12px, 12px;\n"
                                      "      background-color:rgb(230, 230, 230);\n"
                                      "  }\n"
                                      "  QCalendarWidget QMenu {\n"
                                      "      width: 120px;\n"
                                      "      left: 5px;\n"
                                      "      color: rgb(0,0, 0);\n"
                                      "      font-size: 15px;\n"
                                      "    border-radius:10px\n"
                                      "      \n"
                                      "  }\n"
                                      "  QCalendarWidget QSpinBox { \n"
                                      "      width: 40px; \n"
                                      "      font-size:12px; \n"
                                      "      color: black; \n"
                                      "      \n"
                                      "      selection-background-color: rgb(136, 136, 136);\n"
                                      "      selection-color: rgb(255, 255, 255);\n"
                                      "  }\n"
                                      "  QCalendarWidget QSpinBox::up-button { subcontrol-origin: border;  subcontrol-position: top right;  width:65px; }\n"
                                      "  QCalendarWidget QSpinBox::down-button {subcontrol-origin: border; subcontrol-position: bottom right;  width:65px;}\n"
                                      "  QCalendarWidget QSpinBox::up-arrow { width:20px;  height:20px; }\n"
                                      "  QCalendarWidget QSpinBox::down-arrow { width:20px;  height:20px; }\n"
                                      "   \n"
                                      "  /* header row */\n"
                                      "  QCalendarWidget QWidget { alternate-background-color:rgb(245, 246, 247); }\n"
                                      "   \n"
                                      "  /* normal days */\n"
                                      "  QCalendarWidget QAbstractItemView:enabled \n"
                                      "  {\n"
                                      "      font-size:12px;  \n"
                                      "      color:rgb(84, 94, 107);  \n"
                                      "    \n"
                                      "      background-color: white;  \n"
                                      "      selection-background-color:rgb(245, 246, 247); \n"
                                      "      selection-color:rgb(84, 94, 107); ; \n"
                                      "  }\n"
                                      "   \n"
                                      "  /* days in other months */\n"
                                      "  /* navigation bar */\n"
                                      "QCalendarWidget QWidget#qt_calendar_navigationbar\n"
                                      "{ \n"
                                      "  background-color: rgb(230, 230, 230);\n"
                                      " color:rgb(0, 82, 136);\n"
                                      "    \n"
                                      "}\n"
                                      "\n"
                                      "QCalendarWidget QAbstractItemView:disabled \n"
                                      "{ \n"
                                      "color:rgb(230, 230, 230); \n"
                                      "}\n"
                                      "\n"
                                      "QCalendarWidget QAbstractItemView:enabled \n"
                                      "{ \n"
                                      "color:rgb(0, 82, 136) ;\n"
                                      "}\n"
                                      "\n"
                                      "")
        self.dataInicio.setFrame(True)
        self.dataInicio.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.dataInicio.setCalendarPopup(True)
        self.dataInicio.setObjectName("dataInicio")
        self.dataFim = QtWidgets.QDateEdit(self.filtroJanela)
        self.dataFim.setGeometry(QtCore.QRect(300, 220, 171, 31))
        self.dataFim.setStyleSheet("QDateEdit {\n"
                                   "    \n"
                                   "    border-radius: 3px;\n"
                                   "    padding: 1px 18px 1px 8px;\n"
                                   "    border-width:1px;\n"
                                   "    border-style:solid;\n"
                                   "    border-color:rgb(243, 241, 241);\n"
                                   "    color: rgb(82, 94, 108);\n"
                                   "    background: white;\n"
                                   "    \n"
                                   "}\n"
                                   "\n"
                                   "\n"
                                   "QDateEdit::drop-down {\n"
                                   "    subcontrol-origin: padding;\n"
                                   "    subcontrol-position: top right;\n"
                                   "    width: 36px;\n"
                                   "    \n"
                                   "    background-color: rgb(0, 82, 136);\n"
                                   "    border-left-width: 1px;\n"
                                   "    border-left-color: pink;\n"
                                   "    border-left-style: solid; /* just a single line */\n"
                                   "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
                                   "    border-bottom-right-radius: 3px;\n"
                                   "}\n"
                                   "\n"
                                   "QDateEdit::down-arrow {\n"
                                   "   image:url(:/newPrefix/arrow3.png)\n"
                                   "}\n"
                                   "\n"
                                   "QCalendarWidget QToolButton {\n"
                                   "      height: 20px;\n"
                                   "      width: 60px;\n"
                                   "      color: rgb(0, 82, 136);\n"
                                   "      font-size: 12px;\n"
                                   "      icon-size: 12px, 12px;\n"
                                   "      background-color:rgb(230, 230, 230);\n"
                                   "  }\n"
                                   "  QCalendarWidget QMenu {\n"
                                   "      width: 120px;\n"
                                   "      left: 5px;\n"
                                   "      color: rgb(0,0, 0);\n"
                                   "      font-size: 15px;\n"
                                   "    border-radius:10px\n"
                                   "      \n"
                                   "  }\n"
                                   "  QCalendarWidget QSpinBox { \n"
                                   "      width: 40px; \n"
                                   "      font-size:12px; \n"
                                   "      color: black; \n"
                                   "      \n"
                                   "      selection-background-color: rgb(136, 136, 136);\n"
                                   "      selection-color: rgb(255, 255, 255);\n"
                                   "  }\n"
                                   "  QCalendarWidget QSpinBox::up-button { subcontrol-origin: border;  subcontrol-position: top right;  width:65px; }\n"
                                   "  QCalendarWidget QSpinBox::down-button {subcontrol-origin: border; subcontrol-position: bottom right;  width:65px;}\n"
                                   "  QCalendarWidget QSpinBox::up-arrow { width:20px;  height:20px; }\n"
                                   "  QCalendarWidget QSpinBox::down-arrow { width:20px;  height:20px; }\n"
                                   "   \n"
                                   "  /* header row */\n"
                                   "  QCalendarWidget QWidget { alternate-background-color:rgb(245, 246, 247); }\n"
                                   "   \n"
                                   "  /* normal days */\n"
                                   "  QCalendarWidget QAbstractItemView:enabled \n"
                                   "  {\n"
                                   "      font-size:12px;  \n"
                                   "      color:rgb(84, 94, 107);  \n"
                                   "    \n"
                                   "      background-color: white;  \n"
                                   "      selection-background-color:rgb(245, 246, 247); \n"
                                   "      selection-color:rgb(84, 94, 107); ; \n"
                                   "  }\n"
                                   "   \n"
                                   "  /* days in other months */\n"
                                   "  /* navigation bar */\n"
                                   "QCalendarWidget QWidget#qt_calendar_navigationbar\n"
                                   "{ \n"
                                   "  background-color: rgb(230, 230, 230);\n"
                                   " color:rgb(0, 82, 136);\n"
                                   "    \n"
                                   "}\n"
                                   "\n"
                                   "QCalendarWidget QAbstractItemView:disabled \n"
                                   "{ \n"
                                   "color:rgb(230, 230, 230); \n"
                                   "}\n"
                                   "\n"
                                   "QCalendarWidget QAbstractItemView:enabled \n"
                                   "{ \n"
                                   "color:rgb(0, 82, 136) ;\n"
                                   "}\n"
                                   "\n"
                                   "")
        self.dataFim.setFrame(True)
        self.dataFim.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
        self.dataFim.setCalendarPopup(True)
        self.dataFim.setObjectName("dataFim")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.StatusOption)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(1106, 50, 78, 31))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.boxHipotVertical_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.boxHipotVertical_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.boxHipotVertical_4.setContentsMargins(0, 0, 0, 0)
        self.boxHipotVertical_4.setSpacing(0)
        self.boxHipotVertical_4.setObjectName("boxHipotVertical_4")
        self.toggleHIPOT_2 = ToggleButton()
        self.toggleHIPOT_2.setObjectName("toggleHIPOT_2")
        self.boxHipotVertical_4.addWidget(self.toggleHIPOT_2)
        self.label_37 = QtWidgets.QLabel(self.StatusOption)
        self.label_37.setGeometry(QtCore.QRect(520, 30, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.label_37.setFont(font)
        self.label_37.setStyleSheet("color: rgb(0, 82, 136);\n"
                                    "margin:-5px;\n"
                                    "")
        self.label_37.setObjectName("label_37")
        self.label_10 = QtWidgets.QLabel(self.StatusOption)
        self.label_10.setGeometry(QtCore.QRect(520, 69, 167, 3))
        self.label_10.setStyleSheet("background-color: rgb(84, 192, 232);")
        self.label_10.setText("")
        self.label_10.setObjectName("label_10")
        self.stackedWidget.addWidget(self.StatusPage)
        self.HistoricoPage = QtWidgets.QWidget()
        self.HistoricoPage.setObjectName("HistoricoPage")
        self.stackedWidget.addWidget(self.HistoricoPage)
        self.HipotPage = QtWidgets.QWidget()
        self.HipotPage.setObjectName("HipotPage")
        self.stackedWidget.addWidget(self.HipotPage)
        self.ModelosPage = QtWidgets.QWidget()
        self.ModelosPage.setObjectName("ModelosPage")
        self.stackedWidget.addWidget(self.ModelosPage)
        self.UsuarioPage = QtWidgets.QWidget()
        self.UsuarioPage.setObjectName("UsuarioPage")
        self.stackedWidget.addWidget(self.UsuarioPage)
        self.criaUsuarioPage = QtWidgets.QWidget()
        self.criaUsuarioPage.setObjectName("criaUsuarioPage")
        self.stackedWidget.addWidget(self.criaUsuarioPage)
        self.criaModeloPage = QtWidgets.QWidget()
        self.criaModeloPage.setObjectName("criaModeloPage")
        self.stackedWidget.addWidget(self.criaModeloPage)
        self.loginWindow = QtWidgets.QWidget(self.generalPage)
        self.loginWindow.setEnabled(True)
        self.loginWindow.setGeometry(QtCore.QRect(1010, 60, 0, 171))
        self.loginWindow.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                       "border-radius:15px;\n"
                                       "")
        self.loginWindow.setObjectName("loginWindow")
        self.UsuarioMenuNome = QtWidgets.QLabel(self.loginWindow)
        self.UsuarioMenuNome.setGeometry(QtCore.QRect(35, 29, 181, 20))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.UsuarioMenuNome.setFont(font)
        self.UsuarioMenuNome.setStyleSheet("color: rgb(0, 82, 136);")
        self.UsuarioMenuNome.setObjectName("UsuarioMenuNome")
        self.usuarioMudaBotao = QtWidgets.QPushButton(self.loginWindow)
        self.usuarioMudaBotao.setGeometry(QtCore.QRect(0, 84, 235, 43))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(12)
        self.usuarioMudaBotao.setFont(font)
        self.usuarioMudaBotao.setStyleSheet("border-top-width:1px;\n"
                                            "border-bottom-width:1px;\n"
                                            "border-style:solid;\n"
                                            "border-color:rgb(229, 231, 235);\n"
                                            "border-radius:0;\n"
                                            "text-align:left;\n"
                                            "padding-left:10px;\n"
                                            "color: rgb(84, 94, 107);\n"
                                            "\n"
                                            "")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../../../../Jabil_HIPOT/3-SW/Icones/cadastro.svg"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.usuarioMudaBotao.setIcon(icon4)
        self.usuarioMudaBotao.setIconSize(QtCore.QSize(20, 20))
        self.usuarioMudaBotao.setObjectName("usuarioMudaBotao")
        self.LogoutBotao = QtWidgets.QPushButton(self.loginWindow)
        self.LogoutBotao.setGeometry(QtCore.QRect(0, 127, 235, 43))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(12)
        self.LogoutBotao.setFont(font)
        self.LogoutBotao.setStyleSheet("border-top-width:1px;\n"
                                       "border-bottom-width:1px;\n"
                                       "border-style:solid;\n"
                                       "border-color:rgb(229, 231, 235);\n"
                                       "border-radius:0;\n"
                                       "text-align:left;\n"
                                       "padding-left:10px;\n"
                                       "color: rgb(84, 94, 107);\n"
                                       "border-bottom-right-radius: 5px; \n"
                                       "border-bottom-left-radius: 5px; \n"
                                       "\n"
                                       "")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../../../../Jabil_HIPOT/3-SW/Icones/logout.svg"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.LogoutBotao.setIcon(icon5)
        self.LogoutBotao.setIconSize(QtCore.QSize(20, 20))
        self.LogoutBotao.setObjectName("LogoutBotao")
        self.UsuarioNome = QtWidgets.QToolButton(self.generalPage)
        self.UsuarioNome.setGeometry(QtCore.QRect(1040, 30, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.UsuarioNome.setFont(font)
        self.UsuarioNome.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.UsuarioNome.setStyleSheet("QToolButton {\n"
                                       "    spacing:10px;\n"
                                       "    border:None;\n"
                                       "    /* 16px width + 4px for border = 20px allocated above */\n"
                                       "    \n"
                                       "    background-color:white;\n"
                                       "    \n"
                                       "    color: rgb(0, 82, 136);\n"
                                       "    padding-left:15px;\n"
                                       "    \n"
                                       "}")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../Icones/ic_arrow.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.UsuarioNome.setIcon(icon6)
        self.UsuarioNome.setIconSize(QtCore.QSize(20, 20))
        self.UsuarioNome.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.UsuarioNome.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.UsuarioNome.setAutoRaise(False)
        self.UsuarioNome.setArrowType(QtCore.Qt.NoArrow)
        self.UsuarioNome.setObjectName("UsuarioNome")
        self.WidgetPopUp = QtWidgets.QWidget(self.generalPage)
        self.WidgetPopUp.setGeometry(QtCore.QRect(0, 0, 0, 861))
        self.WidgetPopUp.setStyleSheet("background-color: rgba(0, 0, 0,0.4);\n"
                                       "")
        self.WidgetPopUp.setObjectName("WidgetPopUp")
        self.widget_26 = QtWidgets.QWidget(self.WidgetPopUp)
        self.widget_26.setGeometry(QtCore.QRect(418, 190, 542, 410))
        self.widget_26.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                     "border-radius:7px;")
        self.widget_26.setObjectName("widget_26")
        self.label_11 = QtWidgets.QLabel(self.widget_26)
        self.label_11.setGeometry(QtCore.QRect(220, 30, 111, 101))
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap("../../../../Jabil_HIPOT/3-SW/Icones/bloqueioAviso.svg"))
        self.label_11.setScaledContents(True)
        self.label_11.setObjectName("label_11")
        self.tituloPopUp = QtWidgets.QLabel(self.widget_26)
        self.tituloPopUp.setGeometry(QtCore.QRect(80, 140, 391, 51))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.tituloPopUp.setFont(font)
        self.tituloPopUp.setStyleSheet("color: rgb(0, 82, 136);")
        self.tituloPopUp.setAlignment(QtCore.Qt.AlignCenter)
        self.tituloPopUp.setObjectName("tituloPopUp")
        self.descricaoPopUp = QtWidgets.QLabel(self.widget_26)
        self.descricaoPopUp.setGeometry(QtCore.QRect(100, 190, 351, 101))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.descricaoPopUp.setFont(font)
        self.descricaoPopUp.setStyleSheet("color: rgb(84, 94, 107);")
        self.descricaoPopUp.setAlignment(QtCore.Qt.AlignCenter)
        self.descricaoPopUp.setWordWrap(True)
        self.descricaoPopUp.setObjectName("descricaoPopUp")
        self.botaoPopUp = QtWidgets.QPushButton(self.widget_26)
        self.botaoPopUp.setGeometry(QtCore.QRect(182, 320, 178, 54))
        self.botaoPopUp.setStyleSheet("QPushButton{\n"
                                      "background-color: rgb(0, 82, 136);\n"
                                      "border-radius:27px;\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "font: 12pt \"Lato\";\n"
                                      "}\n"
                                      "QPushButton:hover{\n"
                                      "background-color: rgb(1, 110, 181);\n"
                                      "}")
        self.botaoPopUp.setObjectName("botaoPopUp")
        self.stackedWidget_2.addWidget(self.generalPage)
        self.loginPage = QtWidgets.QWidget()
        self.loginPage.setObjectName("loginPage")
        self.widget_22 = QtWidgets.QWidget(self.loginPage)
        self.widget_22.setGeometry(QtCore.QRect(0, 0, 1361, 858))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        self.widget_22.setFont(font)
        self.widget_22.setObjectName("widget_22")
        self.label_66 = QtWidgets.QLabel(self.widget_22)
        self.label_66.setGeometry(QtCore.QRect(660, 0, 701, 861))
        self.label_66.setText("")
        self.label_66.setPixmap(QtGui.QPixmap("../Icones/backgroundLogin.png"))
        self.label_66.setScaledContents(True)
        self.label_66.setObjectName("label_66")
        self.label_72 = QtWidgets.QLabel(self.widget_22)
        self.label_72.setGeometry(QtCore.QRect(138, 68, 216, 144))
        self.label_72.setText("")
        self.label_72.setPixmap(QtGui.QPixmap("../Icones/jabil.png"))
        self.label_72.setObjectName("label_72")
        self.label_73 = QtWidgets.QLabel(self.widget_22)
        self.label_73.setGeometry(QtCore.QRect(350, 120, 3, 40))
        self.label_73.setStyleSheet("background-color: rgb(0, 255, 127);")
        self.label_73.setText("")
        self.label_73.setObjectName("label_73")
        self.label_74 = QtWidgets.QLabel(self.widget_22)
        self.label_74.setGeometry(QtCore.QRect(360, 120, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_74.setFont(font)
        self.label_74.setStyleSheet("color: rgb(0, 82, 136);")
        self.label_74.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_74.setObjectName("label_74")
        self.label_75 = QtWidgets.QLabel(self.widget_22)
        self.label_75.setGeometry(QtCore.QRect(134, 225, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_75.setFont(font)
        self.label_75.setStyleSheet("color: rgb(0, 82, 136);")
        self.label_75.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_75.setObjectName("label_75")
        self.label_76 = QtWidgets.QLabel(self.widget_22)
        self.label_76.setGeometry(QtCore.QRect(134, 307, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_76.setFont(font)
        self.label_76.setStyleSheet("color: rgb(0, 82, 136);")
        self.label_76.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_76.setObjectName("label_76")
        self.widget_23 = QtWidgets.QWidget(self.widget_22)
        self.widget_23.setGeometry(QtCore.QRect(134, 342, 341, 41))
        self.widget_23.setStyleSheet("border-bottom:1px solid rgb(224, 224, 224);")
        self.widget_23.setObjectName("widget_23")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_23)
        self.horizontalLayout_6.setContentsMargins(6, 0, 0, 4)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.controleLogin = QtWidgets.QLineEdit(self.widget_23)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controleLogin.sizePolicy().hasHeightForWidth())
        self.controleLogin.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(11)
        self.controleLogin.setFont(font)
        self.controleLogin.setStyleSheet("border:None;")
        self.controleLogin.setObjectName("controleLogin")
        self.horizontalLayout_2.addWidget(self.controleLogin)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_2)
        self.label_83 = QtWidgets.QLabel(self.widget_22)
        self.label_83.setGeometry(QtCore.QRect(130, 396, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_83.setFont(font)
        self.label_83.setStyleSheet("color: rgb(0, 82, 136);")
        self.label_83.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_83.setObjectName("label_83")
        self.widget_24 = QtWidgets.QWidget(self.widget_22)
        self.widget_24.setGeometry(QtCore.QRect(130, 437, 341, 41))
        self.widget_24.setStyleSheet("border-bottom:1px solid rgb(224, 224, 224);")
        self.widget_24.setObjectName("widget_24")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_24)
        self.horizontalLayout_9.setContentsMargins(6, 0, 0, 4)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.controleSenha = QtWidgets.QLineEdit(self.widget_24)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controleSenha.sizePolicy().hasHeightForWidth())
        self.controleSenha.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(11)
        self.controleSenha.setFont(font)
        self.controleSenha.setStyleSheet("border:None;")
        self.controleSenha.setObjectName("controleSenha")
        self.horizontalLayout_10.addWidget(self.controleSenha)
        self.ocultarIcone = QtWidgets.QPushButton(self.widget_24)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ocultarIcone.sizePolicy().hasHeightForWidth())
        self.ocultarIcone.setSizePolicy(sizePolicy)
        self.ocultarIcone.setStyleSheet("border:None;")
        self.ocultarIcone.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../Icones/icon-view.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ocultarIcone.setIcon(icon7)
        self.ocultarIcone.setIconSize(QtCore.QSize(25, 25))
        self.ocultarIcone.setObjectName("ocultarIcone")
        self.horizontalLayout_10.addWidget(self.ocultarIcone)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_10)
        self.entrarLogin = QtWidgets.QPushButton(self.widget_22)
        self.entrarLogin.setGeometry(QtCore.QRect(134, 560, 341, 48))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(14)
        self.entrarLogin.setFont(font)
        self.entrarLogin.setStyleSheet("QPushButton{\n"
                                       "border-radius:10px;\n"
                                       "background-color: rgb(0, 82, 136);\n"
                                       "color:white;\n"
                                       "}\n"
                                       "QPushButton:hover{\n"
                                       "background-color:rgb(1, 110, 181)\n"
                                       "}")
        self.entrarLogin.setObjectName("entrarLogin")
        self.label_85 = QtWidgets.QLabel(self.widget_22)
        self.label_85.setGeometry(QtCore.QRect(350, 507, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(10)
        self.label_85.setFont(font)
        self.label_85.setStyleSheet("color: rgb(84, 94, 107);")
        self.label_85.setObjectName("label_85")
        self.erroLogin = QtWidgets.QLabel(self.widget_22)
        self.erroLogin.setGeometry(QtCore.QRect(130, 480, 341, 21))
        font = QtGui.QFont()
        font.setFamily("Lato")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.erroLogin.setFont(font)
        self.erroLogin.setStyleSheet("color: rgb(255, 0, 0);")
        self.erroLogin.setText("")
        self.erroLogin.setObjectName("erroLogin")
        self.stackedWidget_2.addWidget(self.loginPage)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget_2.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
            self.label_17.setText(_translate("MainWindow", "Desenvolvido por"))
            self.label_19.setText(_translate("MainWindow", "All Rights Reserved@2022"))
            self.historicoBotao.setText(_translate("MainWindow", "LOG"))
            self.usuarioBotao.setText(_translate("MainWindow", "LOCAL"))
            self.modeloBotao.setText(_translate("MainWindow", "SERVIDOR"))
            self.label_24.setText(_translate("MainWindow", "TESTE COMERCIAL"))
            self.Titulo_1.setText(_translate("MainWindow", "LOG"))
            self.label_6.setText(_translate("MainWindow", "SN:"))
            self.label_9.setText(_translate("MainWindow", "CÓDIGO"))
            self.label.setText(_translate("MainWindow", "MODELO A"))
            self.statusGeral.setText(_translate("MainWindow", "AGUARDANDO"))
            self.Titulo_2.setText(_translate("MainWindow", "FASE"))
            self.label_35.setText(_translate("MainWindow", "Teste Atual"))
            self.Titulo_3.setText(_translate("MainWindow", "FTP Status"))
            item = self.tableWidget.verticalHeaderItem(0)
            item.setText(_translate("MainWindow", "New Row"))
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Modelo"))
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Número Serial"))
            item = self.tableWidget.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Hora"))
            item = self.tableWidget.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "LOG"))
            item = self.tableWidget.horizontalHeaderItem(4)
            item.setText(_translate("MainWindow", "FASE"))
            item = self.tableWidget.horizontalHeaderItem(5)
            item.setText(_translate("MainWindow", "FTP"))
            self.acionaFiltro.setText(_translate("MainWindow", "FILTRO"))
            self.label_21.setText(_translate("MainWindow", "ENVIAR LOG"))
            self.label_36.setText(_translate("MainWindow", "Filtro"))
            self.historicoModeloCombo.setCurrentText(_translate("MainWindow", "TODOS"))
            self.historicoModeloCombo.setItemText(0, _translate("MainWindow", "TODOS"))
            self.label_22.setText(_translate("MainWindow", "Modelo"))
            self.label_23.setText(_translate("MainWindow", "Status Fase"))
            self.statusCombBox.setCurrentText(_translate("MainWindow", "TODOS"))
            self.statusCombBox.setItemText(0, _translate("MainWindow", "TODOS"))
            self.statusCombBox.setItemText(1, _translate("MainWindow", "OK"))
            self.statusCombBox.setItemText(2, _translate("MainWindow", "NG"))
            self.label_26.setText(_translate("MainWindow", "Início"))
            self.label_31.setText(_translate("MainWindow", "Fim"))
            self.limpaTela.setText(_translate("MainWindow", "CANCELAR"))
            self.buscarButton.setText(_translate("MainWindow", "CONFIRMAR"))
            self.toggleHIPOT_2.setText(_translate("MainWindow", "CheckBox"))
            self.label_37.setText(_translate("MainWindow", "Histórico"))
            self.UsuarioMenuNome.setText(_translate("MainWindow", "Nome"))
            self.usuarioMudaBotao.setText(_translate("MainWindow", "Dados de Cadastro"))
            self.LogoutBotao.setText(_translate("MainWindow", "Sair"))
            self.UsuarioNome.setText(_translate("MainWindow", "Nome"))
            self.tituloPopUp.setText(_translate("MainWindow", "USUÁRIO BLOQUEADO"))
            self.descricaoPopUp.setText(
                _translate("MainWindow", "Bloqueio por falha contínua em teste, contate o administrador."))
            self.botaoPopUp.setText(_translate("MainWindow", "OK"))
            self.label_74.setText(_translate("MainWindow", "TESTE COMERCIAL"))
            self.label_75.setText(_translate("MainWindow", "Login"))
            self.label_76.setText(_translate("MainWindow", "Controle"))
            self.controleLogin.setPlaceholderText(_translate("MainWindow", "Controle"))
            self.label_83.setText(_translate("MainWindow", "Senha"))
            self.controleSenha.setPlaceholderText(_translate("MainWindow", "Senha"))
            self.entrarLogin.setText(_translate("MainWindow", "ENTRAR"))
            self.label_85.setText(_translate("MainWindow", "Esqueceu sua senha?"))

    def inicializadores(self):

        self.notificacoes=Notificacoes()
        self.contadorErro=datetime.now()

        self.usuarioBotao.setText("Servidor Local")
        self.modeloBotao.setText("Servidor MES")
        servidor = ""

        with open("servidor.txt", "r") as file:
            for i in file:
                servidor = i

        try:

            self.modelos = BancoDeDados(servidor, "bancofv", "P&D", "@Jabil.2022")
            self.notificacoes.erroBanco = False

        except Exception as e:

            self.notificacoes.erroBanco=True
            print("SEM BANCO DE DADOS:", e)


        self.getBotaoEdicao()
        self.getModelos()

        self.EstilosStatus()

        self.historicoModeloCombo.setEditable(True)

        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.Callbacks)

        self.buscarButton.clicked.connect(self.getDateInterval)

        self.caminhos["objetos"]=[self.historicoBotao,self.modeloBotao,self.usuarioBotao]

        self.controleSenha.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.ocultarIcone.setIcon(QtGui.QIcon('../Icones/senha_off.svg'))
        self.ocultarIcone.clicked.connect(self.mudaLoginIcon)

        self.dataInicio.setDate(datetime.now())
        self.dataFim.setDate(datetime.now())

        self.entrarLogin.clicked.connect(partial(self.MudaMainPage,0))
        self.botaoPopUp.clicked.connect(partial(self.MudaMainPage, 1))
        self.LogoutBotao.clicked.connect(partial(self.MudaMainPage, 1))

        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(1)

        self.UsuarioNome.clicked.connect(self.usuarioMenuClicked)

        self.setToggle()
        self.toggleHIPOT_2.toggled.connect(self.changeToggle)


        self.usuarioBotao.clicked.connect(partial(self.dialogPath,"local"))
        self.modeloBotao.clicked.connect(partial(self.dialogPath,"server"))
        self.historicoBotao.clicked.connect(partial(self.dialogPath,"log"))

        self.acionaFiltro.clicked.connect(self.acionaFiltroJanela)
        self.limpaTela.clicked.connect(self.acionaFiltroJanela)



        self.timer.start(1)

    def mudaLoginIcon(self):

        if self.controleSenha.echoMode()==QtWidgets.QLineEdit.EchoMode.Password:
            self.controleSenha.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
            self.ocultarIcone.setIcon(QtGui.QIcon('../Icones/senha_on.svg'))

        else:
            self.controleSenha.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
            self.ocultarIcone.setIcon(QtGui.QIcon('../Icones/senha_off.svg'))

    def dialogPath(self,tipo):
        self.notificacoes.checkNetwork("https://www.google.com/")
        if not self.notificacoes.erroConexao and not self.notificacoes.erroBanco:
            dialog = QtWidgets.QFileDialog()
            foo_dir = dialog.getExistingDirectory()
            print(foo_dir)

            if tipo=="log" and foo_dir:
                foo_dir = foo_dir.replace("//", "/")
                foo_dir=foo_dir.replace("/","\\\\")
                try:
                    self.modelos.writeQuery("update dbo.caminho set logCaminho='"+foo_dir+"'")
                except:
                    self.notificacoes.erroBanco=True
                print(foo_dir)
            if tipo=="server" and foo_dir:
                foo_dir = foo_dir.replace("//", "/")
                foo_dir=foo_dir.replace("/","\\\\")
                try:
                    self.modelos.writeQuery("update dbo.caminho set serverCaminho='"+foo_dir+"'")
                except:
                    self.notificacoes.erroBanco=True
                print(foo_dir)
            if tipo=="local" and foo_dir:
                foo_dir = foo_dir.replace("//", "/")
                foo_dir = foo_dir.replace("/", "\\\\")
                try:
                    self.modelos.writeQuery("update dbo.caminho set localCaminho='" + foo_dir + "'")
                except:
                    self.notificacoes.erroBanco=True
                print(foo_dir)

    def acionaFiltroJanela(self):

        if self.filtroJanela.width()==0:
            self.filtroJanela.setFixedWidth(561)
        else:
            self.filtroJanela.setFixedWidth(0)

    def usuarioMenuClicked(self):
        if self.loginWindow.width()==0:
            self.loginWindow.setFixedWidth(235)
        else:
            self.loginWindow.setFixedWidth(0)

    def getModelos(self,filtro=None):
        query = "select id,modelo from dbo.configuracoes"
        self.listaBotaoModelos = []
        ordem = [1,2,4,6,8]
        try:
            self.notificacoes.erroBanco=False
            q = self.modelos.readQuery(query)
        except Exception as e:
            print(e)
            q = []
            self.notificacoes.erroBanco=True
        print("Saida:",q)
        if filtro == None:

            for i in q:

                self.historicoModeloCombo.addItem(i[1])


    def EstilosStatus(self):

        self.statusTesteVisivel="color: rgb(84, 94, 107);background-color: rgb(224, 224, 224);\nborder-bottom-right-radius: 7px; \nborder-bottom-left-radius: 7px; \n"

        self.statusTesteNaoVisivel="color: rgb(230, 230, 230);background-color: rgb(224, 224, 224);\nborder-bottom-right-radius: 7px; \nborder-bottom-left-radius: 7px; \n"

        self.tituloVisivel="border-top-right-radius:7px;\nborder-top-left-radius:7px;\nbackground-color: rgb(255, 255, 255);\ncolor: rgb(0, 82, 136);"

        self.tituloNVisivel="border-top-right-radius:7px;\nborder-top-left-radius:7px;\nbackground-color: rgb(255, 255, 255);\ncolor: rgb(230, 230, 230);"

        self.estiloStatusOK="color: white;background-color: rgb(32, 195, 58);\nborder-bottom-right-radius: 7px; \nborder-bottom-left-radius: 7px; \n"

        self.estiloStatusNG="color: white;background-color: rgb(232, 6, 29);\nborder-bottom-right-radius: 7px; \nborder-bottom-left-radius: 7px; \n"

        self.estiloStatusInTeste="color: rgb(84, 94, 107);background-color: rgb(255, 201, 76);\nborder-bottom-right-radius: 7px; \nborder-bottom-left-radius: 7px; \n"

        self.estiloStatusGeralAguardando="background-color: rgb(255, 255, 255); border-radius: 7px;\n color: rgb(84, 94, 107);"

        self.estiloStatusGeralInTeste="background-color: rgb(255, 255, 255); border-radius: 7px;\n color: rgb(255, 201, 76);"

        self.estiloStatusGeralOK = "background-color: rgb(32, 195, 58); border-radius: 7px;\n color: white;"

        self.estiloStatusGeralNG = "background-color: rgb(232, 6, 29); border-radius: 7px;\n color: white;"

    def MudaMainPage(self,a):
        self.notificacoes.checkNetwork("https://www.google.com/")
        print(self.notificacoes.erroConexao)
        if a == 0:
            try:
                q=self.modelos.readQuery("select * from dbo.usuarios where controle='"+self.controleLogin.text()+"' and senha ='"+
                                         self.controleSenha.text()+"'")
                self.notificacoes.erroBanco = False
            except:
                self.notificacoes.erroBanco=True
            print("query:"+"select * from dbo.usuarios where controle='"+self.controleLogin.text()+"' and senha ='"+
                                   self.controleSenha.text()+"'")
            try:

                self.usuario=q[0][1]
                self.notificacoes.erroLogin=False
                #self.usuarioLogado.setText(self.usuario)
                self.UsuarioNome.setText(self.usuario)
                self.UsuarioMenuNome.setText(self.usuario)
                if len(q) == 1:
                    self.stackedWidget_2.setCurrentIndex(a)
                    self.stackedWidget.setCurrentIndex(0)
                self.controleLogin.setText("")
                self.controleSenha.setText("")
            except:
                self.notificacoes.erroLogin=True
                self.controleLogin.setText("")
                self.controleSenha.setText("")
                print("Senha incorreta!!")

            if self.loginWindow.width() != 0:
                self.usuarioMenuClicked()

        if a==1:
            self.stackedWidget_2.setCurrentIndex(a)

    def getBotaoEdicao(self):

        botaoTabela=QtWidgets.QPushButton()
        botaoTabela.setIcon(QtGui.QIcon("../Icones/editar_Icon.png"))
        botaoTabela.setIconSize(QtCore.QSize(30,30))
        botaoTabela.setStyleSheet("background-color:white;border:None;width:30;height:30;")
        return botaoTabela

    def menuChange(self,tipo):

        if tipo=="status":
            self.stackedWidget.setCurrentIndex(0)
            self.changeColor(self.caminhos["local"][0])
            self.hipotBotao.setIcon(QtGui.QIcon(self.caminhos["local"][4]))

        elif tipo=="historico":
            self.stackedWidget.setCurrentIndex(1)
            self.changeColor(self.caminhos["local"][1])
            self.hipotBotao.setIcon(QtGui.QIcon(self.caminhos["local"][4]))

        elif tipo =="modelo":
            self.stackedWidget.setCurrentIndex(3)
            self.changeColor(self.caminhos["local"][2])
            self.hipotBotao.setIcon(QtGui.QIcon(self.caminhos["local"][4]))

        elif tipo=="hipot":
            self.stackedWidget.setCurrentIndex(2)
            self.changeColor(self.caminhos["local"][4])
            self.hipotBotao.setIcon(QtGui.QIcon("../Icones/hipot_icon_off.svg"))
        elif tipo=="usuario":
            self.stackedWidget.setCurrentIndex(4)
            self.changeColor(self.caminhos["local"][3])
            self.hipotBotao.setIcon(QtGui.QIcon(self.caminhos["local"][4]))


        self.statusBotao.setIcon(QtGui.QIcon(self.caminhos["local"][0]))
        self.historicoBotao.setIcon(QtGui.QIcon(self.caminhos["local"][1]))
        self.modeloBotao.setIcon(QtGui.QIcon(self.caminhos["local"][2]))

        self.usuarioBotao.setIcon(QtGui.QIcon(self.caminhos["local"][3]))

    def Callbacks(self):

        self.timer.stop()
        #time.sleep(1)
        self.notificacoes.callbackNotificacao()
        if not self.notificacoes.erroConexao and not self.notificacoes.erroBanco:
            self.lista["status"] = [ui.statusTeste1, ui.statusTeste1_2, ui.statusTeste1_3]
            self.FiltroModelos()

            try:
                q=self.modelos.readQuery("SELECT TOP 1 * FROM dbo.Dados ORDER BY id DESC ;")
            except:
                self.notificacoes.erroBanco=True
            status="OK"
            #print(q)
            try:
                self.label_9.setText(q[0][4])
                if q[0][2]=="OK":
                    self.lista["status"][0].setText("APROVADO")
                    self.lista["status"][0].setStyleSheet(ui.estiloStatusOK)
                    self.label_4.setPixmap(QtGui.QPixmap("../Icones/AprovadoMaior.svg"))

                elif q[0][2]=="ABERTO":

                    self.lista["status"][0].setText("EM TESTE")
                    self.lista["status"][0].setStyleSheet(ui.estiloStatusInTeste)
                    self.label_4.setPixmap(QtGui.QPixmap("../Icones/Aguardando.png"))
                    if status!="NG":
                        status="WAIT"

                else:
                    self.lista["status"][0].setText("REPROVADO")
                    self.lista["status"][0].setStyleSheet(ui.estiloStatusNG)
                    self.label_4.setPixmap(QtGui.QPixmap("../Icones/ReprovadoMaior.svg"))
                    status="NG"

                if q[0][5]=="ABERTO":

                    self.lista["status"][1].setText("EM TESTE")
                    self.lista["status"][1].setStyleSheet(ui.estiloStatusInTeste)
                    self.label_5.setPixmap(QtGui.QPixmap("../Icones/Aguardando.png"))
                    if status!="NG":
                        status="WAIT"

                elif q[0][5]=="OK":
                    self.lista["status"][1].setText("APROVADO")
                    self.lista["status"][1].setStyleSheet(ui.estiloStatusOK)
                    self.label_5.setPixmap(QtGui.QPixmap("../Icones/AprovadoMaior.svg"))

                else:
                    self.lista["status"][1].setText("REPROVADO")
                    self.lista["status"][1].setStyleSheet(ui.estiloStatusNG)
                    self.label_5.setPixmap(QtGui.QPixmap("../Icones/ReprovadoMaior.svg"))
                    status="NG"

                if q[0][8]=="ABERTO":
                    self.lista["status"][2].setText("AGUARDANDO")
                    self.lista["status"][2].setStyleSheet(ui.estiloStatusInTeste)
                    self.label_8.setPixmap(QtGui.QPixmap("../Icones/Aguardando.png"))
                    if status!="NG":
                        status="WAIT"

                elif q[0][8]=="OK":
                    self.lista["status"][2].setText("ENVIADO")
                    self.lista["status"][2].setStyleSheet(ui.estiloStatusOK)
                    self.label_8.setPixmap(QtGui.QPixmap("../Icones/AprovadoMaior.svg"))

                else:
                    self.lista["status"][2].setText("NÃO ENVIADO")
                    self.lista["status"][2].setStyleSheet(ui.estiloStatusNG)
                    self.label_8.setPixmap(QtGui.QPixmap("../Icones/ReprovadoMaior.svg"))
                    status="NG"

                if status=="OK":
                    ui.statusGeral.setText("APROVADO")
                    ui.statusGeral.setStyleSheet(ui.estiloStatusGeralOK)
                elif status=="NG":
                    ui.statusGeral.setText("REPROVADO")
                    ui.statusGeral.setStyleSheet(ui.estiloStatusGeralNG)
                else:
                    ui.statusGeral.setStyleSheet(ui.estiloStatusGeralInTeste)
                    ui.statusGeral.setText("EM TESTE")
            except Exception as e:
                self.notificacoes.erroBanco=True
                print("SEM DADOS",e)
        if self.notificacoes.erroBanco and (datetime.now()-self.contadorErro).total_seconds()>=10:
            servidor = ""
            with open("servidor.txt", "r") as file:
                for i in file:
                    servidor = i
            self.modelos.host=servidor

            if not self.ErroThread.isRunning() :
                print("Entrou thread")
                self.ErroThread.start()
            self.contadorErro=datetime.now()

        print("Running:", not self.ErroThread.isRunning())
        print("Finished:", not self.ErroThread.isFinished())
        self.timer.start(100)

    def FiltroModelos(self):

        if self.historicoModeloCombo.itemChecked(0) != self.totalChecked:

            self.historicoModeloCombo.TodosChecked()
            self.totalChecked = self.historicoModeloCombo.itemChecked(0)

            if self.totalChecked:
                self.historicoModeloCombo.setEditText("TODOS")
                self.filtroModelos="TODOS"
            else:
                self.historicoModeloCombo.setEditText("NENHUM")
                self.filtroModelos="NENHUM"
        else:

            txt=""
            selecionado=self.historicoModeloCombo.CustomEdit()

            if len(selecionado)==0:
                if self.historicoModeloCombo.itemChecked(0):
                    self.historicoModeloCombo.handle_item_pressed(0)
                    self.totalChecked = False
                txt="NENHUM"

            elif len(selecionado)<self.historicoModeloCombo.count():
                if self.historicoModeloCombo.itemChecked(0):
                    self.historicoModeloCombo.handle_item_pressed(0)
                    self.totalChecked = False
                for i in selecionado:
                    if i != 0:
                        txt=txt+i+","
                txt=txt[:-1]
            elif len(selecionado)==self.historicoModeloCombo.count():
                if self.historicoModeloCombo.itemChecked(0)==False:
                    self.historicoModeloCombo.handle_item_pressed(0)
                    self.totalChecked = True
                txt="TODOS"
            self.filtroModelos=txt
            self.historicoModeloCombo.setEditText(txt)

    def getDateInterval(self):
        ordem=[9,4,1,2,5,8]


        ini=str(self.dataInicio.date().year())+"/"+str(self.dataInicio.date().month())+"/"+str(self.dataInicio.date().day())
        fim=str(self.dataFim.date().year())+"/"+str(self.dataFim.date().month())+"/"+str(self.dataFim.date().day())


        query="SELECT * FROM dbo.Dados WHERE hora BETWEEN '{inicio}' AND '{fim} 23:59:59' ".format(inicio=ini,fim=fim)

        if self.filtroModelos!="TODOS" and self.filtroModelos!="NENHUM":
            print(self.filtroModelos)
            modelos=self.filtroModelos.split(",")

            if len(modelos)==1:
                query= query+" AND modelo ='"+modelos[0]+"'"
            else:
                query=query+" AND modelo ='"+modelos[0]+"'"
                for k in range(1,len(modelos)):
                    query=query+ " OR modelo ='"+modelos[k]+"'"
        if self.statusCombBox.currentText()!="TODOS":
            query =query+ " AND resultadoFase ='" + self.statusCombBox.currentText() + "'"

        print(query)

        self.tableWidget.setRowCount(0)
        try:
            q=self.modelos.readQuery(query)

        except:
            q=[]
            self.notificacoes.erroBanco=True
        for i in q:
            print(i)
            currentRowCount = self.tableWidget.rowCount()  # necessary even when there are no rows in the table
            self.tableWidget.insertRow(currentRowCount)  # insert new row
            c=0
            for j in ordem:
                item=QtWidgets.QTableWidgetItem(str(i[j]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableWidget.setItem(currentRowCount, c, item)
                c+=1
            '''
            self.tableWidget.setItem(currentRowCount - 1, 1, QtWidgets.QTableWidgetItem(str(i[2])))
            self.tableWidget.setItem(currentRowCount - 1, 2, QtWidgets.QTableWidgetItem(str(i[6])))
            self.tableWidget.setItem(currentRowCount - 1, 3, QtWidgets.QTableWidgetItem(str(i[7])))
            self.tableWidget.setItem(currentRowCount - 1, 4, QtWidgets.QTableWidgetItem(str(i[3])))
            self.tableWidget.setItem(currentRowCount - 1, 5, QtWidgets.QTableWidgetItem(str(i[4])))
            self.tableWidget.setItem(currentRowCount - 1, 6, QtWidgets.QTableWidgetItem(str(i[5])))
            #self.tableWidget.insertRow(currentRowCount, 0, QtWidgets.QTableWidgetItem("Some text"))
            print(currentRowCount)
            '''
            print(currentRowCount)
        header=self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.acionaFiltroJanela()

    def changeColor(self,caminho):

        st=""

        for i in range (len(self.caminhos["nomes"])):

            if self.caminhos["local"][i]!=caminho:

                atualiza=False
                self.caminhos["objetos"][i].setStyleSheet(self.naoSelecionadoStyle)
                st=""
                if self.caminhos["nomes"][i]!="Hipot":
                    with open(self.caminhos["local"][i], "r") as file:
                        for line in file:
                            if line.find("#fff"):
                                atualiza=True
                                line = line.replace("#fff", "#005288")
                            st = st + line
                    if atualiza:
                        with open(self.caminhos["local"][i], "w") as file:
                            file.write(st)

            else:
                st=""
                if self.caminhos["nomes"][i] != "Hipot":
                    with open(caminho, "r") as file:
                        for line in file:
                            if line.find("#005288"):
                                line = line.replace("#005288", "#fff")
                            st = st + line
                    with open(caminho, "w") as file:
                        file.write(st)

                self.caminhos["objetos"][i].setStyleSheet(self.selecionadoStyle)

    def atualizaResultadoDiario(self):

        ini = str(self.dataInicio.date().year()) + "/" + str(self.dataInicio.date().month()) + "/" + str(
            self.dataInicio.date().day())
        fim = str(self.dataFim.date().year()) + "/" + str(self.dataFim.date().month()) + "/" + str(
            self.dataFim.date().day())
        query = "SELECT * FROM dbo.valorhipot WHERE DATA BETWEEN '{inicio}' AND '{fim} 23:59:59' ".format(inicio=ini,
                                                                                                      fim=fim)
        res=self.modelos.readQuery(query)
        countOk=0
        countNG=0
        for i in res:
            if i[7]!="OK":
                countNG+=1
            else:
                countOk+=1

        self.aprovadosQuantidade.setText(str(countOk))
        self.reprovadosQuantidade.setText(str(countNG))

    def changeToggle(self,state):

        if state:
            query="update dbo.caminho set modoCaminho='Local'"
        else:
            query = "update dbo.caminho set modoCaminho='Log'"

        try:
            self.modelos.writeQuery(query)
        except:
            self.notificacoes.erroBanco=True

    def setToggle(self):

        try:
            q=self.modelos.readQuery("select * from dbo.caminho")
            if q[0][4]=="Local":
                self.toggleHIPOT_2.setChecked(True)
            else:
                self.toggleHIPOT_2.setChecked(False)

        except Exception as e:
            q=[]
            self.notificacoes.erroBanco=True
            print(e)

    def startTestSimulated(self):

        self.chamaTeste.stop()
        self.Testando=True
        self.TestandoIndex=0

        self.Evento.update_data.connect(self.setTesteIndex)
        self.Evento.start()
        self.atualizaResultadoDiario()

        self.Testando = False

    def setTesteIndex(self,a):
        self.TestandoIndex=a
        print(a)




import icones_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.inicializadores()
    MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    MainWindow.show()
    sys.exit(app.exec_())
