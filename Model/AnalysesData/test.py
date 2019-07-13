# from PyQt4 import QtGui  # (the example applies equally well to PySide)
# import pyqtgraph as pg
#
# ## Always start by initializing Qt (only once per application)
# app = QtGui.QApplication([])
#
# ## Define a top-level widget to hold everything
# w = QtGui.QWidget()
#
# ## Create some widgets to be placed inside
# btn = QtGui.QPushButton('press me')
# text = QtGui.QLineEdit('enter text')
# listw = QtGui.QListWidget()
# plot = pg.PlotWidget()
#
# ## Create a grid layout to manage the widgets size and position
# layout = QtGui.QGridLayout()
# w.setLayout(layout)
#
# ## Add widgets to the layout in their proper positions
# layout.addWidget(btn, 0, 0)   # button goes in upper-left
# layout.addWidget(text, 1, 0)   # text edit goes in middle-left
# layout.addWidget(listw, 2, 0)  # list widget goes in bottom-left
# layout.addWidget(plot, 0, 1, 3, 1)  # plot goes on right side, spanning 3 rows
#
# ## Display the widget as a new window
# w.show()
#
# ## Start the Qt event loop
# app.exec_()

import sys
import pathlib
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    count = 0

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        bar = self.menuBar()

        load_fluore_img = QAction("Load fluorescence img", self)
        load_absorption_img = QAction("Load absorption images", self)
        save_fluore_img = QAction("save fluorescence image", self)
        save_absorption_imgs = QAction("Save absorption images", self)

        load_absorption_img.triggered.connect(self.absorptionImgs)
        load_fluore_img.triggered.connect(self.flourescenceImg)
        # save_fluore_img.triggered.connect(self.save_fluore)
        # save_absorption_imgs.triggered.connect(self.save_absorption)



        load_save_image = bar.addMenu("Load and Save")
        load_save_image.addAction(load_fluore_img)
        load_save_image.addAction(load_absorption_img)
        load_save_image.addAction(save_fluore_img)
        load_save_image.addAction(save_absorption_imgs)


        plot = bar.addMenu("Plot")
        plot.addAction("fluorescence img")
        plot.addAction("absorption imgs")
        plot.addAction("New")
        plot.addAction("cascade")
        plot.addAction("Tiled")
        plot.triggered[QAction].connect(self.windowaction)

        bar.addMenu("Image Process")
        ImgProcessDockWidget = QDockWidget("Image Process Console", self)
        ImgProcessDockWidget.setAllowedAreas(
            Qt.LeftDockWidgetArea |Qt.RightDockWidgetArea
            | Qt.BottomDockWidgetArea)


        # add console widget to dock
        ImgProcessDockWidget.setWidget(ImgProcess)
        self.addDockWidget(Qt.RightDockWidgetArea, ImgProcessDockWidget)

        # enable the toggle view action
        bar.addAction(ImgProcessDockWidget.toggleViewAction())

        self.setWindowTitle("MDI demo")


    def loadImg(self):
        print("load--flourescence img")
        fname, _ = QFileDialog.getOpenFileName(self, '选择图片', 'c:\\', 'Image files(*.jpg *.gif *.png)')
        print(fname)
        return fname

    def loadImgFile(self):
        print("load absorption-file")
        fpath, _ = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      "./")  # 起始路径
        print(fpath)
        return fpath


    def flourescenceImg(self):
        print("flourescence")
        sub = QMdiSubWindow()
        flour = QLabel()
        sub.setWidget(flour)

        self.mdi.addSubWindow(sub)
        fname = self.loadImg()
        flour.setPixmap(QPixmap(fname))
        sub.show()

    def absorptionImgs(self):
        self.absorption = {"WI":QLabel(),
                           "WO":QLabel(),
                           "BKG":QLabel(),
                           "IMG":QLabel()
                           }
        fpath = self.loadImgFile()
        print(fpath)
        for i in self.absorption.keys():
            print(i)
            sub = QMdiSubWindow()
            sub.setWidget(self.absorption[i])
            self.mdi.addSubWindow(sub)
            # print(pathlib.Path(fpath+"/"+i+'.jpg'))
            # self.absorption[i].setPixmap(QPixmap(pathlib.Path(fpath+"/"+i+'.png')))

            sub.show()


    def windowaction(self, q):
        print("triggered")

        if q.text() == "New":
            MainWindow.count = MainWindow.count + 1
            sub = QMdiSubWindow()
            sub.setWidget(QTextEdit())
            sub.setWindowTitle("subwindow" + str(MainWindow.count))
            self.mdi.addSubWindow(sub)
            sub.show()

        if q.text() == "cascade":
            self.mdi.cascadeSubWindows()

        if q.text() == "Tiled":
            self.mdi.tileSubWindows()

class ImgProcess(QWidget):
    """
    1. roi status
    2.the number of atom

    """
    addRoiCs = pyqtSignal()
    def __init__(self, parent):
        super(ImgProcess, self).__init__(parent=parent)
        self.parent = parent
        self.roi = QPushButton("roi", self)

        self.grid_layout = QGridLayout()
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.roi)

        self.grid_layout.addLayout(self.horizontal_layout, 0, 0)


    def addROICS(self):
        self.addRoi.emit()



    def updateCrossSection(self):
        pass

    def calculateAtom(self, roiImg, anotherParas):
        """
        calculate atom number for absorption mode
        :return:
        """
        pass

    def calculateOD(self, roiImg, anotherParas):
        """
        calculate optic density
        :return:
        """
        pass



class ImgDisplay(QWidget):
    """

    2. background image status
    3. photon range status
    4. magnification status



    """

    def __init__(self):
        super(ImgDisplay, self).__init__()

        self.roi = QPushButton("roi",self)
        self.pause_cam = QPushButton("pause",self)
        self.capture_cam = QPushButton("capture",self)
        self.stop_cam = QPushButton("stop",self)
        self.grid_layout = QGridLayout()
        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.start_cam)
        self.horizontal_layout.addWidget(self.pause_cam)
        self.horizontal_layout.addWidget(self.capture_cam)
        self.horizontal_layout.addWidget(self.stop_cam)

        self.grid_layout.addLayout(self.horizontal_layout,0,0)

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()