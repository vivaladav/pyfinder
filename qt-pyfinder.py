import astar

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from enum import IntEnum, unique
import sys

@unique
class Colors(IntEnum):
    """List of colors used to render the map."""
    BG_MAP = 1
    BG_SURF = 2
    CELL_GOAL = 3
    CELL_NOPATH = 4
    CELL_PATH = 5
    CELL_START = 6
    CELL_UNWALK = 7
    CELL_WALK = 8

class QTilemap(QWidget):
    """A 2D map made of tiles using Qt for rendering and input handling."""

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

        self.colors = { Colors.BG_MAP : QColor(33, 33, 33), \
                        Colors.BG_SURF : QColor(0, 0, 0), \
                        Colors.CELL_GOAL : QColor(0, 230, 118), \
                        Colors.CELL_NOPATH : QColor(239, 83, 80), \
                        Colors.CELL_PATH : QColor(255, 245, 157), \
                        Colors.CELL_START : QColor(41, 182, 246), \
                        Colors.CELL_UNWALK : QColor(99, 99, 99), \
                        Colors.CELL_WALK : QColor(230, 230, 230) }

        self.surfW = 1280
        self.surfH = 720
        self.surf = QImage(self.surfW, self.surfH, QImage.Format_RGB32)
        self.clear_surface()

        self.setFixedSize(self.surfW , self.surfH)

        self.animating = False
        self.animPathIdx = 0
        self.animFrameTime = 100
        self.animTimer = QTimer(self)
        self.animTimer.timeout.connect(self.next_anim_frame)

        self.painter = QPainter()

    def clear_surface(self):
        self.surf.fill(self.colors[Colors.BG_SURF])

    def get_color(self, colorId):
        if colorId in self.colors:
            return self.colors[colorId]
        else:
            return QColor(255, 0, 255)

    def set_color(self, colorId, color):
        if colorId in self.colors:
            self.colors[colorId] = color

    def paintEvent(self, event):
        self.painter.begin(self)
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(Qt.NoBrush)
        self.painter.drawImage(0, 0, self.surf)
        self.painter.end()

    def next_anim_frame(self):
        if self.animating:
            if self.animPathIdx > 0 and self.animPathIdx < (len(self.path) - 1):
                cell = self.path[self.animPathIdx]

                self.draw_cell(cell, self.colors[Colors.CELL_PATH])
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

    def set_map(self, map):
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
        self.surf.fill(self.colors[Colors.BG_SURF])

        self.painter.begin(self.surf)

        # draw background
        self.painter.setPen(Qt.NoPen)
        self.painter.setBrush(self.colors[Colors.BG_MAP])
        self.painter.drawRect(self.mapX0, self.mapY0, self.mapW, self.mapH)

        # draw cells
        for r in range(self.mapRows):
            cellY = self.mapY0 + (r * self.sizeCell) + self.sizeBorder

            for c in range(self.mapCols):
                cellX = self.mapX0 + (c * self.sizeCell) + self.sizeBorder

                if(self.map[r][c] == 1):
                    self.painter.setBrush(self.colors[Colors.CELL_WALK])
                elif(self.map[r][c] == 0):
                    self.painter.setBrush(self.colors[Colors.CELL_UNWALK])
                else:
                    self.painter.setBrush(self.colors[Colors.BG_MAP])

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
                self.draw_cell(self.start, self.colors[Colors.CELL_START])
                self.repaint()
            else:
                self.start = None

        # set goal
        elif self.goal == None:
            self.goal = self.get_cell_from_point(event.pos())

            if self.is_cell_walkable(self.goal) and self.start != self.goal:
                self.draw_cell(self.goal, self.colors[Colors.CELL_GOAL])

                try:
                    self.path = self.pf.make_path(self.start, self.goal)

                    # path found -> start animation
                    if len(self.path) > 0:
                        self.animating = True
                        self.animPathIdx = 1
                        self.animTimer.start(self.animFrameTime)
                    # no path found
                    else:
                        self.draw_cell(self.start, self.colors[Colors.CELL_NOPATH])
                        self.draw_cell(self.goal, self.colors[Colors.CELL_NOPATH])
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
                    self.draw_cell(cell, self.colors[Colors.CELL_WALK])

            else:
                self.draw_cell(self.start, self.colors[Colors.CELL_WALK])
                self.draw_cell(self.goal, self.colors[Colors.CELL_WALK])

            self.start = None
            self.goal = None

            self.repaint()

