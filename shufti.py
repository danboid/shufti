#!/usr/bin/python3
# -*- coding: utf-8 -*-
# shufti - A WIP, PyQt5 persistent image viewer for Gahnooh slaash Leenoox.

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap

class Shufti(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):               
        
        self.scene = QGraphicsScene()
        self.scene.addPixmap(QPixmap("/home/dan/pic.jpg"))
        self.view = QGraphicsView(self.scene, self)
        self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    shufti = Shufti()
    sys.exit(app.exec_())
