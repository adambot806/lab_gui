import sys
from pyqtgraph.Qt import QtCore
import numpy as np
import pyqtgraph as pg

from PyQt5.QtCore import pyqtSignal
import PyQt5.QtWidgets as QtWidgets
from MainWindow import TestMainWindow
import settings


class SubWin(QtWidgets.QWidget):

    roiStateChange = pyqtSignal()
    crossHairStateChange = pyqtSignal()
    roiRangeChange = pyqtSignal()
    crossHairChange = pyqtSignal()

    def __init__(self, parent, mode, label=None):
        """
        :param mode: different kind subwindows
        :param label: marker 4 images in absorption mode
        :param parent:
        """
        super(SubWin, self).__init__()
        self.label = label
        self.mode = mode
        self.parent = parent
        self.custom_window()

    def custom_window(self):
        self.sub = QtWidgets.QMdiSubWindow()
        if self.label != None:
            self.sub.setWindowTitle(self.label)
        self.plotWindow = pg.GraphicsView()
        l = pg.GraphicsLayout()
        self.plotWindow.setCentralItem(l)
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.viewBox = l.addPlot()
        self.viewBox.setAspectLocked(True)
        self.img = pg.ImageItem()
        self.viewBox.addItem(self.img)
        self.viewBox.setRange(QtCore.QRectF(0, 0, 600, 600))
        if (self.mode == 2 and self.label == 'PIC') or self.mode == 1:
            self.verticalAxes = l.addPlot(angle=-90, colspan=1)
            l.nextRow()
            self.horizontalAxes = l.addPlot()
            self.horizontalAxes.setMaximumHeight(250)
        self.sub.setWidget(self.plotWindow)
        self.parent.mdi.addSubWindow(self.sub)
        self.sub.show()

    def handleActivationChange(self, subwindow):
        if subwindow is self.parent():
            print('activated: ', self)
        else:
            print('deactivated: ', self)

    def add_roi(self):
        # video mode doesn't have roi statistics
        if (self.mode == 2 and self.label == 'PIC') or self.mode == 1:
            # Qrect(left_down_x, left_down_y, width, height) left down as origin
            self.roi = pg.ROI([100, 50], [30, 20], maxBounds=QtCore.QRect(0, 0, 100, 100), removable=True)
            self.roi.addScaleHandle([0.5, 1], [0.5, 0.5])
            self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])
            if settings.params["Analyse Data Setting"]["roiStatus"] == True:
                self.viewBox.addItem(self.roi)
                # make sure ROI is drawn above image
                self.roi.setZValue(10)
                self.roi.sigRegionChanged.connect(self.update_roi_range)
            else:
                # remove viewBox's items, including roi and image item
                self.viewBox.clear()
                # add image item
                self.viewBox.addItem(self.img)
        else:
            print("video mode doesn't have roi statistics, please choose another mode.")

    def add_cross_hair(self):
        # video mode doesn't have cross hair statistics
        if (self.mode == 2 and self.label == 'PIC') or self.mode == 1:
            self.vLine = pg.InfiniteLine(angle=90, pen=(255, 0, 0), movable=False)
            self.hLine = pg.InfiniteLine(angle=0, pen=(255, 0, 0), movable=False)
            if settings.params["Analyse Data Setting"]["crossHStatus"] == True:
            # cross hair
                self.viewBox.addItem(self.vLine, ignoreBounds=True)
                self.viewBox.addItem(self.hLine, ignoreBounds=True)
                self.vb = self.viewBox.vb
                self.proxy = pg.SignalProxy(self.viewBox.scene().sigMouseMoved, rateLimit=20, slot=self.update_cursor_pos)
            else:
                settings.params["Analyse Data Setting"]["crossHStatus"] = False
                self.viewBox.clear()
                self.viewBox.addItem(self.img)
        else:
            print("video mode doesn't have cross hair, please choose another mode.")

    def update_cross_section(self):
        """
        update cross hair line statistics
        :return:
        """
        if (self.mode == 2 and self.label == 'PIC') or self.mode == 1:
            self.verticalAxes.plot(settings.ImgData[self.label][:, int(settings.params["Analyse Data Setting"]["cursorPos"][0])],
                         pen=(255, 0, 0))
            self.horizontalAxes.plot(settings.ImgData[self.label][int(settings.params["Analyse Data Setting"]["cursorPos"][0]), :],
                         pen=(0, 255, 0))

    def update_fitting(self):
        """
        update gaussian fitting curve.
        :param data:
        :return:
        """
        if (self.mode == 2 and self.label == 'PIC') or self.mode == 1:
            self.verticalAxes.plot(settings.params["Analyse Data Setting"]["fittingData"]["verticalAxes"], pen=(0, 255, 0), clear=True)
            self.horizontalAxes.plot(settings.params["Analyse Data Setting"]["fittingData"]["horizontalAxes"], pen=(255, 0, 0), clear=True)

    def update_roi_range(self):
        # [(lower-left corner), (size)]
        if (self.mode == 2 and self.label == 'PIC') or self.mode == 1:
            settings.params["Analyse Data Setting"]["roiRange"] = [self.roi.pos(), self.roi.size()]
            self.roiRangeChange.emit()

    def update_cursor_pos(self, evt):
        if (self.mode == 2 and self.label == 'PIC') or self.mode == 1:
            index_x = 0
            index_y = 0
            pos = evt[0]  # using signal proxy turns original arguments into a tuple
            if self.viewBox.sceneBoundingRect().contains(pos):
                mousePoint = self.vb.mapSceneToView(pos)
                index_x = int(mousePoint.x())
                index_y = int(mousePoint.y())

                # update cross line position in plot window
                if index_x < 0:
                    self.vLine.setPos(0)
                    index_x = 0
                elif index_x > settings.ImgData[self.label].shape[1]:
                    self.vLine.setPos(settings.ImgData[self.label].shape[1])
                    index_x = settings.ImgData[self.label].shape[1] - 1
                else:
                    self.vLine.setPos(mousePoint.x())

                if index_y < 0:
                    self.hLine.setPos(0)
                    index_y = 0
                elif index_y > settings.ImgData[self.label].shape[0]:
                    self.hLine.setPos(settings.ImgData[self.label].shape[0])
                    index_y = settings.ImgData[self.label].shape[0] - 1
                else:
                    self.hLine.setPos(mousePoint.y())


            settings.params["Analyse Data Setting"]["cursorPos"] = [index_x, index_y]

            self.crossHairChange.emit()
            self.crossHairChange.connect(self.update_cross_section)

    def update_img(self):
        if self.mode == 0 and self.mode == 1:
            if settings.ImgData['FluorescenceImg'] == []:
                print("Fluorescence image is None")
            else:
                self.img.setImage(np.array(settings.ImgData['FluorescenceImg']))
                print("update Fluorescence image ing...")
        elif self.mode == 2:
            if settings.ImgData['ABSImg'][self.label] == []:
                print("{} image is None".format(self.label))
            else:
                self.img.setImage(np.array(settings.ImgData['ABSImg'][self.label]))
                print("update {} image ing...".format(self.label))


class PlotWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)
        self.mdi = QtWidgets.QMdiArea()
        self.parent = parent

    def plot_window(self, mode):
        # vanilla mode
        self.mode = mode
        if self.mode == 0:
            self.vanilla_plot()
        # statistics mode
        elif self.mode == 1:
            self.statistics_plot()
        # multiple mode
        elif self.mode == 2:
            self.multiple_window_plot()

    def vanilla_plot(self):
        """
        single imageItem, design for video mode.
        :return:
        """
        self.vanilla_win = SubWin(self, 0)

    def statistics_plot(self):
        """
        single imgItem with cross section and roi statistics
        :return:
        """
        self.statistics_win = SubWin(self, 1)

    def multiple_window_plot(self):
        """
        multiple imageItem for display, specially for absorption mode
        :return:
        """
        self.with_light_win = SubWin(self, 2, "WI")
        self.mdi.addSubWindow(self.with_light_win.sub)
        self.with_light_win.sub.show()
        self.without_light_win = SubWin(self, 2, "WO")
        self.mdi.addSubWindow(self.without_light_win.sub)
        self.without_light_win.sub.show()
        self.background_win = SubWin(self, 2, "BKG")
        self.mdi.addSubWindow(self.background_win.sub)
        self.background_win.sub.show()
        self.pic_win = SubWin(self, 2, "PIC")
        self.mdi.addSubWindow(self.pic_win.sub)
        self.pic_win.sub.show()
        self.mdi.tileSubWindows()

    def add_roi(self):
        if self.mode == 1:
            self.statistics_win.add_roi()
        if self.mode == 2:
            # add roi in pic subwindow, other subwindow don't need to take roi
            self.pic_win.add_roi()
        else:
            print("mode error")

    def add_cross_hair(self):
        if self.mode == 1:
            self.statistics_win.add_cross_hair()
        if self.mode == 2:
            self.pic_win.add_cross_hair()
        else:
            print("mode error")

    def update_cross_section(self):
        """
        update cross hair line statistics
        :return:
        """
        if self.mode == 1:
            self.statistics_win.update_cross_section()
        if self.mode == 2:
            self.pic_win.update_cross_section()
        else:
            print("mode error")

    def update_fitting(self):
        """
        update gaussian fitting curve.
        :param data:
        :return:
        """
        if self.mode == 1:
            self.statistics_win.update_fitting()
        if self.mode == 2:
            self.pic_win.update_fitting()
        else:
            print("mode error")

    def update_roi_range(self):
        if self.mode == 1:
            self.statistics_win.update_roi_range()
        if self.mode == 2:
            self.pic_win.update_roi_range()
        else:
            print("mode error")

    def update_img(self):
        if self.mode == 0 and self.mode == 1:
            self.statistics_win.update_img()
        elif self.mode == 2:
            self.with_light_win.update_img()
            self.wothout_light_win.update_img()
            self.background_win.update_img()
            self.pic_win.update_img()


def add_widget_into_main(parent):
    """
    add a widget into the main window of LabGuiMain
    create a QDock widget and store a reference to the widget
    and output widget is responsible for connect origin signal
    to the itself through LabGuiMain's widgets but input collector
    is responsible for signal emit
    """

    mywidget = PlotWidget(parent=parent)
    # create a MidWidget
    parent.setCentralWidget(mywidget.mdi)

    # fill the dictionary with the widgets added into LabGuiMain
    parent.widgets['PlotWidget'] = mywidget

    #
    # parent.widgets["AnalyseWidget"].fittingFinished.connect(mywidget.update_fitting)
    # #  TODO: make sure change the global variable first
    # parent.widgets["AnalyseWidget"].roi.stateChanged.connect(mywidget.add_ROI)
    # parent.widgets["AnalyseWidget"].crossHair.stateChanged.connect(mywidget.add_cross_hair)
    #
    #


# test console widget in main windows
class MainWindow(TestMainWindow):

    def __init__(self):
        super().__init__()
        add_widget_into_main(self)
        self.widgets["PlotWidget"].plot_window(2)
        self.initUI()




def test_console_dock_widget():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_console_dock_widget()




