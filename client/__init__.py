from time import time
from socket import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QGraphicsColorizeEffect
from PyQt5.QtGui import QColor, QFontDatabase, QIcon
from PyQt5.QtCore import QTimer
from functools import partial
from threading import Thread
<<<<<<< HEAD
from p2pl import Node
=======
from p2p import Node
import os
>>>>>>> 4d4d591740e2fd92955265a6921e921aefc853a2

"""
Main UI program:
includes detection for the CO2 Monitor to the person's selected device
"""
class UI:
    def __init__(self):
        self.node = Node(8888,6768,'Carbon-Client',protocol='CarbonDock')
        self.rt = Thread(target=self.refresh,name='Refresher')
        self.rt.start()
        self.app = QApplication(['CarbonDock'])
        self.app.setWindowIcon(QIcon('icon.png'))

        QFontDatabase.addApplicationFont('main.ttf')

        self.window = QWidget()
        self.window.setWindowTitle('CarbonDock')
        self.window.setGeometry(50,50,300,300)
        self.window.setStyleSheet(open(os.path.join(os.path.abspath(os.curdir),'client','style.qss'),'r').read())
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel('CarbonDock'))
        self.modStats = QWidget()
        self.modLayout = QVBoxLayout()
        self.modStats.setLayout(self.modLayout)
        self.stats = []
        self.layout.addWidget(self.modStats)
        self.window.setLayout(self.layout)
        self.window.show()
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.check_refresh)
        self.timer.start()
        self.app.exec_()

    def runButtonFunc(self,func):
        func()

    def check_refresh(self):
        for i in reversed(range(self.modLayout.count())): 
            self.modLayout.itemAt(i).widget().setParent(None)
        for i in self.stats:
            main = QWidget()
            main.setStyleSheet('background-color: rgb('+','.join(map(str,i['color']))+')')
            mlayout = QVBoxLayout()
            mlayout.addWidget(QLabel(i['name'] + ': ' + i['stat']))
            main.setLayout(mlayout)
            self.modLayout.addWidget(main)
        
    def refresh(self):
        while True:
            discovered = []
            print(self.node.targets)
            for n in self.node.targets.keys():
                discovered.append([n,self.node.targets[n]])
            stats = []
            #for i in discovered:
            stat = self.node.request('192.168.137.156','status')
            cf = stat['danger_coeff']
            if cf < 0:
                cf = 0
            if cf > 1:
                cf = 1
            col = (cf*255,((1-cf)*255)/1.2,0)
            stats.append({'color':col,'stat':stat['danger'],'name':'CarbonDock-192.168.137.156'})
                
            self.stats = stats

UI()

