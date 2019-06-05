import sys
import PyQt5.QtCore as QtCore
import  PyQt5.QtWidgets as QtWidgets
from Utilities.Helper import Helper
from types import MethodType
from MainWindow import TestMainWindow




class ConsoleWidget(QtWidgets.QWidget):

    """
    This class is a TextEdit with a few extra features,
    can be integrated into LabGui as a message box,which
    can be use for warning and display calculate result
    """

    def __init__(self, parent=None):
        super(ConsoleWidget, self).__init__(parent)
        self.consoleTextEdit = QtWidgets.QTextEdit()
        self.consoleTextEdit.setReadOnly(True)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.addWidget(self.consoleTextEdit)
        self.setLayout(self.verticalLayout)

    def console_text(self, new_text=None):

        """get/set method for the text in the console"""

        if new_text == None:

            return str((self.consoleTextEdit.toPlainText())).rstrip()

        else:

            self.consoleTextEdit.setPlainText(new_text)

    def automatic_scroll(self):
        """
        performs an automatic scroll up
        the latest text shall always be in view
        """
        sb = self.consoleTextEdit.verticalScrollBar()
        sb.setValue(sb.maximum())


def add_widget_into_main(parent):
    """
    add a widget into the main window of LabGuiMain
    create a QDock widget and store a reference to the widget
    """

    mywidget = ConsoleWidget(parent=parent)

    # create a QDockWidget
    consoleDockWidget = QtWidgets.QDockWidget("Output Console", parent)
    consoleDockWidget.setObjectName("consoleDockWidget")
    consoleDockWidget.setAllowedAreas(
        QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea
        | QtCore.Qt.BottomDockWidgetArea)

    # fill the dictionary with the widgets added into LabGuiMain
    parent.widgets['ConsoleWidget'] = mywidget

    # add console widget to dock
    consoleDockWidget.setWidget(mywidget)
    parent.addDockWidget(QtCore.Qt.BottomDockWidgetArea, consoleDockWidget)

    # enable the toggle view action
    parent.windowMenu.addAction(consoleDockWidget.toggleViewAction())

    # redirect print statements to show a copy on "console"
    sys.stdout = Helper.print_redirect()
    # binding a update console function to class object
    parent.update_console = MethodType(update_console, parent)
    sys.stdout.print_signal.connect(parent.update_console)

def update_console(parent, stri):
    MAX_LINES = 50
    stri = str(stri)
    new_text = parent.widgets['ConsoleWidget'].console_text() + '\n' + stri
    line_list = new_text.splitlines()
    N_lines = min(MAX_LINES, len(line_list))
    # limit output lines
    new_text = '\n'.join(line_list[-N_lines:])
    parent.widgets['ConsoleWidget'].console_text(new_text)

    parent.widgets['ConsoleWidget'].automatic_scroll()



# test console widget in main windows
class MainWindow(TestMainWindow):

    def __init__(self):
        super().__init__()
        add_widget_into_main(self)
        print("hello LabGui")
        print(self.widgets['ConsoleWidget'].console_text())

        self.initUI()




def test_console_dock_widget():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_console_dock_widget()