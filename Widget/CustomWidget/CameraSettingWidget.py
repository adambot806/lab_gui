from PyQt5.QtWidgets import *
import Utilities.Helper.settings as settings


class CameraSettingWidget(QWidget):
    """
        camera setting and control widget for initialization and running,
        including basis camera settings and control.

    """
    def __init__(self, parent=None):
        super(CameraSettingWidget, self).__init__(parent)
        self.GroupBox = QGroupBox("Camera Setting")
        layout = QVBoxLayout()
        exposure = QHBoxLayout()
        self.exposure_time_label = QLabel("Exposure time: ")
        self.exposure_time = QDoubleSpinBox()
        self.exposure_time.setRange(10, 80)
        self.exposure_time.setSingleStep(1)
        exposure.addWidget(self.exposure_time_label)
        exposure.addWidget(self.exposure_time)

        shutter = QHBoxLayout()
        self.shutter_label = QLabel("Shutter time: ")
        self.shutter_time = QDoubleSpinBox()
        self.shutter_time.setRange(10, 80)
        self.shutter_time.setSingleStep(1)
        shutter.addWidget(self.shutter_label)
        shutter.addWidget(self.shutter_time)

        gain = QHBoxLayout()
        self.gain_label = QLabel("Shutter time: ")
        self.gain_value = QDoubleSpinBox()
        self.gain_value.setRange(1, 10)
        self.gain_value.setSingleStep(1)
        gain.addWidget(self.gain_label)
        gain.addWidget(self.gain_value)

        layout.addLayout(exposure)
        layout.addLayout(shutter)
        layout.addLayout(gain)

        self.GroupBox.setLayout(layout)
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.GroupBox)

        self.setLayout(self.vertical_layout)

        self.default_setting()

        self.exposure_time.valueChanged.connect(self.change_exposure)
        self.shutter_time.valueChanged.connect(self.change_shutter)
        self.gain_value.valueChanged.connect(self.change_gain)

    def default_setting(self):
        first = True
        if first:
            self.shutter_time.setValue(settings.instrument_params["Camera"]["shutter time"])
            self.exposure_time.setValue(settings.instrument_params["Camera"]["exposure time"])
            self.gain_value.setValue(settings.instrument_params["Camera"]["gain value"])
            first = False

    def change_shutter(self):
        settings.instrument_params["Camera"]["shutter time"] = self.shutter_time.value()
        print("shutter time is ", settings.instrument_params["Camera"]["shutter time"])

    def change_exposure(self):
        settings.instrument_params["Camera"]["exposure time"] = self.exposure_time.value()
        print("exposure time is ", settings.instrument_params["Camera"]["exposure time"])

    def change_gain(self):
        settings.instrument_params["Camera"]["gain value"] = self.gain_value.value()
        print("gain value is ", settings.instrument_params["Camera"]["gain value"])