class DialogOptions(QDialog):
    """Dialog that allows to set several options like cell size, animation speed and colors."""

    def __init__(self, parent = None):
        super(DialogOptions, self).__init__(parent)

        self.setWindowTitle("Options")

        self.setMinimumSize(300, 179)

        layout = QVBoxLayout()
        self.setLayout(layout)

        group = self.create_group_map()
        layout.addWidget(group)

        self.colors = dict()
        group = self.create_group_colors()
        layout.addWidget(group)

        # spacer
        spacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addItem(spacer)

        # CANCEL, OK buttons
        layoutRow = QHBoxLayout()

        buttonCanc = QPushButton("CANCEL")
        buttonCanc.setMaximumWidth(100)
        buttonCanc.clicked.connect(self.reject)
        layoutRow.addWidget(buttonCanc)

        buttonOK = QPushButton("OK")
        buttonOK.setDefault(True)
        buttonOK.setMaximumWidth(100)
        buttonOK.clicked.connect(self.accept)
        layoutRow.addWidget(buttonOK)

        layout.addLayout(layoutRow)

    def create_group_map(self):
        group = QGroupBox("Map")

        layout = QGridLayout()
        layout.setColumnMinimumWidth(0, 200)
        group.setLayout(layout)

        # CELL SIZE
        label = QLabel("Cell size (in px):")
        layout.addWidget(label, 0, 0)

        self.inputCell = QSpinBox()
        self.inputCell.setRange(1, 100)
        layout.addWidget(self.inputCell, 0, 1)

        # ANIMATION SPEED
        label = QLabel("Animation speed:")
        layout.addWidget(label, 1, 0)

        self.animSpeed = QSlider(Qt.Horizontal, self)
        self.animSpeed.setMinimum(1)
        self.animSpeed.setMaximum(10)
        layout.addWidget(self.animSpeed, 1, 1)

        return group

    def create_group_colors(self):
        group = QGroupBox("Colors")

        layout = QGridLayout()
        layout.setColumnMinimumWidth(0, 200)
        group.setLayout(layout)

        strings = [ "MAP background:", "WINDOW background:", "GOAL cell:", "NO PATH cell:",\
                    "PATH cell:", "START cell:", "UNWALKABLE cell:", "WALKABLE cell:" ]
        ids = list(Colors)

        for row in range(len(Colors)):
            self.create_color_row(strings[row], ids[row], layout, row)

        return group

    def create_color_row(self, text, colorId, layout, row):
        label = QLabel(text)
        layout.addWidget(label, row, 0)

        button = ButtonColor(colorId)
        layout.addWidget(button, row, 1, 1, 1, Qt.AlignRight)

        self.colors[colorId] = button

    def get_color(self, colorId):
        if colorId in self.colors:
            return self.colors[colorId].color
        else:
            return QColor(255, 0, 255)

    def set_color(self, colorId, color):
        if colorId not in self.colors:
            return

        button = self.colors[colorId]
        button.set_color(color)

    def get_cell_size(self):
        return self.inputCell.value()

    def set_cell_size(self, size):
        self.inputCell.setValue(size)

    def get_anim_speed(self):
        return self.animSpeed.value()

    def set_anim_speed(self, speed):
        self.animSpeed.setValue(speed)

class ButtonColor(QPushButton):
    """A button that can be used to show and set a color."""

    def __init__(self, colorId, color = QColor(), parent = None):
        super(ButtonColor, self).__init__(parent)

        self.colorId = colorId
        self.color = color

        self.setFixedSize(32, 32)

        self.clicked.connect(self.button_color_clicked)

    def set_color(self, color):
        self.color = color

        pal = self.palette()
        pal.setColor(QPalette.Button, color)
        self.setPalette(pal)

    @Slot()
    def button_color_clicked(self, checked):
        color = QColorDialog.getColor(self.color, self.parentWidget())

        if color.isValid():
            self.set_color(color)

class MainWindow(QMainWindow):
    """Main window of the application that contains the rendering surface and a menubar."""

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("qt-pyfinder")

        # -- File menu --
        self.menuFile = self.menuBar().addMenu("&File")

        self.actOpen = QAction("&Open map", triggered = self.open_dialog_load)
        self.menuFile.addAction(self.actOpen)

        self.menuFile.addSeparator()

        self.actOpt = QAction("O&ptions", triggered = self.open_dialog_options)
        self.menuFile.addAction(self.actOpt)

        self.menuFile.addSeparator()

        self.actQuit = QAction("&Quit", triggered = self.close)
        self.menuFile.addAction(self.actQuit)

        # -- MainWidget --
        self.widget = QTilemap()
        self.setCentralWidget(self.widget)

        layout = self.layout()
        layout.setSizeConstraint(QLayout.SetFixedSize)

    def open_dialog_load(self):
        fileName, fil = QFileDialog.getOpenFileName(self, "Open Map", "data/maps/", "Map files (*.map)")

        # have a file to load
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

            self.widget.set_map(map)
            self.widget.draw_map()
            self.widget.repaint()

    def open_dialog_options(self):
        self.dialogOpt = DialogOptions(self)

        self.dialogOpt.set_cell_size(self.widget.get_cell_size())
        self.dialogOpt.set_anim_speed(self.widget.get_anim_speed())

        for colorId in Colors:
            self.dialogOpt.set_color(colorId, self.widget.get_color(colorId))

        self.dialogOpt.finished.connect(self.dialog_opt_finished)

        self.dialogOpt.open()

    @Slot()
    def dialog_opt_finished(self, result):
        if result != QDialog.Accepted:
            return

        changed = False

        # update size cell
        sizeCell = self.dialogOpt.get_cell_size()

        if sizeCell != self.widget.get_cell_size():
            changed = True
            self.widget.set_cell_size(sizeCell)

        # animation speed
        animSpeed = self.dialogOpt.get_anim_speed()

        if animSpeed != self.widget.get_anim_speed():
            self.widget.set_anim_speed(animSpeed)

        # colors
        for colorId in Colors:
            newColor = self.dialogOpt.get_color(colorId)

            if self.widget.get_color(colorId) != newColor:
                changed = True
                self.widget.set_color(colorId, newColor)

        # redraw
        if changed:
            # redraw everything
            if self.widget.has_map():
                self.widget.clear_path()
                self.widget.draw_map()
            # redraw window background only
            else:
                self.widget.clear_surface()

            self.widget.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())
