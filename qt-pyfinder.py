from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import sys

class QTilemap(QWidget):
    def __init__(self, parent = None):
        super(QTilemap, self).__init__(parent)

        self.map = None
        self.mapRows = 0
        self.mapCols = 0
        self.mapW = 0
        self.mapH = 0
        self.mapX0 = 0
        self.mapY0 = 0
        self.mapX1 = 0
        self.mapY1 = 0

        self.sizeCell = 30
        self.sizeBorder = 1
        self.sizeIncell = self.sizeCell - (self.sizeBorder * 2)

        self.setAutoFillBackground(False)

        self.surfW = 1280
        self.surfH = 720
        self.colorSurf = QColor(0, 0, 0)
        self.surf = QImage(self.surfW, self.surfH, QImage.Format_RGB32)
        self.surf.fill(self.colorSurf)

        self.setFixedSize(self.surfW , self.surfH)

        self.painter = QPainter()

        self.repaint()

    def paintEvent(self, event):
        print("paintEvent")

        self.painter.begin(self)
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(Qt.NoBrush)
        self.painter.drawImage(0, 0, self.surf)
        self.painter.end()

    def setMap(self, map):
        self.map = map

        self.mapRows = len(map)
        self.mapCols = len(map[0])
        self.mapW = self.mapCols * self.sizeCell
        self.mapH = self.mapRows * self.sizeCell
        self.mapX0 = int((self.surfW - self.mapW) / 2)
        self.mapY0 = int((self.surfH - self.mapH) / 2)
        self.mapX1 = self.mapX0 + self.mapW
        self.mapY1 = self.mapY0 + self.mapH

    def drawMap(self, colorBg, colorWalk, colorUnwalk):
        # clear surface
        self.surf.fill(self.colorSurf)

        self.painter.begin(self.surf)

        # draw background
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(colorBg)
        self.painter.drawRect(self.mapX0, self.mapY0, self.mapW, self.mapH)

        # draw cells
        for r in range(self.mapRows):
            cellY = self.mapY0 + (r * self.sizeCell) + self.sizeBorder

            for c in range(self.mapCols):
                cellX = self.mapX0 + (c * self.sizeCell) + self.sizeBorder

                if(self.map[r][c] == 1):
                    self.painter.setBrush(colorWalk)
                elif(self.map[r][c] == 0):
                    self.painter.setBrush(colorUnwalk)
                else:
                    self.painter.setBrush(colorBg)

                self.painter.drawRect(cellX, cellY, self.sizeIncell, self.sizeIncell)

        self.painter.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("qt-pyfinder")

        self.colorBg = QColor(33, 33, 33)
        self.colorWalk = QColor(230, 230, 230)
        self.colorUnwalk = QColor(99, 99, 99)
        self.colorStart = QColor(41, 182, 246)
        self.colorGoal = QColor(0, 230, 118)
        self.colorPath = QColor(255, 245, 157)
        self.colorNoPath = QColor(239, 83, 80)

        # -- File menu --
        self.menuFile = self.menuBar().addMenu("&File")

        self.actOpen = QAction("&Open map", triggered = self.openDialogLoad)
        self.menuFile.addAction(self.actOpen)

        self.menuFile.addSeparator()

        self.actQuit = QAction("&Quit", triggered = self.close)
        self.menuFile.addAction(self.actQuit)

        # -- MainWidget --
        self.widget = QTilemap()
        self.setCentralWidget(self.widget)

        layout = self.layout()
        layout.setSizeConstraint(QLayout.SetFixedSize)

    def openDialogLoad(self):
        fileName, fil = QFileDialog.getOpenFileName(self, "Open Map", "data/maps/", "Map files (*.map)")

        if len(fileName) > 0:
            with open(fileName, 'r') as f:
                fdata = f.readlines()

            # convert map file to usable format
            # 1 = walkable cell
            # 0 = unwalkable cell
            fRows = len(fdata)

            if fRows == 0:
                print("ERROR empty map")
                return

            # skip last column of '\n'
            fCols = len(fdata[0]) - 1

            map = []

            for r in range(fRows):
                map.append([1] * fCols)

            for r in range(fRows):
                for c in range(fCols):
                    if fdata[r][c] == '#':
                        map[r][c] = 0

            self.widget.setMap(map)
            self.widget.drawMap(self.colorBg, self.colorWalk, self.colorUnwalk)
            self.widget.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())
