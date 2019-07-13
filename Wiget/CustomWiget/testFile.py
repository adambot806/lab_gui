import Wiget.CustomWiget.CameraWidget  as camera
import Wiget.CustomWiget.SlmWidget as slm

import sys
import  PyQt5.QtWidgets as QtWidgets
from MainWindow import TestMainWindow





class MainWindow(TestMainWindow):

    def __init__(self):
        super().__init__()

        camera.add_widget_into_main(self)
        slm.add_widget_into_main(self)
        self.initUI()




def test_console_dock_widget():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_console_dock_widget()