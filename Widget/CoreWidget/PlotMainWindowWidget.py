from queue import Queue
import pyqtgraph as pg
from pyqtgraph.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities.Helper import settings


class PlotMainWindow(QWidget):

    # roiChange = pyqtSignal(object)
    # crossSectionChange = pyqtSignal(object)

    def __init__(self):
        super(PlotMainWindow, self).__init__()
        self.layout = QVBoxLayout(self)

        win = pg.GraphicsView()
        l = pg.GraphicsLayout(border=(100, 100, 100))
        win.setCentralItem(l)
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.viewBox = l.addPlot()
        self.img = pg.ImageItem()
        self.viewBox.addItem(self.img)
        self.layout.addWidget(win)
        self.img_label = QLabel()
        self.layout.addWidget(self.img_label)
        self.setLayout(self.layout)
        self.data = None
        self.data_shape = None
        self.roi_range_dict = Queue(1)
        self.cross_section_dict = Queue(1)

    def add_roi(self, roi_cbk_state, cs_cbk_state):
        if roi_cbk_state.isChecked():
            # video mode doesn't have roi statistics
            if settings.widget_params["Image Display Setting"]["imgSource"] == "camera":
                if settings.widget_params["Image Display Setting"]["mode"] == 0:
                    print("video mode doesn't have roi statistics, please choose another mode.")
                    # 0 doesn't check, 2 means check
                    roi_cbk_state.setCheckState(0)
                    cs_cbk_state.setCheckState(0)
                    settings.widget_params["Analyse Data Setting"]["crossHStatus"] = False
                    settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
                    return
            if self.data is None:
                print("Main plot window doesn't handle image, please load image first")
                roi_cbk_state.setCheckState(0)
                settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
                cs_cbk_state.setCheckState(0)
                settings.widget_params["Analyse Data Setting"]["crossHStatus"] = False
                return
            self.roi = pg.ROI([100, 50], [30, 20], maxBounds=QtCore.QRect(0, 0, self.data_shape[1], self.data_shape[0]), removable=True)
            self.roi.setPen(color='r', width=3)  # set roi width and color
            self.roi.addScaleHandle([0.5, 1], [0.5, 0.5])
            self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])
            self.viewBox.addItem(self.roi)
            # make sure ROI is drawn above image
            self.roi.setZValue(10)
            self.roi.sigRegionChanged.connect(self.update_roi_range)
            settings.widget_params["Analyse Data Setting"]["roiStatus"] = True
            cs_cbk_state.setCheckState(0)
            settings.widget_params["Analyse Data Setting"]["crossHStatus"] = False
        else:
            roi_cbk_state.setCheckState(0)
            settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
            # remove viewBox's items, including roi, cross line and image item
            self.viewBox.clear()

            # add image item
            self.viewBox.addItem(self.img)

    def add_cross_line(self, cs_cbk_state, roi_cbk_state):
        # video mode doesn't have cross hair statistics
        if cs_cbk_state.isChecked():
            if settings.widget_params["Image Display Setting"]["imgSource"] == "camera":
                if settings.widget_params["Image Display Setting"]["mode"] == 0:
                    print("video mode doesn't have cross hair statistics, please choose another mode.")
                    settings.widget_params["Analyse Data Setting"]["crossHStatus"] = False
                    cs_cbk_state.seCheckState(0)
                    roi_cbk_state.setCheckState(0)
                    settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
                    print("camera mode is 0")
                    return
            if self.data is None:
                print("Main plot window doesn't handle image, please load image first")
                settings.widget_params["Analyse Data Setting"]["crossHStatus"] = False
                cs_cbk_state.setCheckState(0)
                roi_cbk_state.setCheckState(0)
                settings.widget_params["Analyse Data Setting"]["roiStatus"] = False

                print("data is none")
                return

            self.vLine = pg.InfiniteLine(angle=90, movable=False)
            self.hLine = pg.InfiniteLine(angle=0, movable=False)
            self.vLine.setPen(color='r', width=3)
            self.hLine.setPen(color='r', width=3)
            # add horizontal axes and vertical axes
            self.h_axes = self.viewBox.plot()
            self.h_axes.setPen(color='r', width=3)
            # TODO: vertical axes hasn't finished
            self.v_axes = self.viewBox.plot()
            self.v_axes.setPen(color='g', width=3)
            # cross hair
            self.viewBox.addItem(self.vLine, ignoreBounds=True)
            self.viewBox.addItem(self.hLine, ignoreBounds=True)
            self.vb = self.viewBox.vb
            self.proxy = pg.SignalProxy(self.viewBox.scene().sigMouseMoved, rateLimit=40, slot=self.update_cross_section)
            settings.widget_params["Analyse Data Setting"]["crossHStatus"] = True
            roi_cbk_state.setCheckState(0)
            settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
        else:
            print("cross hair isn't checked")
            settings.widget_params["Analyse Data Setting"]["crossHStatus"] = False
            cs_cbk_state.setCheckState(0)
            self.viewBox.clear()

            self.viewBox.addItem(self.img)

    def plot_cross_section(self, v_data, h_data):
        """
        update gaussian fitting curve.
        :param data:
        :return:
        """
        if settings.widget_params["Image Display Setting"]["imgSource"] == "camera":
            if settings.widget_params["Image Display Setting"]["mode"] == 0:
                print("video mode doesn't have  statistics, please choose another mode.")
                return
        self.h_axes.setData(h_data)
        self.v_axes.setData(v_data)

    def update_roi_range(self):
        # [(lower-left corner), (size)]
        if settings.widget_params["Image Display Setting"]["imgSource"] == "camera":
            if settings.widget_params["Image Display Setting"]["mode"] == 0:
                print("video mode doesn't have roi statistics, please choose another mode.")
            return
        # pos = left down corner(x,y) note: x means normal x axis
        # size = (roi_height, roi_width)
        roi = {'pos': [int(self.roi.pos()[0]), int(self.roi.pos()[1])], 'size': [int(self.roi.size()[0]), int(self.roi.size()[1])]}
        # change the global parameters
        settings.widget_params["Analyse Data Setting"]["roiRange"] = roi

        while not self.roi_range_dict.empty():
            _ = self.roi_range_dict.get()
        self.roi_range_dict.put(roi)

        # self.roiChange.emit(roi)

    def update_cross_section(self, evt):
        if settings.widget_params["Image Display Setting"]["imgSource"] == "camera":
            if settings.widget_params["Image Display Setting"]["mode"]  == 0:
                print("video mode doesn't have roi statistics, please choose another mode.")
                return
        v_data = None
        h_data = None
        pos = evt[0]  # using signal proxy turns original arguments into a tuple
        if self.viewBox.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            index_x = int(mousePoint.x())
            index_y = int(mousePoint.y())

            # update cross line position in plot window
            if index_x <= 0:
                self.vLine.setPos(0)
                self.v_axes.setData(self.data[:, 0, 1])
                v_data = self.data[:, 0, 1]
            elif index_x >= self.data_shape[1]:
                self.vLine.setPos(self.data_shape[1])
                self.v_axes.setData(self.data[:, self.data_shape[1]-1, 1])
                v_data = self.data[:, self.data_shape[1]-1, 1]
            else:
                self.vLine.setPos(mousePoint.x())
                self.v_axes.setData(self.data[:, index_x, 1])
                v_data = self.data[:, index_x, 1]

            if index_y <= 0:
                self.hLine.setPos(0)
                self.h_axes.setData(self.data[0, :, 1])
                h_data = self.data[0, :, 1]
            elif index_y >= self.data_shape[0]:
                self.hLine.setPos(self.data_shape[0])
                self.h_axes.setData(self.data[self.data_shape[0]-1, :, 1])
                h_data = self.data[self.data_shape[0]-1, :, 1]
            else:
                self.hLine.setPos(mousePoint.y())
                self.h_axes.setData(self.data[index_y, :, 1])
                h_data = self.data[index_y, :, 1]
        if h_data is None and v_data is None:
            return
        cross_section_dict = {"h_data": h_data, "v_data": v_data}
        settings.widget_params["Analyse Data Setting"]["crossSectionData"] = cross_section_dict
        # self.crossSectionChange.emit(cross_section_dict)
        while not self.cross_section_dict.empty():
            _ = self.cross_section_dict.get()
        self.cross_section_dict.put(cross_section_dict)

    def img_plot(self, img_dict):
        """
        design for software mode and hardware mode, choose image from image stack to display in main window
        :param img_dict:
        :return:
        """
        self.img.setImage(img_dict['img_data'])
        self.img_label.setText(img_dict['img_name'])
        self.data = img_dict['img_data']
        settings.imgData['MainImg'] = img_dict['img_data']
        self.data_shape = self.data.shape
        print("update image")

    def clear_win(self):
        self.viewBox.clear()
        # add image item
        self.viewBox.addItem(self.img)
        if self.img is None:
            return
        self.img.clear()
        self.img_label.setText('')
        self.data = None
        self.data_shape = None






