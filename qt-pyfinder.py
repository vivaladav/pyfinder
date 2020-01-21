from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import sys

class MainWidget(QWidget):
    def __init__(self, parent = None):
        super(MainWidget, self).__init__(parent)

        self.imgW = 1280
        self.imgH = 720

        self.setAutoFillBackground(False)

        self.setFixedSize(self.imgW , self.imgH)

        self.surface = QImage(self.imgW, self.imgH, QImage.Format_ARGB32)
        self.surface.fill(QColor(0, 0, 0, 255))

        self.painter = QPainter()

        self.repaint()

    def paintEvent(self, event):
        print("paintEvent")
        self.painter.begin(self)
        self.painter.drawImage(0, 0, self.surface)
        self.painter.end()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("qt-pyfinder")

        # -- File menu --
        self.menuFile = self.menuBar().addMenu("&File")

        self.actOpen = QAction("&Open map", triggered = self.openDialogLoad)
        self.menuFile.addAction(self.actOpen)

        self.menuFile.addSeparator()

        self.actQuit = QAction("&Quit", triggered = self.close)
        self.menuFile.addAction(self.actQuit)

        # -- MainWidget --
        self.widget = MainWidget()
        self.setCentralWidget(self.widget)

        layout = self.layout()
        layout.setSizeConstraint(QLayout.SetFixedSize)

    def openDialogLoad(self):
        fileName, fil = QFileDialog.getOpenFileName(self, "Open Map", "data/maps/", "Map files (*.map)")
        print(fileName)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWin = MainWindow()
    mainWin.show()

    sys.exit(app.exec_())
