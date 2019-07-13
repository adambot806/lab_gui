
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PIL import Image
from MainWindow import TestMainWindow
import sys
import settings
import numpy as np


class ImgDisplaySetting(QWidget):
    """
    1. background image status
    2. photon range status
    3. magnification status
    4. load and save images
    """
    magnification = pyqtSignal(bool)
    photonRange = pyqtSignal(bool)

    FluorescenceImg = pyqtSignal()
    ABSImg = pyqtSignal()


    def __init__(self, parent=None):
        super(ImgDisplaySetting, self).__init__(parent)
        self.parent = parent

        self.GroupBox1 = QGroupBox("Image Display Setting")
        self.GroupBox2 = QGroupBox("Experiment Parameters")
        layout1 = QVBoxLayout()

        bkg = QHBoxLayout()
        self.bkgStatus = QCheckBox("subtract background image", self)
        self.bkgLoad = QPushButton("load background image", self)
        bkg.addWidget(self.bkgStatus)
        bkg.addWidget(self.bkgLoad)

        pf = QVBoxLayout()
        self.pfStatus = QCheckBox('photon filter', self)
        Min = QHBoxLayout()
        RangeMin = QLabel('Min')
        self.pfMin = QDoubleSpinBox()
        self.pfMin.setMinimum(20)  # Prevent numerical underflow
        self.pfMin.setSingleStep(1)
        Min.addWidget(RangeMin)
        Min.addWidget(self.pfMin)


        Max = QHBoxLayout()
        RangeMax = QLabel('Max')
        self.pfMax = QDoubleSpinBox()
        self.pfMax.setMaximum(255)
        self.pfMax.setSingleStep(1)
        Max.addWidget(RangeMax)
        Max.addWidget(self.pfMax)

        pf.addWidget(self.pfStatus)
        pf.addLayout(Min)
        pf.addLayout(Max)


        mf = QHBoxLayout()
        self.magStatus = QCheckBox('magnification')
        self.magValue = QDoubleSpinBox()
        self.magValue.setRange(0.01,10)
        self.magValue.setSingleStep(0.1)
        mf.addWidget(self.magStatus)
        mf.addWidget(self.magValue)


        imgSource = QHBoxLayout()
        self.fromDisk = QRadioButton('disk', self)
        self.fromCamera = QRadioButton('camera', self)
        imgSource.addWidget(self.fromCamera)
        imgSource.addWidget(self.fromDisk)


        mode = QHBoxLayout()
        self.vanillaWin = QRadioButton('video mode', self)
        self.singleWin = QRadioButton('single mode', self)
        self.ABSWin = QRadioButton('absorption mode', self)
        mode.addWidget(self.vanillaWin)
        mode.addWidget(self.singleWin)
        mode.addWidget(self.ABSWin)





        layout1.addLayout(bkg)
        layout1.addLayout(pf)
        layout1.addLayout(mf)
        layout1.addLayout(imgSource)
        layout1.addLayout(mode)





        self.GroupBox1.setLayout(layout1)
        # self.GroupBox2.setLayout(layout2)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.GroupBox1)
        # self.vertical_layout.addWidget(self.GroupBox2)


        self.setLayout(self.vertical_layout)

        self.default_setting()

        self.fromDisk.toggled.connect(lambda: self.rdbstate(self.fromDisk))
        self.fromCamera.toggled.connect(lambda: self.rdbstate(self.fromCamera))

        self.singleWin.toggled.connect(lambda: self.rdbstate(self.singleWin))
        self.vanillaWin.toggled.connect(lambda: self.rdbstate(self.vanillaWin))
        self.ABSWin.toggled.connect(lambda: self.rdbstate(self.ABSWin))

        self.bkgStatus.stateChanged.connect(lambda: self.ckbstate(self.bkgStatus))
        self.magStatus.stateChanged.connect(lambda: self.ckbstate(self.magStatus))
        self.pfStatus.stateChanged.connect(lambda: self.ckbstate(self.pfStatus))

        self.magValue.valueChanged.connect(self.changeMagValue)
        self.pfMin.valueChanged.connect(self.changePfMin)
        self.pfMax.valueChanged.connect(self.changePfMax)

        self.bkgLoad.clicked.connect(self.loadbkgImg)





    def loadbkgImg(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open Image', 'c:\\', 'Image files(*.jpg *.gif *.png)')
        img = Image.open(path)
        self.data = np.ones((200, 150)) * 200


        img = self.data
        settings.ImgData["bkgImg"] = img
        # settings.ImgData["bkgImg"].show()








    def default_setting(self):
        first = True
        if first:
            if settings.params["Image Display Setting"]["imgSource"] == "disk":
                self.fromCamera.setChecked(False)
                self.fromDisk.setChecked(True)
            if settings.params["Image Display Setting"]["imgSource"] == "Camera":
                self.fromDisk.setChecked(False)
                self.fromCamera.setChecked(True)

            if settings.params["Image Display Setting"]["imgSource"] == None:
                self.fromDisk.setChecked(False)
                self.fromCamera.setChecked(False)

            if settings.params["Image Display Setting"]["mode"] == "video mode":
                self.ABSWin.setChecked(False)
                self.singleWin.setChecked(False)
                self.vanillaWin.setChecked(True)


            if settings.params["Image Display Setting"]["mode"] == "single mode":
                self.vanillaWin.setChecked(False)
                self.ABSWin.setChecked(False)
                self.singleWin.setChecked(True)

            if settings.params["Image Display Setting"]["mode"] == "absorption mode":
                self.singleWin.setChecked(False)
                self.vanillaWin.setChecked(False)
                self.ABSWin.setChecked(True)

            if settings.params["Image Display Setting"]["mode"] == None:
                self.ABSWin.setChecked(False)
                self.singleWin.setChecked(False)
                self.vanillaWin.setChecked(False)

            self.bkgStatus.setChecked(settings.params["Image Display Setting"]["bkgStatus"])
            self.pfStatus.setChecked(settings.params["Image Display Setting"]["pfStatus"])
            self.magStatus.setChecked(settings.params["Image Display Setting"]["magStatus"])

            self.pfMax.setValue(settings.params["Image Display Setting"]["pfMax"])
            self.pfMin.setValue(settings.params["Image Display Setting"]["pfMin"])
            self.magValue.setValue(settings.params["Image Display Setting"]["magValue"])




    def changeMagValue(self):
        settings.params["Image Display Setting"]["magValue"] = self.magValue.value()
        print("mag value is ", settings.params["Image Display Setting"]["magValue"])

    def changePfMin(self):
        settings.params["Image Display Setting"]["pfMin"] = self.pfMin.value()
        print("photon filter min value is ", settings.params["Image Display Setting"]["pfMin"])

    def changePfMax(self):
        settings.params["Image Display Setting"]["pfMax"] = self.pfMax.value()
        print("photon filter max value is ", settings.params["Image Display Setting"]["pfMax"])


    def rdbstate(self, b):
        if b.text() == "disk":
            settings.params["Image Display Setting"]["imgSource"] = "disk"
            print("image source is ", settings.params["Image Display Setting"]["imgSource"])
        if b.text() == "camera":
            settings.params["Image Display Setting"]["imgSource"] = "camera"
            print("image source is ", settings.params["Image Display Setting"]["imgSource"])
        if b.text()== "single mode":
            settings.params["Image Display Setting"]["mode"] = "single mode"
            print("mode is ", settings.params["Image Display Setting"]["mode"])
        if b.text()== "video mode":
            settings.params["Image Display Setting"]["mode"] = "video mode"
            print("mode is ", settings.params["Image Display Setting"]["mode"])
        if b.text()== "absorption mode":
            settings.params["Image Display Setting"]["mode"] = "absorption mode"
            print("mode is ", settings.params["Image Display Setting"]["mode"])



    def ckbstate(self, b):
        if b.text() == "subtract background image":
            if b.isChecked() == True:
                settings.params["Image Display Setting"]["bkgStatus"] = True
                print("background status", settings.params["Image Display Setting"]["bkgStatus"])
            else:
                settings.params["Image Display Setting"]["bkgStatus"] = False
                print("background status", settings.params["Image Display Setting"]["bkgStatus"])

        if b.text() == "photon filter":
            if b.isChecked() == True:
                settings.params["Image Display Setting"]["pfStatus"] = True
                print("photon filter Status status", settings.params["Image Display Setting"]["pfStatus"])
            else:
                settings.params["Image Display Setting"]["pfStatus"] = False
                print("photon filter Status status", settings.params["Image Display Setting"]["pfStatus"])

        if b.text() == "magnification":
            if b.isChecked() == True:
                settings.params["Image Display Setting"]["magStatus"] = True
                print("magnification status", settings.params["Image Display Setting"]["magStatus"])
            else:
                settings.params["Image Display Setting"]["magStatus"] = False
                print("magnification status", settings.params["Image Display Setting"]["magStatus"])






def add_widget_into_main(parent):
    """
    add a widget into the main window of LabGuiMain
    create a QDock widget and store a reference to the widget
    and output widget is responsible for connect origin signal
    to the itself through LabGuiMain's widgets but input collector
    is responsible for signal emit
    """

    mywidget = ImgDisplaySetting(parent=parent)

    # create a QDockWidget
    displaySettingDockWidget = QDockWidget("Display Setting", parent)
    displaySettingDockWidget.setObjectName("displaySettingDockWidget")
    displaySettingDockWidget.setAllowedAreas(
        Qt.LeftDockWidgetArea |Qt.RightDockWidgetArea
        | Qt.BottomDockWidgetArea)

    # fill the dictionary with the widgets added into LabGuiMain
    parent.widgets['displaySettingDockWidget'] = mywidget

    # add console widget to dock
    displaySettingDockWidget.setWidget(mywidget)
    parent.addDockWidget(Qt.RightDockWidgetArea, displaySettingDockWidget)

    # enable the toggle view action
    parent.windowMenu.addAction(displaySettingDockWidget.toggleViewAction())
    # parent.widgets['PlotWidget'].crossHair.connect(mywidget.updateCrossSection)
    # parent.widgets['PlotWidget'].roi.connect(mywidget.calculateAtom)


# test image display widget in main windows
class MainWindow(TestMainWindow):

    def __init__(self):
        super().__init__()
        add_widget_into_main(self)


        self.initUI()




def test_img_display_widget():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_img_display_widget()


