import sys
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from MainWindow import TestMainWindow
import settings




class ResultWidget(QtWidgets.QWidget):

    """
    This class is a TextEdit with a few extra features,
    can be integrated into LabGui as a message box,which
    can be use for warning and display calculate result
    """

    def __init__(self, parent=None):
        super(ResultWidget, self).__init__(parent)
        self.atom_num_label = QtWidgets.QLabel('Atom number: ')
        self.atom_num = QtWidgets.QLabel(str(0))
        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.addWidget(self.atom_num_label)
        self.hLayout.addWidget(self.atom_num)
        self.setLayout(self.hLayout)

    def change_atom_num(self):
        self.atom_num.setText(str(settings.params['Analyse Data Setting']['AtomNum']))



def add_widget_into_main(parent):
    """
    add a widget into the main window of LabGuiMain
    create a QDock widget and store a reference to the widget
    """

    mywidget = ResultWidget(parent=parent)

    # create a QDockWidget
    resultDockWidget = QtWidgets.QDockWidget("Result Console", parent)
    resultDockWidget.setObjectName("resultDockWidget")
    resultDockWidget.setAllowedAreas(
        QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        | QtCore.Qt.BottomDockWidgetArea)

    # fill the dictionary with the widgets added into LabGuiMain
    parent.widgets['ResultWidget'] = mywidget

    # add result widget to dock
    resultDockWidget.setWidget(mywidget)
    parent.addDockWidget(QtCore.Qt.BottomDockWidgetArea, resultDockWidget)

    # enable the toggle view action
    parent.windowMenu.addAction(resultDockWidget.toggleViewAction())








# test result widget in main windows
class MainWindow(TestMainWindow):

    def __init__(self):
        super().__init__()
        add_widget_into_main(self)
        self.initUI()




def test_result_dock_widget():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_result_dock_widget()