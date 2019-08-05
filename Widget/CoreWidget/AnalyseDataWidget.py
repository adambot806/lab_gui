from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities.Helper import settings
import numpy as np
import time
import datetime

class ImgAnalysisSetting(QWidget):

    """
    input collector is responsible for signal emit
    1. roi status
    2.the number of atom
    Analyse Dock Window
    Deal with the ROI data(ndarray)
    To realize these functions:
        fitting data: fit the handle data (need different fit functions)
        calculate data: calculate the handle data(different mode==<absorb mode> <normal mode> <slm mode> )
        handle data: select and deal with ROI(specific line or area)
        miscellaneous:

    """

    # atomNumber = pyqtSignal(object)
    # fittingFinished = pyqtSignal(object, object)

    def __init__(self, parent=None):
        super(ImgAnalysisSetting, self).__init__(parent=parent)
        self.parent = parent

        self.horizontalGroupBox1 = QGroupBox("Analyse Data Setting")
        self.horizontalGroupBox2 = QGroupBox("Experiment Parameters")
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        self.roi = QCheckBox("roi", self)
        self.crossHair = QCheckBox("cross hair", self)

        self.calAtom = QCheckBox("calculate atom", self)
        self.fitting = QCheckBox("fitting crossSection", self)

        ToPwrLabel = QLabel('toPwr')
        self.ToPwr = QDoubleSpinBox()
        self.ToPwr.setMinimum(0)
        self.ToPwr.setSingleStep(1)
        DetuLabel = QLabel('Detu')
        self.Detu = QDoubleSpinBox()
        self.Detu.setMinimum(0)
        self.Detu.setSingleStep(1)
        DiaLabel = QLabel('Dia')
        self.Dia = QDoubleSpinBox()
        self.Dia.setMinimum(0)
        self.Dia.setSingleStep(1)

        layout1.addWidget(self.roi)
        layout1.addWidget(self.crossHair)
        layout1.addWidget(self.calAtom)
        layout1.addWidget(self.fitting)

        layout2.addWidget(ToPwrLabel)
        layout2.addWidget(self.ToPwr)
        layout2.addWidget(DetuLabel)
        layout2.addWidget(self.Detu)
        layout2.addWidget(DiaLabel)
        layout2.addWidget(self.Dia)

        self.horizontalGroupBox1.setLayout(layout1)
        self.horizontalGroupBox2.setLayout(layout2)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.horizontalGroupBox1)
        self.vertical_layout.addWidget(self.horizontalGroupBox2)

        self.setLayout(self.vertical_layout)

        self.default_setting()

        self.Detu.valueChanged.connect(self.change_Detu)
        self.Dia.valueChanged.connect(self.change_Dia)
        self.ToPwr.valueChanged.connect(self.change_ToPwr)

        # self.roi.stateChanged.connect(lambda: self.ckb_state(self.roi))
        # self.crossHair.stateChanged.connect(lambda: self.ckb_state(self.crossHair))
        self.fitting.stateChanged.connect(lambda: self.ckb_state(self.fitting))
        self.calAtom.stateChanged.connect(lambda: self.ckb_state(self.calAtom))

    # def cross_section_process(self, cross_section_data):
    #     """
    #     process cross section data.
    #     :return:
    #     """
    #     # h_data means fitting y axes data, v_data means fitting x axes data.
    #     h_data = cross_section_data['horizontalAxes']
    #     v_data = cross_section_data['verticalAxes']
    #     if settings.widget_params["Analyse Data Setting"]["fittingStatus"]:
    #         # time.sleep(.3)
    #         h_data = 60 * np.random.rand(200)
    #         v_data = 50 * np.random.rand(200)
    #         self.fittingFinished.emit(h_data, v_data)
    #         # h, v = CA.crosseSectionDraw(settings.params["Miscellanea"]["MagStatus"],
    #         # settings.params["Miscellanea"]["MagFactor"], settings.params["Miscellanea"]["CCDPixelSize"],
    #         # settings.params["Analyse Data Setting"]["cursorPos"],settings.params["Miscellanea"]['tmpfactor'],
    #         # settings.params["Miscellanea"]['GSFittingStatue'], settings.params["Miscellanea"]['ROILength'],
    #         # settings.ImgData["FluorescenceImg"])
    #     else:
    #         # emit the raw data without fitting
    #         self.fittingFinished.emit(h_data, v_data)
    #
    # # def calculate_atom(self, roi_dict):
    # #     """
    # #     calculate roi's atom number by using global parameters.
    # #     :return:
    # #     """
    # #     # dlist = [AtomROITot, AtomROIPX, ElectronROI, AtomROITotFit]
    # #     # dlist = CA.calculateAtom(settings.params["Miscellanea"]["MagFactor"],
    # #     # settings.params["Miscellanea"]["MagStatus"], settings.params["Miscellanea"]["CCDPixelSize"],
    # #     # settings.params["Miscellanea"]['MotPower'],settings.params["Miscellanea"]['MOTBeamOD'],
    # #     # settings.params["Miscellanea"]['MOTDetuning'], settings.params["Miscellanea"]['tmpfactor'],
    # #     # settings.params["Miscellanea"]['exposureTime'],settings.params["Miscellanea"]['NCountStatus'],
    # #     # settings.params["Miscellanea"]['NCountsfitting'], settings.params["Miscellanea"]['MotionRPStatus'],
    # #     # settings.params["Miscellanea"]['ButtonLastPos'], settings.params["Miscellanea"]['ROILength'],
    # #     # settings.ImgData["FluorescenceImg"])
    # #
    # #     roi_left_down = roi_dict['pos']
    # #     roi_size = roi_dict['size']
    # #     roi = settings.imgData['MainImg'][roi_left_down[1]: roi_left_down[1]+roi_size[0] , roi_left_down[0]: roi_left_down[0]+roi_size[1]]
    # #     self.calculate_OD(roi)
    # #
    # #     self.atomNumber.emit(datetime.datetime.now())
    # #
    # # # def calculate_OD(self, roi):
    #     """
    #     calculate optic density
    #     :return:
    #     """
    #     # time.sleep(.3)
    #     return
    #
    # def fitting(self):
    #     pass

    def default_setting(self):
        first = True
        if first:
            self.roi.setChecked(False)
            self.fitting.setChecked(False)
            self.calAtom.setChecked(False)
            self.crossHair.setChecked(False)

            self.Detu.setValue(settings.widget_params["Analyse Data Setting"]["Detu"])
            self.Dia.setValue(settings.widget_params["Analyse Data Setting"]["Dia"])
            self.ToPwr.setValue(settings.widget_params["Analyse Data Setting"]["ToPwr"])
            first = False

    def ckb_state(self, b):
        if b.text() == "roi":
            if b.isChecked():
                settings.widget_params["Analyse Data Setting"]["roiStatus"] = True
                print("roi status in global variable change ", settings.widget_params["Analyse Data Setting"]["roiStatus"])
            else:
                settings.widget_params["Analyse Data Setting"]["roiStatus"] = False

        if b.text() == "cross hair":
            if b.isChecked():
                settings.widget_params["Analyse Data Setting"]["crossHStatus"] = True
                print("cross hair status", settings.widget_params["Analyse Data Setting"]["crossHStatus"])
            else:
                settings.widget_params["Analyse Data Setting"]["crossHStatus"] = False
                print("cross hair status", settings.widget_params["Analyse Data Setting"]["crossHStatus"])

        if b.text() == "calculate atom":
            if b.isChecked():
                settings.widget_params["Analyse Data Setting"]["calculate atom"] = True
                print("calculate atom status", settings.widget_params["Analyse Data Setting"]["calculate atom"])
            else:
                settings.widget_params["Analyse Data Setting"]["calculate atom"] = False
                print("calculate atom status", settings.widget_params["Analyse Data Setting"]["calculate atom"])
        if b.text() == "fitting crossSection":
            if b.isChecked():
                settings.widget_params["Analyse Data Setting"]["fitting crossSection"] = True
                print("fitting crossSection status", settings.widget_params["Analyse Data Setting"]["fitting crossSection"])
            else:
                settings.widget_params["Analyse Data Setting"]["fitting crossSection"] = False
                print("fitting crossSection status", settings.widget_params["Analyse Data Setting"]["fitting crossSection"])


    def change_Detu(self):
        settings.widget_params["Analyse Data Setting"]["Detu"] = self.Detu.value()
        print("new Detu is ", settings.widget_params["Analyse Data Setting"]["Detu"])

    def change_Dia(self):
        settings.widget_params["Analyse Data Setting"]["Dia"] = self.Dia.value()
        print("new Dia is ", settings.widget_params["Analyse Data Setting"]["Dia"])

    def change_ToPwr(self):
        settings.widget_params["Analyse Data Setting"]["ToPwr"] = self.ToPwr.value()
        print("new toPwr is ", settings.widget_params["Analyse Data Setting"]["ToPwr"])



