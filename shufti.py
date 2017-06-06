#!/usr/bin/env python

'''
shufti 2.2 - The persistent image viewer

By Dan MacDonald, 2017.

Licensed under the latest GNU Affero GPL license.

Usage:

shufti.py path/to/image

You may want to associate shufti with image files in your file manager rather than
use it from the terminal.
'''

import os, sys, glob
from functools import partial
from PyQt5 import QtCore, QtSql
from PyQt5.QtGui import QPixmap, QTransform
from os.path import expanduser, dirname
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QMenu, QLabel

class ShuftiView(QGraphicsView):
    
    def wheelEvent(self, event):
        
        moose = event.angleDelta().y()/120
        if moose > 0:
            shufti.zoomIn()
        elif moose < 0:
            shufti.zoomOut()
            
    def contextMenuEvent(self, event):
        
        menu = QMenu()
        menu.addAction('Zoom in                 +, e', shufti.zoomIn)
        menu.addAction('Zoom out               -, d', shufti.zoomOut)
        menu.addAction('Toggle fullscreen   F11', shufti.toggleFullscreen)
        menu.addAction('Vertically max.      v', shufti.vertMax)
        menu.addAction('HoriZontally max.  z', shufti.horizMax)
        menu.addAction('Rotate CCW           r', partial(shufti.rotateImg, 1))
        menu.addAction('Spin CW                 s', partial(shufti.rotateImg, -1))
        menu.addAction('Next image            SPACE', partial(shufti.dirBrowse, 1))
        menu.addAction('Previous image      BACKSPACE', partial(shufti.dirBrowse, -1))
        menu.addAction('Fit image                f', shufti.fitView)
        menu.addAction('Reset zoom            1', shufti.zoomReset)
        menu.addAction('About shufti', shufti.about)
        menu.addAction('Quit                        q', shufti.close)
        menu.exec_(event.globalPos())
        

class ShuftiWindow(QMainWindow):
    
    def resizeEvent(self,resizeEvent):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()
        self.view.resize(width + 2, height + 2)
        
    def closeEvent(self, event):
        
        shufti.winState()
        if self.inshuft == 0:
            shufti.dbInsert()
            self.db.close()
        else:
            shufti.dbUpdate()
            self.db.close()
            
