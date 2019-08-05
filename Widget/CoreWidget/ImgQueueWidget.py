import sys
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities.Helper import settings
from Utilities.Helper.Helper import thread_with_trace
import numpy as np
from PIL import Image
import datetime
import time
from queue import Queue


class ImgQueueWidget(QWidget):

    def __init__(self, parent=None):
        super(ImgQueueWidget, self).__init__(parent)
        # plot image history
        self.verticalLayout = QVBoxLayout()
        self.plot_wins = Queue(settings.widget_params['Image Display Setting']['img_stack_num'])
        for i in range(settings.widget_params['Image Display Setting']['img_stack_num']):
            plot_win = PlotWindow()
            plot_win.video.image = None
            self.plot_wins.put(plot_win)
            self.verticalLayout.addWidget(plot_win)
        self.setLayout(self.verticalLayout)


def run(plot_wins,  imgs):
    """
    use a thread to update image stack. top image always the newest one.
    :param plot_wins:
    :param imgs:
    :return:
    """
    while True:
        while not imgs.empty():
            time.sleep(1.5)  # for debug
            img_dict = imgs.get()
            plot_win = plot_wins.get()
            plot_win.img_plot(img_dict)
            plot_wins.put(plot_win)


class PlotWindow(QWidget):

    img_dict = pyqtSignal(object)

    def __init__(self):
        super(PlotWindow, self).__init__()
        self.layout = QVBoxLayout(self)

        pg.setConfigOptions(imageAxisOrder='row-major')
        self.viewport = GraphicsLayoutWidget()
        self.video_view = self.viewport.addViewBox()
        self.video = pg.ImageItem()
        self.video_view.addItem(self.video)

        self.setLayout(self.layout)

        self.layout.addWidget(self.viewport)
        self.img_label = QLabel()

        self.rdb = QRadioButton()
        self.rdb.toggled.connect(self.btn_state)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.rdb)
        self.horizontalLayout.addWidget(self.img_label)
        self.layout.addLayout(self.horizontalLayout)

    def btn_state(self):
        if self.rdb.isChecked():
            img_dict = {'img_data': np.array(self.video.image), 'img_name': self.img_label.text()}
            self.img_dict.emit(img_dict)

    def img_plot(self, img_dict):
        self.video.setImage(img_dict['img_data'])
        self.img_label.setText(img_dict['img_name'])

    def get_img_dict(self):
        """
        return plot windows image name and data
        :return: image name and image data
        """
        if self.video.image is None:
            return None
        else:
            return {'img_data': np.array(self.video.image), 'img_name': self.img_label.text()}

    def clear_win(self):
        self.video.clear()
        self.img_label.setText('')


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.q = Queue()
        i = 0
        while i < 50:
            img = Image.open(
                r'C:\Users\LingfengZ\Documents\GitHub\lab_gui\debug_data\images\20190713_213618OD_crop.png')
            time.sleep(.2)
            self.q.put({'img_data': np.array(img), 'img_name': str(datetime.datetime.now())})
            i += 1
        settings.inintParams()
        self.widgets = {}
        self.centralPlot = PlotWindow()
        self.setCentralWidget(self.centralPlot)
        self.t1 = thread_with_trace(target=run, args=(self.widgets['ImgStackWidget'].plot_wins, self.q))
        self.t1.start()

        self.show()


def test_img_queue_dock_widget():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    test_img_queue_dock_widget()

