import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import Model.AnalysesData.CaculateAtoms as CA
import numpy as np
from MainWindow import TestMainWindow
import logging
import settings


class AnalyseData(QWidget):

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


    atomNumber = pyqtSignal(int)
    fittingFinished = pyqtSignal()



    def __init__(self, parent):
        super(AnalyseData, self).__init__(parent=parent)
        self.parent = parent

        self.horizontalGroupBox1 = QGroupBox("Analyse Data Setting")
        self.horizontalGroupBox2 = QGroupBox("Experiment Parameters")
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        self.roi = QCheckBox("roi", self)
        self.crossHair = QCheckBox("cross hair", self)
        self.calAtom = QCheckBox('calculate atom', self)
        self.fitting = QCheckBox('fitting crossSection')


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

        self.defaultSetting()


        self.Detu.valueChanged.connect(self.changeDetu)
        self.Dia.valueChanged.connect(self.changeDia)
        self.ToPwr.valueChanged.connect(self.changeToPwr)

        self.roi.stateChanged.connect(lambda: self.ckbstate(self.roi))
        self.crossHair.stateChanged.connect(lambda: self.ckbstate(self.crossHair))
        self.fitting.stateChanged.connect(lambda: self.ckbstate(self.fitting))
        self.calAtom.stateChanged.connect(lambda: self.ckbstate(self.calAtom))



    def CrossSection(self):
        """
        use roi image emit from plot windows to process cross section data and emit it to plot window.
        :param roiImg:
        :param anotherParas:
        :return:
        """
        # h, v = CA.crosseSectionDraw(settings.params["Miscellanea"]["MagStatus"], settings.params["Miscellanea"]["MagFactor"], settings.params["Miscellanea"]["CCDPixelSize"], settings.params["Analyse Data Setting"]["cursorPos"],
        #                      settings.params["Miscellanea"]['tmpfactor'], settings.params["Miscellanea"]['GSFittingStatue'], settings.params["Miscellanea"]['ROILength'], settings.ImgData["FluorescenceImg"])

        h = settings.ImgData["FluorescenceImg"][10, :]
        v = settings.ImgData["FluorescenceImg"][:, 10]
        settings.params["Analyse Data Setting"]["fittingData"]["horizontalAxes"] = h
        settings.params["Analyse Data Setting"]["fittingData"]["verticalAxes"] = v
        self.fittingFinished.emit()


    def calculateAtom(self):
        """
        use roi image emit from plot windows to process atom number and emit it to result window.
        calculate atom number for absorption mode
        :return:
        """
        # dlist = [AtomROITot, AtomROIPX, ElectronROI, AtomROITotFit]
        # dlist = CA.calculateAtom(settings.params["Miscellanea"]["MagFactor"], settings.params["Miscellanea"]["MagStatus"], settings.params["Miscellanea"]["CCDPixelSize"], settings.params["Miscellanea"]['MotPower'],
        #                          settings.params["Miscellanea"]['MOTBeamOD'], settings.params["Miscellanea"]['MOTDetuning'], settings.params["Miscellanea"]['tmpfactor'], settings.params["Miscellanea"]['exposureTime'],
        #                          settings.params["Miscellanea"]['NCountStatus'], settings.params["Miscellanea"]['NCountsfitting'], settings.params["Miscellanea"]['MotionRPStatus'],
        #                          settings.params["Miscellanea"]['ButtonLastPos'], settings.params["Miscellanea"]['ROILength'], settings.ImgData["FluorescenceImg"])
        dlist = 10
        self.atomNumber.emit(dlist)

    def calculateOD(self):
        """
        calculate optic density
        :return:
        """
        pass

    def fitting(self):
        pass


    def defaultSetting(self):
        first = True
        if first:
            self.roi.setChecked(False)
            self.fitting.setChecked(False)
            self.calAtom.setChecked(False)
            self.crossHair.setChecked(False)

            self.Detu.setValue(settings.params["Analyse Data Setting"]["Detu"])
            self.Dia.setValue(settings.params["Analyse Data Setting"]["Dia"])
            self.ToPwr.setValue(settings.params["Analyse Data Setting"]["ToPwr"])
            first = False

    def ckbstate(self, b):
        if b.text() == "roi":
            if b.isChecked() == True:
                settings.params["Analyse Data Setting"]["roiStatus"] = True
                print("roi status in global variable change ", settings.params["Analyse Data Setting"]["roiStatus"])

            else:
                settings.params["Analyse Data Setting"]["roiStatus"] = False
                print("roi status in global variable change", settings.params["Analyse Data Setting"]["roiStatus"])

        if b.text() == "cross hair":
            if b.isChecked() == True:
                settings.params["Analyse Data Setting"]["crossHStatus"] = True
                print("cross hair status", settings.params["Analyse Data Setting"]["crossHStatus"])
            else:
                settings.params["Analyse Data Setting"]["crossHStatus"] = False
                print("cross hair status", settings.params["Analyse Data Setting"]["crossHStatus"])

        if b.text() == "calculate atom":
            if b.isChecked() == True:
                settings.params["Analyse Data Setting"]["calculate atom"] = True
                print("calculate atom status", settings.params["Analyse Data Setting"]["calculate atom"])
            else:
                settings.params["Analyse Data Setting"]["calculate atom"] = False
                print("calculate atom status", settings.params["Analyse Data Setting"]["calculate atom"])
        if b.text() == "fitting crossSection":
            if b.isChecked() == True:
                settings.params["Analyse Data Setting"]["fitting crossSection"] = True
                print("fitting crossSection status", settings.params["Analyse Data Setting"]["fitting crossSection"])
            else:
                settings.params["Analyse Data Setting"]["fitting crossSection"] = False
                print("fitting crossSection status", settings.params["Analyse Data Setting"]["fitting crossSection"])


    def changeDetu(self):
        settings.params["Analyse Data Setting"]["Detu"] = self.Detu.value()
        print("new Detu is ", settings.params["Analyse Data Setting"]["Detu"])

    def changeDia(self):
        settings.params["Analyse Data Setting"]["Dia"] = self.Dia.value()
        print("new Dia is ", settings.params["Analyse Data Setting"]["Dia"])

    def changeToPwr(self):
        settings.params["Analyse Data Setting"]["ToPwr"] = self.ToPwr.value()
        print("new toPwr is ", settings.params["Analyse Data Setting"]["ToPwr"])





