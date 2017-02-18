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

# We need to sublass QMainWindow to enable realtime resizing of the QGrapicsView
# display area when the user resizes a window
class ShuftiWindow(QMainWindow):
    
    def resizeEvent(self,resizeEvent):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        self.view.resize(width + 2, height + 2)
        
    def closeEvent(self, event):
        winsizex = self.frameGeometry().width()
        winsizey = self.frameGeometry().height()
        vscroll = self.view.verticalScrollBar().value()
        hscroll = self.view.horizontalScrollBar().value()
        winposx = self.pos().x()
        winposy = self.pos().y()
        if self.inshuft == 0:
            self.query.exec_("insert into shuftery values('" + str(self.key) + 
            "', " + str(self.zoomlev) + ", " + str(winposx) + ", " + str(winposy) + 
            ", " + str(winsizex) + ", " + str(winsizey) + ", " + str(hscroll) + 
            ", " + str(vscroll) + ")")
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
            # If inshuft = 0, an image is not in shufti's image database
            self.inshuft = 0
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
                self.zoomlev = self.query.value(1)
                self.winposx = self.query.value(2)
                self.winposy = self.query.value(3)
                self.winsizex = self.query.value(4)
                self.winsizey = self.query.value(5)
                self.hscroll = self.query.value(6)
                self.vscroll = self.query.value(7)
                self.inshuft = 1
            # Set common window attributes
            self.setWindowTitle("shufti")
            self.img = QPixmap(self.key)
            self.zoom = 1
            self.scene = QGraphicsScene()
            self.scene.addPixmap(self.img)
            self.view = QGraphicsView(self.scene, self)
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
        
        self.zoomlev = 0
        self.resize(self.img.size())
        self.view.resize(self.img.width() + 2, self.img.height() + 2)
        self.show()
        
    def oldImage(self):
        
        self.resize(self.winsizex, self.winsizey)
        #self.view.resize(self.winsizex + 2, self.winsizey + 2)
        if self.zoomlev > 0:
            for _ in range(self.zoomlev):
                self.zoom *= 1.05
                self.view.scale(self.zoom, self.zoom)
        elif self.zoomlev < 0:
            for _ in range((self.zoomlev * -1)):
                self.zoom = 1 - (self.zoom / 20)
                self.view.scale(self.zoom, self.zoom)
        self.show()
        self.view.verticalScrollBar().setValue(self.vscroll)
        self.view.horizontalScrollBar().setValue(self.hscroll)
        # Attempt at placing window
        #self.view.mapToGlobal(QtCore.QPoint(self.winposx, self.winposy))
        
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
            self.zoomlev += 1
        elif event.key() == QtCore.Qt.Key_Minus:
            self.zoom = 1 - (self.zoom / 20)
            self.view.scale(self.zoom, self.zoom)
            self.zoomlev -= 1
            
    def createDB(self):
        
        os.makedirs(self.dbdir)
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.dbfile)
        self.query = QtSql.QSqlQuery()
        self.db.open()
        self.query.exec_("create table shuftery(filename text primary key, "
        "zoomlev int, winposx int, winposy int, winsizex int, winsizey int, "
        "hscroll int, vscroll int)")
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
