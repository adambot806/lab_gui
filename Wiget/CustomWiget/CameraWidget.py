import sys
import PyQt5.QtCore as QtCore
import  PyQt5.QtWidgets as QtWidgets
from types import MethodType
from MainWindow import TestMainWindow


class CameraWidget(QtWidgets.QWidget):
    """
        camera setting and control widget for initialization and running,
        including basis camera settings and control.

    """
    def __init__(self, parent=None):
        super(CameraWidget, self).__init__(parent)

        self.start_cam = QtWidgets.QPushButton("start", self)
        self.pause_cam = QtWidgets.QPushButton("pause", self)
        self.capture_cam = QtWidgets.QPushButton("capture", self)
        self.stop_cam = QtWidgets.QPushButton("stop", self)
        self.grid_layout = QtWidgets.QGridLayout()
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.addWidget(self.start_cam)
        self.horizontal_layout.addWidget(self.pause_cam)
        self.horizontal_layout.addWidget(self.capture_cam)
        self.horizontal_layout.addWidget(self.stop_cam)

        self.grid_layout.addLayout(self.horizontal_layout, 0, 0)

        # choose camera to use

        #TODO camrea setting:  ==> mode: video mode; software trigger mode; hardware trigger mode;
        #                       ==> exposure time
        #                       ==> gain





        self.setLayout(self.grid_layout)




def add_widget_into_main(parent):
    """add a widget into the main window of LabGuiMain

    create a QDock widget and store a reference to the widget
    """

    mywidget = CameraWidget(parent=parent)

    # create a QDockWidget
    camDockWidget = QtWidgets.QDockWidget("Camera control window", parent)
    camDockWidget.setObjectName("CameraWidget")
    camDockWidget.setAllowedAreas(
        QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        )

    # fill the dictionary with the widgets added into LabGuiMain
    parent.widgets['CameraWidget'] = mywidget
    camDockWidget.setWidget(mywidget)
    parent.addDockWidget(QtCore.Qt.RightDockWidgetArea, camDockWidget)
    # Enable the toggle view action
    parent.windowMenu.addAction(camDockWidget.toggleViewAction())



# test camera widget in main windows
class MainWindow(TestMainWindow):

    def __init__(self):
        super().__init__()
        add_widget_into_main(self)
        self.initUI()


def test_console_dock_widget():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_console_dock_widget()