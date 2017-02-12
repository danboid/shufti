#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# shufti - A WIP, PyQt5 persistent image viewer
#
# By Dan MacDonald
#
# 2017
#
# Usage:
#
# python shufti.py path/to/image

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap

class Shufti(QMainWindow):
    
    def __init__(self):
        super().__init__()
        try:
            self.file = open(sys.argv[1], 'r')
        except IOError:
            print('There was an error opening the file')
            sys.exit(1)
        
        if (sys.argv[1]).lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.pbm', '.pgm', '.ppm', '.xbm', '.xpm')):
            self.initUI()
            self.setWindowTitle("shufti")
            self.resize(999, 999)
        else:
            print("Unsupported file format")
            sys.exit(1)
        
    def initUI(self):               
        
        self.scene = QGraphicsScene()
        self.scene.addPixmap(QPixmap(sys.argv[1]))
        self.view = QGraphicsView(self.scene, self)
        self.view.resize(999, 999)
        self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    shufti = Shufti()
    sys.exit(app.exec_())