class AboutShufti(QLabel):
    
    def __init__(self):
        
        QLabel.__init__(self,"shufti 2.2\n\nBy Dan MacDonald, 2017\n\nIf you find shufti useful, please make a donation via PayPal\n\nallcoms@gmail.com\n\nThanks!")
        self.setAlignment(QtCore.Qt.AlignCenter)

    def initUI(self):               
        
        self.center()
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = app.desktop().availableGeometry().centre()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class Shufti(ShuftiWindow):
    
    def __init__(self):
        super(Shufti,self).__init__()
        try:
            self.key = sys.argv[1]
        except IndexError:
            print('\nshufti 2.2\n\nTo use shufti from the terminal, you must specify the full path to an image as a parameter.\n')
            sys.exit(1)
        self.dbSanitise()
        self.formats = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.pbm', '.pgm', '.ppm',
         '.xbm', '.xpm', '.dds', '.icns', '.jp2', '.mng', '.tga', '.tiff', '.wbmp', '.webp')
        try:
            open(self.key, 'r')
        except IOError:
            print('There was an error opening the file')
            sys.exit(1)
        
        if self.key.lower().endswith(self.formats):
            # If inshuft = 0, the image is not in shufti's image database
            self.inshuft = 0
            self.rotval = 0
            self.rotvals = (0,-90,-180,-270)
            self.dbfile = expanduser("~/.config/shufti/shufti.db")
            self.dbdir = os.path.dirname(self.dbfile)
            if not os.path.isfile(self.dbfile):
                self.createDB()
            self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName(self.dbfile)
            self.db.open()
            self.query = QtSql.QSqlQuery()
            self.dbSearch(self.dbkey)
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
            # Create array of images in current image dir
            self.imgfiles = []
            for filename in glob.glob(str(self.path) + '/*'):
                base, ext = os.path.splitext(filename)
                if ext.lower() in self.formats:
                    self.imgfiles.append(filename)
            # Find location of current image in imgfiles array
            self.dirpos = 0
            while self.dirpos < len(self.imgfiles) and self.imgfiles[self.dirpos] != self.key:
                self.dirpos += 1
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
        self.view.verticalScrollBar().setValue(0)
        self.view.horizontalScrollBar().setValue(0)
        
    def oldImage(self):
        
        if self.rotate == -90:
            self.rotval = 1
        elif self.rotate == -180:
            self.rotval = 2
        elif self.rotate == -270:
            self.rotval = 3
        self.resize(self.img.size())
        self.updateView()
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
        
        if event.key() == QtCore.Qt.Key_F11:
            self.toggleFullscreen()
        elif event.key() == QtCore.Qt.Key_Equal or event.key() == QtCore.Qt.Key_E:
            self.zoomIn()
        elif event.key() == QtCore.Qt.Key_Minus or event.key() == QtCore.Qt.Key_D:
            self.zoomOut()
        elif event.key() == QtCore.Qt.Key_1:
            self.zoomReset()
        elif event.key() == QtCore.Qt.Key_S:
            self.rotateImg(-1)
        elif event.key() == QtCore.Qt.Key_R:
            self.rotateImg(1)
        elif event.key() == QtCore.Qt.Key_F:
            self.fitView()
        elif event.key() == QtCore.Qt.Key_Space:
            self.dirBrowse(1)
        elif event.key() == QtCore.Qt.Key_Backspace:
            self.dirBrowse(-1)
        elif event.key() == QtCore.Qt.Key_V:
            self.vertMax()
        elif event.key() == QtCore.Qt.Key_Z:
            self.horizMax()
        elif event.key() == QtCore.Qt.Key_Q:
            self.close()
            
    def mouseDoubleClickEvent(self, event):
        
        self.toggleFullscreen()
            
    def createDB(self):
        
        if not os.path.exists(self.dbdir):
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
        self.updateView()
        
    def zoomOut(self):
        
        self.zoom /= 1.05
        self.updateView()
        
    def zoomReset(self):
        
        self.zoom = 1
        self.updateView()
        
    def rotateImg(self, clock):
        
        self.rotval += clock
        if self.rotval == 4:
            self.rotval = 0
        elif self.rotval < 0:
            self.rotval = 3
        self.rotate = self.rotvals[self.rotval]
        self.updateView()
        
    def fitView(self):
        
        self.view.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        if self.rotate == 0:
            self.zoom = self.view.transform().m11()
        elif self.rotate == -90:
            self.zoom = (self.view.transform().m12()) * -1
        elif self.rotate == -180:
            self.zoom = (self.view.transform().m11()) * -1
        else:
            self.zoom = self.view.transform().m12()
        
    def updateView(self):
        
        self.view.setTransform(QTransform().scale(self.zoom, self.zoom).rotate(self.rotate))
        
    def winState(self):
        
        self.winsizex = self.geometry().width()
        self.winsizey = self.geometry().height()
        self.vscroll = self.view.verticalScrollBar().value()
        self.hscroll = self.view.horizontalScrollBar().value()
        self.winposx = self.pos().x()
        self.winposy = self.pos().y()
        
    def dbInsert(self):
        
        self.query.exec_("insert into shuftery values('%s" % self.dbkey + 
        "', " + str(self.zoom) + ", " + str(self.winposx) + ", " + str(self.winposy) + 
        ", " + str(self.winsizex) + ", " + str(self.winsizey) + ", " + str(self.hscroll) + 
        ", " + str(self.vscroll) + ", " + str(self.rotate) + ")")
        
    def dbUpdate(self):
        
        self.query.exec_("update shuftery set zoom=" + str(self.zoom) + 
        ", winposx=" + str(self.winposx) + ", winposy=" + str(self.winposy) + 
        ", winsizex=" + str(self.winsizex) + ", winsizey=" + str(self.winsizey) + 
        ", hscroll=" + str(self.hscroll) + ", vscroll=" + str(self.vscroll) + 
        ", rotate=" + str(self.rotate) + " where filename='%s'" % self.dbkey)
        
    def dbSearch(self, field):
        
        self.query.exec_("SELECT * FROM shuftery WHERE filename='%s'" % field)
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
    
    def dbSanitise(self):
        
        self.dbkey = self.key.replace("\"", "\"\"")
        self.dbkey = self.dbkey.replace("\'", "\'\'")
        self.dbkey = self.dbkey.replace("\\", "\\\\")
        
    def dirBrowse(self, direc):
        
        if len(self.imgfiles) > 1:
            self.dirpos += direc
            if self.dirpos > (len(self.imgfiles) - 1):
                self.dirpos = 0
            elif self.dirpos < 0:
                self.dirpos = (len(self.imgfiles) - 1)
            shufti.winState()
            if self.inshuft == 0:
                shufti.dbInsert()
            else:
                shufti.dbUpdate()
            self.key = self.imgfiles[self.dirpos]
            self.dbSanitise()
            self.path, self.title = os.path.split(self.key)
            self.setWindowTitle(str(self.title) + " - shufti")
            self.inshuft = 0
            self.dbSearch(self.dbkey)
            self.scene.clear()
            self.view.resetTransform()
            self.img = QPixmap(self.key)
            self.scene.addPixmap(self.img)
            if self.inshuft == 0:
                self.newImage()
            else:
                self.oldImage()
                
    def vertMax(self):
        
        self.screen_res = app.desktop().availableGeometry(shufti)
        self.screenh = self.screen_res.height()
        self.winsizex = self.geometry().width()
        self.winposx = self.pos().x()
        self.setGeometry(self.winposx, 0, self.winsizex, self.screenh)
        
    def horizMax(self):
        
        self.screen_res = app.desktop().availableGeometry(shufti)
        self.screenw = self.screen_res.width()
        self.winsizey = self.geometry().height()
        self.winposy = self.pos().y()
        self.setGeometry(0, self.winposy, self.screenw, self.winsizey)
        
    def about(self):
        
        self.pop = AboutShufti()
        self.pop.resize(450, 200)
        self.pop.setWindowTitle("About shufti")
        self.pop.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    shufti = Shufti()
    sys.exit(app.exec_())
