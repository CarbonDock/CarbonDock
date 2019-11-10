from time import time
from socket import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QGraphicsColorizeEffect, QHBoxLayout
from PyQt5.QtGui import QColor, QFontDatabase, QIcon, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QTimer, Qt
from functools import partial
from threading import Thread
from p2pl import Node
import os

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
        self.window.setGeometry(50,50,600,500)
        self.window.setStyleSheet(open(os.path.join(os.path.abspath(os.curdir),'client','style.qss'),'r').read())
        self.layout = QVBoxLayout()
        
        self.titlebar = QWidget()
        self.titlebar.setStyleSheet('background-color: rgba(0,0,0,0);border-image: null;')
        self.titlelay = QHBoxLayout()

        label = QLabel()
        pixmap = QPixmap('icon.png').scaled(128,128)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        self.titlelay.addWidget(label)

        self.title = QLabel('CarbonDock')
        self.title.setStyleSheet('font: 20pt;')
        self.title.setAlignment(Qt.AlignCenter)
        self.titlelay.addWidget(self.title)
        self.titlebar.setLayout(self.titlelay)
        self.layout.addWidget(self.titlebar)

        self.modStats = QWidget()
        self.modStats.setStyleSheet('background-color: rgba(0,0,0,0);border-image: null;')
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
            statLab = QLabel(i['stat'])
            statLab.setStyleSheet('font: 15pt;')
            statLab.setAlignment(Qt.AlignCenter)
            mlayout.addWidget(statLab)
            nameLab = QLabel(i['name'])
            nameLab.setStyleSheet('font: 10pt;color:rgb(128,128,128);')
            nameLab.setAlignment(Qt.AlignCenter)
            mlayout.addWidget(nameLab)
            main.setLayout(mlayout)
            self.modLayout.addWidget(main)
        
    def refresh(self):
        while True:
            discovered = []
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

