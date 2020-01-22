from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import astar
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


        self.pf = astar.Pathfinder()
        self.clear_path()

        self.sizeCell = 30
        self.sizeBorder = 1
        self.sizeIncell = self.sizeCell - (self.sizeBorder * 2)

        self.setAutoFillBackground(False)

        self.colorSurf = QColor(0, 0, 0)
        self.colorBg = QColor(33, 33, 33)
        self.colorWalk = QColor(230, 230, 230)
        self.colorUnwalk = QColor(99, 99, 99)
        self.colorStart = QColor(41, 182, 246)
        self.colorGoal = QColor(0, 230, 118)
        self.colorPath = QColor(255, 245, 157)
        self.colorNoPath = QColor(239, 83, 80)

        self.surfW = 1280
        self.surfH = 720
        self.surf = QImage(self.surfW, self.surfH, QImage.Format_RGB32)
        self.surf.fill(self.colorSurf)

        self.setFixedSize(self.surfW , self.surfH)

        self.animating = False
        self.animPathIdx = 0
        self.animFrameTime = 100
        self.animTimer = QTimer(self)
        self.animTimer.timeout.connect(self.nextAnimFrame)

        self.painter = QPainter()

        self.repaint()

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(Qt.NoBrush)
        self.painter.drawImage(0, 0, self.surf)
        self.painter.end()

    def nextAnimFrame(self):
        if self.animating:
            if self.animPathIdx > 0 and self.animPathIdx < (len(self.path) - 1):
                cell = self.path[self.animPathIdx]

                self.draw_cell(cell, self.colorPath)
                self.repaint()

                self.animPathIdx += 1
            else:
                self.animating = False
                self.animTimer.stop()
                self.animPathIdx = 0

    def set_anim_speed(self, speed):
        if speed > 0 and speed < 11:
            self.animFrameTime = 500 / speed

    def get_anim_speed(self):
        return 500 / self.animFrameTime

    def clear_path(self):
        self.path = []
        self.start = None
        self.goal = None

    def setMap(self, map):
        self.map = map

        self.pf.set_map(map)

        self.mapRows = len(map)
        self.mapCols = len(map[0])

        self.clear_path()

        self.update_map_size()

    def is_cell_walkable(self, cell):
        """Check if a cell is walkable.

        Parameters
        ----------
        cell : tuple
            row, col that define a cell of the map

        Returns
        -------
        bool
            True if the cell is walkable, False otherwise
        """

        if self.map == None:
            return False

        r, c = cell
        return self.map[r][c] == 1

    def draw_map(self):
        # clear surface
        self.surf.fill(self.colorSurf)

        self.painter.begin(self.surf)

        # draw background
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(self.colorBg)
        self.painter.drawRect(self.mapX0, self.mapY0, self.mapW, self.mapH)

        # draw cells
        for r in range(self.mapRows):
            cellY = self.mapY0 + (r * self.sizeCell) + self.sizeBorder

            for c in range(self.mapCols):
                cellX = self.mapX0 + (c * self.sizeCell) + self.sizeBorder

                if(self.map[r][c] == 1):
                    self.painter.setBrush(self.colorWalk)
                elif(self.map[r][c] == 0):
                    self.painter.setBrush(self.colorUnwalk)
                else:
                    self.painter.setBrush(self.colorBg)

                self.painter.drawRect(cellX, cellY, self.sizeIncell, self.sizeIncell)

        self.painter.end()

    def draw_cell(self, cell, color):
        r, c = cell

        cellX = self.mapX0 + (c * self.sizeCell) + self.sizeBorder
        cellY = self.mapY0 + (r * self.sizeCell) + self.sizeBorder

        self.painter.begin(self.surf)
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(color)
        self.painter.drawRect(cellX, cellY, self.sizeIncell, self.sizeIncell)
        self.painter.end()

    def get_cell_size(self):
        return self.sizeCell

    def set_cell_size(self, size):
        self.sizeCell = size
        self.sizeIncell = self.sizeCell - (self.sizeBorder * 2)

        self.update_map_size()

        self.clear_path()

    def get_cell_from_point(self, point):
        """Return the cell corresponding to a point in the map.

        Parameters
        ----------
        point : QPoint
            x, y coordinates

        Returns
        -------
        tuple
            row, col that define a cell of the map
        """
        return (int((point.y() - self.mapY0) / self.sizeCell), int((point.x() - self.mapX0) / self.sizeCell))


    def is_point_inside(self, point):
        """Check if a point is inside the map.

        Parameters
        ----------
        point : QPoint
            x, y coordinates

        Returns
        -------
        bool
            True if the point is inside the map, False otherwise
        """
        x, y = point.x(), point.y()
        return x > self.mapX0 and x < self.mapX1 and y > self.mapY0 and y < self.mapY1

    def has_map(self):
        return self.map != None

    def update_map_size(self):
        self.mapW = self.mapCols * self.sizeCell
        self.mapH = self.mapRows * self.sizeCell
        self.mapX0 = int((self.surfW - self.mapW) / 2)
        self.mapY0 = int((self.surfH - self.mapH) / 2)
        self.mapX1 = self.mapX0 + self.mapW
        self.mapY1 = self.mapY0 + self.mapH

    def mouseReleaseEvent(self, event):
        if (event.button() != Qt.LeftButton):
            return

        if not self.is_point_inside(event.pos()):
            return

        if self.animating:
            return

        # set start
        if self.start == None:
            self.start = self.get_cell_from_point(event.pos())

            if self.is_cell_walkable(self.start):
                self.draw_cell(self.start, self.colorStart)
                self.repaint()
            else:
                self.start = None

        # set goal
        elif self.goal == None:
            self.goal = self.get_cell_from_point(event.pos())

            if self.is_cell_walkable(self.goal) and self.start != self.goal:
                self.draw_cell(self.goal, self.colorGoal)

                try:
                    self.path = self.pf.make_path(self.start, self.goal)

                    # path found -> start animation
                    if len(self.path) > 0:
                        self.animating = True
                        self.animPathIdx = 1
                        self.animTimer.start(self.animFrameTime)
                    # no path found
                    else:
                        self.draw_cell(self.start, self.colorNoPath)
                        self.draw_cell(self.goal, self.colorNoPath)
                        self.repaint()

                except Exception as ex:
                    print("ERROR {}".format(ex))

                self.repaint()
            else:
                self.goal = None

        # clear everything
        else:
            if len(self.path) > 0:
                for cell in self.path:
                    self.draw_cell(cell, self.colorWalk)

            else:
                self.draw_cell(self.start, self.colorWalk)
                self.draw_cell(self.goal, self.colorWalk)

            self.start = None
            self.goal = None

            self.repaint()

