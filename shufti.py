#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# shufti - A WIP, PyQt5 persistent image viewer for Gahnooh slaash Leenoox.
#
# By Dan MacDonald
#
# 2017

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap

class Shufti(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("shufti")
        self.resize(999, 999)
        
        
    def initUI(self):               
        
        self.scene = QGraphicsScene()
        self.scene.addPixmap(QPixmap("/home/dan/pic.jpg"))
        self.view = QGraphicsView(self.scene, self)
        self.view.resize(999, 999)
        self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    shufti = Shufti()
    sys.exit(app.exec_())
