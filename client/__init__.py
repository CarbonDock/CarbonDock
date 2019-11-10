from __future__ import print_function	# For Py2/3 compatibility
from time import time
from socket import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QGraphicsColorizeEffect
from PyQt5.QtGui import QColor, QFontDatabase
from PyQt5.QtCore import QTimer
from functools import partial
from threading import Thread
from p2p import Node

"""
Main UI program:
includes detection for the CO2 Monitor to the person's selected device
"""
class UI:
    def __init__(self):
        self.node = Node(8888,6768,'Carbon-Client',protocol='CarbonDock')
        self.rt = Thread(target=self.refresh,name='Refresher')
        self.rt.start()
        self.app = QApplication([])

        QFontDatabase.addApplicationFont('main.ttf')

        self.window = QWidget()
        with open('style.qss','r') as stylesheet:
            self.window.setStyleSheet(stylesheet.read())
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
            for n in self.node.targets.keys():
                discovered.append([n,self.node.targets[n]])
            stats = []
            for i in discovered:
                stat = self.node.request(i[0],'status')
                cf = stat['danger_coeff']
                if cf < 0:
                    cf = 0
                if cf > 1:
                    cf = 1
                col = (cf*255,((1-cf)*255)/1.2,0)
                stats.append({'color':col,'stat':stat['danger'],'name':i[0]})
                
            self.stats = stats

UI()

