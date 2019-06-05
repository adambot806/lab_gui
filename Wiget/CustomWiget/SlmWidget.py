import sys
import PyQt5.QtCore as QtCore
import  PyQt5.QtWidgets as QtWidgets
from types import MethodType
from MainWindow import TestMainWindow


class SlmWidget(QtWidgets.QWidget):
    """
        Slm setting and control widget for initialization and running,
        including basis slm settings and control.

    """
    def __init__(self, parent=None):
        super(SlmWidget,self).__init__(parent)

        self.start_slm = QtWidgets.QPushButton("start",self)
        self.display_slm = QtWidgets.QPushButton("display",self)
        self.stop_slm = QtWidgets.QPushButton("stop",self)
        self.grid_layout = QtWidgets.QGridLayout()
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.addWidget(self.start_slm)
        self.horizontal_layout.addWidget(self.display_slm)
        self.horizontal_layout.addWidget(self.stop_slm)

        self.grid_layout.addLayout(self.horizontal_layout,0,0)

        # choose img which to slm


        # choose different way to convert img to hologram.


        self.setLayout(self.grid_layout)




class slmWorker(QtCore.QThread):

    def __init__(self, slm):
        super(slmWorker,self).__init__(slm)
        self.keep_run = True
        self.slm = slm



    def run(self):
        if self.slm.hadSetImg == True:
            first = True
            while(self.keep_run):
                if first:
                    self.slm.init()
                    first = False
                self.slm.load_img()
            self.slm.stop_load()


def add_widget_into_main(parent):
    """add a widget into the main window of LabGuiMain

    create a QDock widget and store a reference to the widget
    """

    mywidget = SlmWidget(parent=parent)

    # create a QDockWidget
    slmDockWidget = QtWidgets.QDockWidget("SLM control window", parent)
    slmDockWidget.setObjectName("SlmWidget")
    slmDockWidget.setAllowedAreas(
        QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        )

    # fill the dictionary with the widgets added into LabGuiMain
    parent.widgets['SlmWidget'] = mywidget

    slmDockWidget.setWidget(mywidget)
    parent.addDockWidget(QtCore.Qt.RightDockWidgetArea, slmDockWidget)

    # Enable the toggle view action
    parent.windowMenu.addAction(slmDockWidget.toggleViewAction())




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


