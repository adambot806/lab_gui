import sys
from Utilities.Helper import Helper
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea



class TestMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.widgets = {}
        # create the central part of the application
        self.zoneCentrale = QMdiArea()
        self.setCentralWidget(self.zoneCentrale)

        # set up menus and toolbars
        self.fileMenu = self.menuBar().addMenu("File")
        self.plotMenu = self.menuBar().addMenu("Plot")
        self.windowMenu = self.menuBar().addMenu("Window")
        self.optionMenu = self.menuBar().addMenu("Options")

        self.plotToolbar = self.addToolBar("Plot")
        self.instToolbar = self.addToolBar("Instruments")
        self.show()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestMainWindow()
    sys.exit(app.exec_())