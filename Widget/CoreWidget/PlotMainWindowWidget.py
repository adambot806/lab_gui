import pyqtgraph as pg
from pyqtgraph.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities.Helper import settings


class PlotMainWindow(QWidget):

    atom_number = pyqtSignal(object)

    def __init__(self):
        super(PlotMainWindow, self).__init__()
        self.layout = QVBoxLayout(self)

        # win = pg.GraphicsView()
        l = pg.GraphicsLayout(border=(100, 100, 100))
        win = pg.GraphicsLayoutWidget()
        win.setCentralItem(l)
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.viewBox = l.addPlot()
        self.img = pg.ImageItem()
        self.viewBox.addItem(self.img)
        self.layout.addWidget(win)
        self.img_label = QLabel()
        self.layout.addWidget(self.img_label)
        self.setLayout(self.layout)
        self.h_axes = None
        self.v_axes = None
        self.data = None
        self.data_shape = None

    def add_roi(self, roi_cbk_state, axes_cbk_state):
        if roi_cbk_state.isChecked():
            # video mode doesn't have roi statistics
            if settings.widget_params["Image Display Setting"]["imgSource"] == "camera":
                if settings.widget_params["Image Display Setting"]["mode"] == 0:
                    print("video mode doesn't have roi statistics, please choose another mode.")
                    # 0 doesn't check, 2 means check
                    roi_cbk_state.setCheckState(0)
                    settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
                    return
            if self.data is None:
                print("Main plot window doesn't handle image, please load image first")
                roi_cbk_state.setCheckState(0)
                settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
                return
            self.roi = pg.ROI([200, 200], [100, 100], maxBounds=QtCore.QRect(0, 0, self.data_shape[1], self.data_shape[0]),removable=True)
            self.roi.setPen(color='r', width=3)  # set roi width and color
            self.roi.addScaleHandle([0.5, 1], [0.5, 0.5])
            self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])

            self.viewBox.addItem(self.roi)
            # make sure ROI is drawn above image
            self.roi.setZValue(10)
            self.vLine = pg.InfiniteLine(angle=90, movable=False)
            self.hLine = pg.InfiniteLine(angle=0, movable=False)
            self.vLine.setPen(color='r', width=3)
            self.hLine.setPen(color='r', width=3)
            self.vLine.setPos(self.roi.pos()[0]+self.roi.size()[0]/2)
            self.hLine.setPos(self.roi.pos()[1]+self.roi.size()[1]/2)
            self.viewBox.addItem(self.vLine, ignoreBounds=True)
            self.viewBox.addItem(self.hLine, ignoreBounds=True)
            self.roi.sigRegionChanged.connect(self.update_ch_fitting_cs)
            self.roi.sigRegionChanged.connect(self.calculate_roi)
            settings.widget_params["Analyse Data Setting"]["roiStatus"] = True
        else:
            roi_cbk_state.setCheckState(0)
            axes_cbk_state.setCheckState(0)
            settings.widget_params["Analyse Data Setting"]["roiStatus"] = False
            settings.widget_params["Analyse Data Setting"]["add_cross_axes"] = False
            # remove viewBox's items
            self.viewBox.clear()
            # add image item
            self.viewBox.addItem(self.img)

    def add_cross_axes(self, cbk_state):
        if cbk_state.isChecked():
            if settings.widget_params["Analyse Data Setting"]["roiStatus"]:
                settings.widget_params["Analyse Data Setting"]["add_cross_axes"] = True
                # add horizontal axes and vertical axes
                self.h_axes = self.viewBox.plot()
                self.h_axes.setPen(color='r', width=3)
                # TODO: vertical axes hasn't finished
                self.v_axes = self.viewBox.plot()
                self.v_axes.setPen(color='g', width=3)
            else:
                print("please add roi first.")
                # 0 doesn't check, 2 means check
                cbk_state.setCheckState(0)
                settings.widget_params["Analyse Data Setting"]["add_cross_axes"] = False
                return
        else:
            cbk_state.setCheckState(0)
            settings.widget_params["Analyse Data Setting"]["add_cross_axes"] = False
            # remove plotItem if cross axes has added
            if self.h_axes is not None and self.v_axes is not None:
                self.viewBox.removeItem(self.h_axes)
                self.viewBox.removeItem(self.v_axes)

    def update_ch_fitting_cs(self):
        self.vLine.setPos(self.roi.pos()[0]+self.roi.size()[0]/2)
        self.hLine.setPos(self.roi.pos()[1]+self.roi.size()[1]/2)
        if settings.widget_params["Analyse Data Setting"]["add_cross_axes"]:
            # fitting process
            if len(self.data_shape) == 3:
                v_data = self.data[:, int(self.roi.pos()[0]+self.roi.size()[0]/2), 1]
                h_data = self.data[int(self.roi.pos()[1]+self.roi.size()[1]/2), :, 1]
            else:
                v_data = self.data[:, int(self.roi.pos()[0] + self.roi.size()[0] / 2)]
                h_data = self.data[int(self.roi.pos()[1] + self.roi.size()[1] / 2), :]
            # plot origin data and fitting data
            self.h_axes.setData(h_data)
            self.v_axes.setData(v_data)

    def calculate_roi(self):
        # [(lower-left corner), (size)]
        # pos = left down corner(x,y) note: x means normal x axis
        # size = (roi_height, roi_width)
        # roi = {'pos': [int(self.roi.pos()[0]), int(self.roi.pos()[1])], 'size': [int(self.roi.size()[0]), int(self.roi.size()[1])]}
        # calculate atom number
        if self.roi.pos()[0] < 0 or self.roi.pos()[1] < 0 or self.roi.size()[1] > self.data_shape[1] or self.roi.size()[0] > self.data_shape[0]:
            return
        if len(self.data_shape) == 3:
            # three channel data
            atom_num = sum(sum(self.data[int(self.roi.pos()[1]):int(self.roi.pos()[1]+self.roi.size()[0]), int(self.roi.pos()[0]):int(self.roi.pos()[0]+self.roi.size()[1]), 1]))
        else:
            # single channel
            atom_num = sum(sum(self.data[int(self.roi.pos()[1]):int(self.roi.pos()[1] + self.roi.size()[0]), int(self.roi.pos()[0]):int(self.roi.pos()[0] + self.roi.size()[1])]))
        self.atom_number.emit(atom_num)

    def img_plot(self, img_dict):
        """
        design for software mode and hardware mode, choose image from image stack to display in main window
        :param img_dict:
        :return:
        """
        self.img.setImage(img_dict['img_data'])
        self.img_label.setText(img_dict['img_name'])
        self.data = img_dict['img_data']
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






