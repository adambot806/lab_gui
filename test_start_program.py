import sys
import PyQt5.QtWidgets as QtWidgets
from Utilities.Helper import Helper
from MainWindow import TestMainWindow
import Wiget.CoreWiget.ConsoleDockWidget as ConsoleW
import Wiget.CoreWiget.PlotWindowWidget as PlotW
import Wiget.CoreWiget.ImgDisplaySetting as ImgDS
import Wiget.CoreWiget.AnalyseDataWidget as AnalyseW
import Wiget.CoreWiget.ResultWidget as ResultW
import PIL.Image as Image
import numpy as np
import settings
from pathlib import Path

class MainWindow(TestMainWindow):

    def __init__(self):
        super().__init__()

        ConsoleW.add_widget_into_main(self)
        ImgDS.add_widget_into_main(self)
        PlotW.add_widget_into_main(self)
        AnalyseW.add_widget_into_main(self)
        ResultW.add_widget_into_main(self)
        # TODO: combine statistics and absorption mode, add image history stack
        self.widgets["PlotWidget"].plot_window(1)  # 0 for video mode, 1 for statistics windows, 2 for absorption mode


        # load fluorescence image
        self.loadFlImg = Helper.create_action(self, "loadFL", self.load_fluorescence_img)
        self.fileMenu.addAction(self.loadFlImg)

        # load absorption images
        self.loadABSImg = Helper.create_action(self, "loadABS", self.load_absorption_img)
        self.fileMenu.addAction(self.loadABSImg)

        self.widgets["AnalyseDataWidget"].fittingFinished.connect(self.widgets["PlotWidget"].update_fitting)
        #  TODO: make sure change the global variable first

        self.widgets["AnalyseDataWidget"].roi.stateChanged.connect(self.widgets["PlotWidget"].add_roi)
        self.widgets["AnalyseDataWidget"].crossHair.stateChanged.connect(self.widgets["PlotWidget"].add_cross_hair)

        self.widgets['AnalyseDataWidget'].atomNumber.connect(self.widgets['ResultWidget'].change_atom_num)

    def load_absorption_img(self):
        fpath, _ = QtWidgets.QFileDialog.getExistingDirectory(self, "Open File", "./")
        self.imgNmaes = ["WI", "WO", "BKG", "IMG"]
        for ig in self.imgNmaes:
            imgPath = Path(fpath).glob('*/{}.*'.format(ig))
            img = Image.open(imgPath)
            self.data = np.ones((200, 150)) * 0
            self.data[0:2, :] = 255
            self.data[198:200, :] = 255
            self.data[:, 0:2] = 255
            self.data[:, 148:150] = 255
            img = self.data
            settings.ImgData["ABSImg"][ig] = img
        self.widgets['PlotWidget'].update_img()

    def load_fluorescence_img(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "c:\\", "Image files (*.jpg *.gif)")
        img = Image.open(path)
        self.data = np.ones((200, 150)) * 0
        self.data[0:2, :] = 255
        self.data[198:200, :] = 255
        self.data[:, 0:2] = 255
        self.data[:, 148:150] = 255
        img = self.data
        settings.ImgData["FluorescenceImg"] = img
        self.widgets["PlotWidget"].update_img()






def test_console_dock_widget():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_console_dock_widget()