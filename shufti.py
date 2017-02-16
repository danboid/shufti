#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
shufti - A persistent, PyQt5-based image viewer

By Dan MacDonald, 2017

Usage:

python shufti.py path/to/image
'''

import os, sys
from PyQt5 import QtCore, QtSql
from PyQt5.QtGui import QPixmap
from os.path import expanduser, dirname
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView

class ShuftiWindow(QMainWindow):
    
    def resizeEvent(self,resizeEvent):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        self.view.resize(width + 2, height + 2)

class Shufti(ShuftiWindow):
    
    def __init__(self):
        super().__init__()
        try:
            self.file = open(sys.argv[1], 'r')
        except IOError:
            print('There was an error opening the file')
            sys.exit(1)
        
        if (sys.argv[1]).lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.pbm', '.pgm', '.ppm', '.xbm', '.xpm')):
            self.dbfile = expanduser("~/.config/shufti/shufti.db")
            self.dbdir = os.path.dirname(self.dbfile)
            if not os.path.exists(self.dbdir):
                self.createDB()
            self.query = QtSql.QSqlQuery()
            self.db.setDatabaseName(self.dbfile)
            self.db.open()
            self.zoom = 1
            self.initUI()
            self.setWindowTitle("shufti")
            self.resize(self.img.size())
        else:
            print("Unsupported file format")
            sys.exit(1)
        
    def initUI(self):               
        
        self.img = QPixmap(sys.argv[1])
        self.scene = QGraphicsScene()
        self.scene.addPixmap(self.img)
        self.view = QGraphicsView(self.scene, self)
        self.view.resize(self.img.width() + 2, self.img.height() + 2)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.show()
        
    def toggleFullscreen(self):
        
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    def keyPressEvent(self, event):
        
        if event.key() == QtCore.Qt.Key_F11 or event.key() == QtCore.Qt.Key_F:
            self.toggleFullscreen()
        elif event.key() == QtCore.Qt.Key_Equal:
            self.zoom *= 1.05
            self.view.scale(self.zoom, self.zoom)
        elif event.key() == QtCore.Qt.Key_Minus:
            self.zoom = 1 - (self.zoom / 20)
            self.view.scale(self.zoom, self.zoom)
            
    def createDB(self):
        
        os.makedirs(self.dbdir)
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.dbfile)
        self.query = QtSql.QSqlQuery()
        self.db.open()
        self.query.exec_("create table shuftery(filename text primary key, "
        "zoom real, winposx int, winposy int, winsizex int, winsizey int, "
        "hscroll int, vscroll int)")
        self.query.exec_("insert into shuftery values('/home/dan/file.png', 1.111, 456, 546, 665, 556, 5636, 333)")
        return True
        

'''
I'd like to have mousewheel zoom, but I've been unable to stop Qt clashing with the
QGraphicsView vertical scrollbars that appear when you zoom into an image.

    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y()/2880
        self.view.scale(self.zoom, self.zoom)
'''
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    shufti = Shufti()
    sys.exit(app.exec_())
