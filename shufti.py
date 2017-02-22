#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
shufti - A persistent, PyQt5-based image viewer

By Dan MacDonald, 2017

Usage:

shufti.py path/to/image

You may want to associate shufti with image files in your file manager rather than
use it from the terminal.
'''

import os, sys
from PyQt5 import QtCore, QtSql
from PyQt5.QtGui import QPixmap, QTransform
from os.path import expanduser, dirname
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView

class ShuftiView(QGraphicsView):
    
    def wheelEvent(self, event):
        
        moose = event.angleDelta().y()/120
        if moose > 0:
            shufti.zoomIn()
        elif moose < 0:
            shufti.zoomOut()

class ShuftiWindow(QMainWindow):
    
    def resizeEvent(self,resizeEvent):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        self.view.resize(width + 2, height + 2)
        
    def closeEvent(self, event):
        
        winsizex = self.geometry().width()
        winsizey = self.geometry().height()
        vscroll = self.view.verticalScrollBar().value()
        hscroll = self.view.horizontalScrollBar().value()
        winposx = self.pos().x()
        winposy = self.pos().y()
        if self.inshuft == 0:
            self.query.exec_("insert into shuftery values('" + str(self.key) + 
            "', " + str(self.zoom) + ", " + str(winposx) + ", " + str(winposy) + 
            ", " + str(winsizex) + ", " + str(winsizey) + ", " + str(hscroll) + 
            ", " + str(vscroll) + ", " + str(self.rotate) + ")")
            self.db.close()
        else:
            self.query.exec_("update shuftery set zoom=" + str(self.zoom) + 
            ", winposx=" + str(winposx) + ", winposy=" + str(winposy) + 
            ", winsizex=" + str(winsizex) + ", winsizey=" + str(winsizey) + 
            ", hscroll=" + str(hscroll) + ", vscroll=" + str(vscroll) + 
            ", rotate=" + str(self.rotate) + " where filename='" + str(self.key) + "'")
            self.db.close()

class Shufti(ShuftiWindow):
    
    def __init__(self):
        super().__init__()
        self.key = sys.argv[1]
        try:
            open(self.key, 'r')
        except IOError:
            print('There was an error opening the file')
            sys.exit(1)
        
        if self.key.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp',
         '.pbm', '.pgm', '.ppm', '.xbm', '.xpm')):
            # If inshuft = 0, the image is not in shufti's image database
            self.inshuft = 0
            self.rotval = 0
            self.rotvals = (0,-90,-180,-270)
            self.dbfile = expanduser("~/.config/shufti/shufti.db")
            self.dbdir = os.path.dirname(self.dbfile)
            if not os.path.exists(self.dbdir):
                self.createDB()
            self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(self.dbfile)
            self.db.open()
            self.query = QtSql.QSqlQuery()
            self.query.exec_("SELECT * FROM shuftery WHERE filename='" + str(self.key) + "'")
            # If the image is found in shufti.db, load the previous view settings
            while self.query.next() and self.inshuft == 0:
                self.zoom = self.query.value(1)
                self.winposx = self.query.value(2)
                self.winposy = self.query.value(3)
                self.winsizex = self.query.value(4)
                self.winsizey = self.query.value(5)
                self.hscroll = self.query.value(6)
                self.vscroll = self.query.value(7)
                self.rotate = self.query.value(8)
                self.inshuft = 1
            # Set common window attributes
            self.path, self.title = os.path.split(self.key)
            self.setWindowTitle(str(self.title) + " - shufti")
            self.img = QPixmap(self.key)
            self.scene = QGraphicsScene()
            self.scene.addPixmap(self.img)
            self.view = ShuftiView(self.scene, self)
            self.view.setDragMode(QGraphicsView.ScrollHandDrag)
            self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            # If we have no inshuftery, we use the defaults
            if self.inshuft == 0:
                self.newImage()
            else:
                self.oldImage()
        else:
            print("Unsupported file format")
            sys.exit(1)
        
    def newImage(self):               
        
        self.zoom = 1
        self.rotate = 0
        self.resize(self.img.size())
        self.view.resize(self.img.width() + 2, self.img.height() + 2)
        self.show()
        
    def oldImage(self):
        
        if self.rotate == -90:
            self.rotval = 1
        elif self.rotate == -180:
            self.rotval = 2
        elif self.rotate == -270:
            self.rotval = 3
        self.view.setTransform(QTransform().scale(self.zoom, self.zoom).rotate(self.rotate))
        self.show()
        self.setGeometry(self.winposx, self.winposy, self.winsizex, self.winsizey)
        self.view.verticalScrollBar().setValue(self.vscroll)
        self.view.horizontalScrollBar().setValue(self.hscroll)
        
    def toggleFullscreen(self):
        
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    def keyPressEvent(self, event):
        
        if event.key() == QtCore.Qt.Key_F11 or event.key() == QtCore.Qt.Key_F:
            self.toggleFullscreen()
        elif event.key() == QtCore.Qt.Key_Equal:
            self.zoomIn()
        elif event.key() == QtCore.Qt.Key_Minus:
            self.zoomOut()
        elif event.key() == QtCore.Qt.Key_1:
            self.zoom = 1
            self.view.setTransform(QTransform().scale(1, 1))
        elif event.key() == QtCore.Qt.Key_S:
            self.rotateImg(-1)
        elif event.key() == QtCore.Qt.Key_R:
            self.rotateImg(1)
            
    def mouseDoubleClickEvent(self, event):
        
        self.toggleFullscreen()
            
    def createDB(self):
        
        os.makedirs(self.dbdir)
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.dbfile)
        self.query = QtSql.QSqlQuery()
        self.db.open()
        self.query.exec_("create table shuftery(filename text primary key, "
        "zoom real, winposx int, winposy int, winsizex int, winsizey int, "
        "hscroll int, vscroll int, rotate int)")
        return True
        
    def zoomIn(self):
        
        self.zoom *= 1.05
        self.view.setTransform(QTransform().scale(self.zoom, self.zoom).rotate(self.rotate))
        
    def zoomOut(self):
        
        self.zoom /= 1.05
        self.view.setTransform(QTransform().scale(self.zoom, self.zoom).rotate(self.rotate))
        
    def rotateImg(self, clock):
        
        self.rotval += clock
        if self.rotval == 4:
            self.rotval = 0
        elif self.rotval < 0:
            self.rotval = 3
        self.rotate = self.rotvals[self.rotval]
        self.view.setTransform(QTransform().scale(self.zoom, self.zoom).rotate(self.rotate))
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    shufti = Shufti()
    sys.exit(app.exec_())