def add_widget_into_main(parent):
    """
    add a widget into the main window of LabGuiMain
    create a QDock widget and store a reference to the widget
    and output widget is responsible for connect origin signal
    to the itself through LabGuiMain's widgets but input collector
    is responsible for signal emit
    """

    mywidget = AnalyseData(parent=parent)

    # create a QDockWidget
    analyseDataDockWidget = QDockWidget("Analyse Data", parent)
    analyseDataDockWidget.setObjectName("analyseDataDockWidget")
    analyseDataDockWidget.setAllowedAreas(
        Qt.LeftDockWidgetArea |Qt.RightDockWidgetArea
        | Qt.BottomDockWidgetArea)

    # fill the dictionary with the widgets added into LabGuiMain
    parent.widgets['AnalyseDataWidget'] = mywidget

    # default setting


    # add console widget to dock
    analyseDataDockWidget.setWidget(mywidget)
    parent.addDockWidget(Qt.RightDockWidgetArea, analyseDataDockWidget)

    # enable the toggle view action
    parent.windowMenu.addAction(analyseDataDockWidget.toggleViewAction())
    # parent.widgets['PlotWidget'].crossHairChange.connect(mywidget.CrossSection)
    # parent.widgets['PlotWidget'].roiRangeChange.connect(mywidget.calculateAtom)

    # mywidget.Dia.textChanged.connect(parent.changeParams)





# test analyse data widget in main windows
class MainWindow(TestMainWindow):

    def __init__(self):
        super().__init__()
        add_widget_into_main(self)


        self.initUI()




def test_analyse_data_widget():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_analyse_data_widget()



