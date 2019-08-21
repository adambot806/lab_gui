import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget
from Utilities.IO import IOHelper
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities.Helper import settings
from pathlib import Path
import numpy as np
from PIL import Image
import datetime
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

        self.push_btn = QPushButton("sent to main window", self)
        self.push_btn.clicked.connect(self.btn_state)
        self.save_btn = QPushButton("save", self)
        self.save_btn.clicked.connect(self.save_image)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.push_btn)
        self.horizontalLayout.addWidget(self.save_btn)
        self.horizontalLayout.addWidget(self.img_label)
        self.layout.addLayout(self.horizontalLayout)

    def btn_state(self):
        if self.video.image is None:
            print("have no image in window")
            return
        img_dict = {'img_data': np.array(self.video.image), 'img_name': self.img_label.text()}
        self.img_dict.emit(img_dict)

    def save_image(self):
        if self.video.image is None:
            print("have no image in window")
            return
        fpath = IOHelper.get_config_setting('DATA_PATH')
        fpath = Path(fpath)
        dir_path = fpath.joinpath(str(datetime.datetime.now()).split('.')[0].replace(' ', '-').replace(':', '_'))
        print("save images to {}".format(dir_path))
        if not dir_path.exists():
            dir_path.mkdir()
            img_data = np.array(self.video.image)
            # load image name by path
            img_name = (self.img_label.text()).split('.')[0].replace(' ', '-').replace(':', '_')
            img_data = Image.fromarray(img_data)
            img_data.save(r"{}\{}.png".format(dir_path, img_name))
        print("images have saved.")

    def img_plot(self, img_dict):
        self.video.setImage(img_dict['img_data'])
        self.img_label.setText(img_dict['img_name'])

    def clear_win(self):
        self.video.clear()
        self.img_label.setText('')


