import sys
from Utilities.Helper import Helper
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QFileDialog, QAction
from PIL import Image
from pathlib import Path
import settings
import numpy as np


class TestMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        settings.inintParams()
        self.initUI()

    def initUI(self):



        self.widgets = {}
        # # create the central part of the application
        # self.zoneCenter = QMdiArea()
        # self.setCentralWidget(self.zoneCenter)

        # set up menus and toolbars
        self.fileMenu = self.menuBar().addMenu("File")

        self.plotMenu = self.menuBar().addMenu("Plot")
        self.windowMenu = self.menuBar().addMenu("Window")
        self.optionMenu = self.menuBar().addMenu("Options")

        self.plotToolbar = self.addToolBar("Plot")
        self.instToolbar = self.addToolBar("Instruments")




        self.show()





    def ImgFilePath(self):
        fpath, _ = QFileDialog.getExistingDirectory(self, "Open File", "./")
        self.loadABSImgs(fpath)

    def ImgPath(self):
        fpath, _ = QFileDialog.getOpenFileName(self, "Open Image", "c:\\", "Image files (*.jpg *.gif)")

    def saveImg(self):
        pass


    def saveImgFile(self):
        pass


    def loadFluorescenceImg(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Image", "c:\\", "Image files (*.jpg *.gif)")
        img = Image.open(path)
        self.data = np.ones((200, 150)) * 0
        self.data[0:2, :] = 255
        self.data[198:200, :] = 255
        self.data[:, 0:2] = 255
        self.data[:, 148:150] = 255
        img = self.data
        settings.ImgData["FluorescenceImg"] = img








if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestMainWindow()
    sys.exit(app.exec_())