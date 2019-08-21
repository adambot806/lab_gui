from PyQt5.QtWidgets import *
from Utilities.Helper import settings


class ImgAnalysisSetting(QWidget):

    def __init__(self, parent=None):
        super(ImgAnalysisSetting, self).__init__(parent=parent)
        self.parent = parent

        self.horizontalGroupBox1 = QGroupBox("Analyse Data Setting")
        self.horizontalGroupBox2 = QGroupBox("Experiment Parameters")
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()

        self.roi = QCheckBox("roi", self)
        self.cross_axes = QCheckBox("cross axes", self)

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
        layout1.addWidget(self.cross_axes)

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


    def default_setting(self):

        self.roi.setChecked(False)
        self.cross_axes.setChecked(False)

        self.Detu.setValue(settings.widget_params["Analyse Data Setting"]["Detu"])
        self.Dia.setValue(settings.widget_params["Analyse Data Setting"]["Dia"])
        self.ToPwr.setValue(settings.widget_params["Analyse Data Setting"]["ToPwr"])

    def change_Detu(self):
        settings.widget_params["Analyse Data Setting"]["Detu"] = self.Detu.value()
        print("new Detu is ", settings.widget_params["Analyse Data Setting"]["Detu"])

    def change_Dia(self):
        settings.widget_params["Analyse Data Setting"]["Dia"] = self.Dia.value()
        print("new Dia is ", settings.widget_params["Analyse Data Setting"]["Dia"])

    def change_ToPwr(self):
        settings.widget_params["Analyse Data Setting"]["ToPwr"] = self.ToPwr.value()
        print("new toPwr is ", settings.widget_params["Analyse Data Setting"]["ToPwr"])