class DialogOptions(QDialog):
    def __init__(self, parent = None):
        super(DialogOptions, self).__init__(parent)

        self.setWindowTitle("Options")

        self.setMinimumSize(300, 179)

        layout = QGridLayout()
        self.setLayout(layout)

        row = 0

        # cell size
        label = QLabel("Cell size (in px):")
        layout.addWidget(label, row, 0)

        self.inputCell = QSpinBox()
        self.inputCell.setRange(1, 100)
        layout.addWidget(self.inputCell, row, 2)

        row += 1

        # anim speed
        label = QLabel("Animation speed [1-10]:")
        layout.addWidget(label, row, 0)

        self.animSpeed = QSlider(Qt.Horizontal, self)
        self.animSpeed.setMinimum(1)
        self.animSpeed.setMaximum(10)
        layout.addWidget(self.animSpeed, row, 2)

        row += 1

        # spacer
        spacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addItem(spacer, row, 0, 1, 4)

        row += 1

        # CANCEL, OK buttons
        layoutRow = QHBoxLayout()

        buttonCanc = QPushButton("CANCEL")
        buttonCanc.clicked.connect(self.reject)
        layoutRow.addWidget(buttonCanc)

        buttonOK = QPushButton("OK")
        buttonOK.setDefault(True)
        buttonOK.clicked.connect(self.accept)
        layoutRow.addWidget(buttonOK)

        layout.addLayout(layoutRow, row, 0, 1, 4)

    def get_cell_size(self):
        return self.inputCell.value()

    def set_cell_size(self, size):
        self.inputCell.setValue(size)

    def get_anim_speed(self):
        return self.animSpeed.value()

    def set_anim_speed(self, speed):
        self.animSpeed.setValue(speed)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("qt-pyfinder")

        # -- File menu --
        self.menuFile = self.menuBar().addMenu("&File")

        self.actOpen = QAction("&Open map", triggered = self.openDialogLoad)
        self.menuFile.addAction(self.actOpen)

        self.menuFile.addSeparator()

        self.actOpt = QAction("O&ptions", triggered = self.openDialogOptions)
        self.menuFile.addAction(self.actOpt)

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
            self.widget.draw_map()
            self.widget.repaint()

    def openDialogOptions(self):
        self.dialogOpt = DialogOptions(self)
        self.dialogOpt.set_cell_size(self.widget.get_cell_size())
        self.dialogOpt.set_anim_speed(self.widget.get_anim_speed())
        self.dialogOpt.finished.connect(self.dialogOptFinished)

        self.dialogOpt.open()

    @Slot()
    def dialogOptFinished(self, result):
        if result != QDialog.Accepted:
            return

        # update size cell
        sizeCell = self.dialogOpt.get_cell_size()

        if sizeCell != self.widget.get_cell_size():
            self.widget.set_cell_size(sizeCell)

            if self.widget.has_map():
                self.widget.draw_map()
                self.widget.repaint()

        # animation speed
        animSpeed = self.dialogOpt.get_anim_speed()

        if animSpeed != self.widget.get_anim_speed():
            self.widget.set_anim_speed(animSpeed)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())
