from PyQt5.QtWidgets import *
from PIL import Image
from Utilities.Helper import settings
import numpy as np

class ImgDisplaySetting(QWidget):
    """
    1. background image status
    2. photon range status
    3. magnification status
    """
    def __init__(self, parent=None):
        super(ImgDisplaySetting, self).__init__(parent)
        self.parent = parent
        self.GroupBox1 = QGroupBox("Image Display Setting")
        layout1 = QVBoxLayout()

        # background image
        bkg = QHBoxLayout()
        self.bkgStatus = QCheckBox("subtract background image", self)
        self.bkgLoad = QPushButton("load background image", self)
        bkg.addWidget(self.bkgStatus)
        bkg.addWidget(self.bkgLoad)

        # photon filter
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

        # magnification
        mf = QHBoxLayout()
        self.magStatus = QCheckBox('magnification')
        self.magValue = QDoubleSpinBox()
        self.magValue.setRange(0.01,10)
        self.magValue.setSingleStep(0.1)
        mf.addWidget(self.magStatus)
        mf.addWidget(self.magValue)

        mode = QHBoxLayout()
        self.video_mode = QCheckBox("video mode", self)
        self.hardware_mode = QCheckBox("hardware mode", self)
        mode.addWidget(self.video_mode)
        mode.addWidget(self.hardware_mode)

        layout1.addLayout(bkg)
        layout1.addLayout(pf)
        layout1.addLayout(mf)
        layout1.addLayout(mode)

        self.GroupBox1.setLayout(layout1)
        # self.GroupBox2.setLayout(layout2)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.GroupBox1)
        # self.vertical_layout.addWidget(self.GroupBox2)

        self.setLayout(self.vertical_layout)

        self.default_setting()

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
        settings.imgData["BkgImg"] = np.array(img)

    def default_setting(self):
        self.video_mode.setChecked(False)
        self.hardware_mode.setChecked(False)
        self.video_mode.setEnabled(False)
        self.hardware_mode.setEnabled(False)

        self.bkgStatus.setChecked(settings.widget_params["Image Display Setting"]["bkgStatus"])
        self.pfStatus.setChecked(settings.widget_params["Image Display Setting"]["pfStatus"])
        self.magStatus.setChecked(settings.widget_params["Image Display Setting"]["magStatus"])

        self.pfMax.setValue(settings.widget_params["Image Display Setting"]["pfMax"])
        self.pfMin.setValue(settings.widget_params["Image Display Setting"]["pfMin"])
        self.magValue.setValue(settings.widget_params["Image Display Setting"]["magValue"])

    def changeMagValue(self):
        settings.widget_params["Image Display Setting"]["magValue"] = self.magValue.value()
        print("mag value is ", settings.widget_params["Image Display Setting"]["magValue"])

    def changePfMin(self):
        settings.widget_params["Image Display Setting"]["pfMin"] = self.pfMin.value()
        print("photon filter min value is ", settings.widget_params["Image Display Setting"]["pfMin"])

    def changePfMax(self):
        settings.widget_params["Image Display Setting"]["pfMax"] = self.pfMax.value()
        print("photon filter max value is ", settings.widget_params["Image Display Setting"]["pfMax"])

    def ckbstate(self, b):
        if b.text() == "subtract background image":
            if b.isChecked() == True:
                settings.widget_params["Image Display Setting"]["bkgStatus"] = True
                print("background status", settings.widget_params["Image Display Setting"]["bkgStatus"])
            else:
                settings.widget_params["Image Display Setting"]["bkgStatus"] = False

        if b.text() == "photon filter":
            if b.isChecked() == True:
                settings.widget_params["Image Display Setting"]["pfStatus"] = True
                print("photon filter Status status", settings.widget_params["Image Display Setting"]["pfStatus"])
            else:
                settings.widget_params["Image Display Setting"]["pfStatus"] = False

        if b.text() == "magnification":
            if b.isChecked() == True:
                settings.widget_params["Image Display Setting"]["magStatus"] = True
                print("magnification status", settings.widget_params["Image Display Setting"]["magStatus"])
            else:
                settings.widget_params["Image Display Setting"]["magStatus"] = False



