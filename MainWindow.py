from Model.Instruments.Camera.Chameleon import Chameleon
from Utilities.Helper import settings, Helper
from Utilities.IO import IOHelper
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Widget.CoreWidget.PlotMainWindowWidget import PlotMainWindow
from Widget.CoreWidget.ImgQueueWidget import ImgQueueWidget
from Widget.CoreWidget.ImgDisplaySetting import ImgDisplaySetting
from Widget.CoreWidget.AnalyseDataWidget import ImgAnalysisSetting
from Widget.CoreWidget.PromptWidget import PromptWidget
from Widget.CoreWidget.ResultWidget import ResultWidget
from Widget.CustomWidget.CameraSettingWidget import CameraOption

import numpy as np
import sys
from PIL import Image
import time
from pathlib import Path
import datetime


class TestMainWindow(QMainWindow):

    sig_abort_workers = pyqtSignal()

    def __init__(self):
        super(TestMainWindow, self).__init__()

        ### MENUS AND TOOLBARS ###
        self.fileMenu = self.menuBar().addMenu("File")
        self.windowMenu = self.menuBar().addMenu("Window")
        self.optionMenu = self.menuBar().addMenu("Options")

        self.plotToolbar = self.addToolBar("Plot")
        self.expToolbar = self.addToolBar("Experiment")

        # experiment start/stop buttons
        self.start_exp_action = Helper.create_action(self, "Start Experiment", slot=self.start_exp, icon="start")
        self.stop_exp_action = Helper.create_action(self, "Stop Experiment", slot=self.stop_exp, icon="stop")
        self.stop_exp_action.setEnabled(False)

        # plot buttons
        self.clear_img_stack_action = Helper.create_action(self, "clear image stack", slot=self.clear_img_stack, icon="clear_img_stack")
        self.clear_main_win_action = Helper.create_action(self, "clear main window", slot=self.clear_main_win, icon="clear_main_win")

        ### CREATE WIDGET ###
        # global parameters
        settings.inintParams()

        self.plot_main_window = PlotMainWindow()
        self.setCentralWidget(self.plot_main_window)

        # image queue dock
        self.img_queue = ImgQueueWidget()
        # create a QDockWidget
        imgQueueDockWidget = QDockWidget("Image Stack", self)
        imgQueueDockWidget.setObjectName("imgStackDockWidget")
        imgQueueDockWidget.setAllowedAreas(
            Qt.LeftDockWidgetArea)
        imgQueueDockWidget.setWidget(self.img_queue)
        self.addDockWidget(Qt.LeftDockWidgetArea, imgQueueDockWidget)
        self.windowMenu.addAction(imgQueueDockWidget.toggleViewAction())


        # image display setting dock
        self.img_display_setting = ImgDisplaySetting()
        # create a QDockWidget
        displaySettingDockWidget = QDockWidget("Display Setting", self)
        displaySettingDockWidget.setObjectName("displaySettingDockWidget")
        displaySettingDockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
        displaySettingDockWidget.setWidget(self.img_display_setting)
        self.addDockWidget(Qt.RightDockWidgetArea, displaySettingDockWidget)
        # enable the toggle view action
        self.windowMenu.addAction(displaySettingDockWidget.toggleViewAction())

        # image analyse setting dock
        self.img_analyse_setting = ImgAnalysisSetting()
        analyseDataDockWidget = QDockWidget("Analyse Data", self)
        analyseDataDockWidget.setObjectName("analyseDataDockWidget")
        analyseDataDockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
        analyseDataDockWidget.setWidget(self.img_analyse_setting)
        self.addDockWidget(Qt.RightDockWidgetArea, analyseDataDockWidget)
        self.windowMenu.addAction(analyseDataDockWidget.toggleViewAction())

        # camera setting dock
        self.camera_setting = CameraOption()
        cameraSettingDockWidget = QDockWidget("Camera Setting", self)
        cameraSettingDockWidget.setObjectName("cameraSettingDockWidget")
        cameraSettingDockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
        cameraSettingDockWidget.setWidget(self.camera_setting)
        self.addDockWidget(Qt.RightDockWidgetArea, cameraSettingDockWidget)
        self.windowMenu.addAction(cameraSettingDockWidget.toggleViewAction())

        # output dock
        self.prompt_dock = PromptWidget()
        promptDockWidget = QDockWidget("Output Console", self)
        promptDockWidget.setObjectName("consoleDockWidget")
        promptDockWidget.setAllowedAreas(Qt.BottomDockWidgetArea)
        promptDockWidget.setWidget(self.prompt_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, promptDockWidget)
        # redirect print statements to show a copy on "console"
        sys.stdout = Helper.print_redirect()
        sys.stdout.print_signal.connect(self.update_console)
        self.windowMenu.addAction(promptDockWidget.toggleViewAction())

        # result dock
        self.result_dock = ResultWidget()
        resultDockWidget = QDockWidget("Result Console", self)
        resultDockWidget.setObjectName("resultDockWidget")
        resultDockWidget.setAllowedAreas(Qt.BottomDockWidgetArea)
        resultDockWidget.setWidget(self.result_dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, resultDockWidget)
        self.windowMenu.addAction(resultDockWidget.toggleViewAction())

        ### TOOLBAR MENU ###
        self.expToolbar.setObjectName("ExperimentToolbar")

        self.expToolbar.addAction(self.start_exp_action)
        self.expToolbar.addAction(self.stop_exp_action)

        self.plotToolbar.setObjectName("PlotToolbar")

        self.plotToolbar.addAction(self.clear_img_stack_action)
        self.plotToolbar.addAction(self.clear_main_win_action)

        self.fileLoadImgAction = Helper.create_action(self,
                                                           "Load Previous Images",
                                                           slot=self.file_load_imgs,
                                                           shortcut=None,
                                                           icon=None,
                                                           tip="Load previous images to image stack from file")

        self.fileSaveImgAction = Helper.create_action(self,
                                                       "Save Image Data",
                                                       slot=self.file_save_imgs,
                                                       shortcut=None,
                                                       icon=None,
                                                       tip="Save image stack's images")

        self.fileMenu.addAction(self.fileLoadImgAction)
        self.fileMenu.addAction(self.fileSaveImgAction)

        # queue for update main window when camera is in video mode
        self.acquiring = False
        # thread for acquiring image from camera to queue
        self.thread = None
        self.worker = None
        self.connect_slot2signal()
        self.setWindowIcon(QIcon('images/icon/UALab.png'))
        self.show()

    def change_camera_params(self):
        self.camera_setting.apply_button.setEnabled(False)
        if self.acquiring:
            self.sig_abort_workers.emit()
            self.thread.quit()  # this will quit **as soon as thread event loop unblocks**
            self.thread.wait()  # <- so you need to wait for it to *actually* quit
            print("camera thread quit")
            self.worker = Worker()
            self.thread = QThread()
            self.worker.moveToThread(self.thread)
            self.worker.sig_video_mode_img.connect(self.update_main_plot_win)
            self.worker.sig_hardware_mode_img.connect(self.update_image_queue)
            # control worker:
            self.sig_abort_workers.connect(self.worker.abort)
            self.thread.started.connect(self.worker.work)
            self.thread.start()  # this will emit 'started' and start thread's event loop
            print("camera setting is applied ")
        self.camera_setting.apply_button.setEnabled(True)

    def change_camera_mode(self, mode):
        if self.acquiring:
            if mode.isChecked():
                self.sig_abort_workers.emit()
                self.thread.quit()  # this will quit **as soon as thread event loop unblocks**
                self.thread.wait()  # <- so you need to wait for it to *actually* quit
                print("camera thread quit")
                if mode.text() == 'video mode':
                    settings.widget_params["Image Display Setting"]["mode"] = 0
                    self.img_display_setting.hardware_mode.setEnabled(True)
                    self.img_display_setting.video_mode.setEnabled(False)
                    self.img_display_setting.hardware_mode.setChecked(False)
                    self.camera_setting.apply_button.setEnabled(True)
                    self.camera_setting.camera_further_setting.gain_value.setEnabled(True)
                    self.camera_setting.camera_further_setting.exposure_time.setEnabled(True)
                    self.camera_setting.camera_further_setting.shutter_time.setEnabled(True)

                elif mode.text() == 'hardware mode':
                    settings.widget_params["Image Display Setting"]["mode"] = 2
                    self.img_display_setting.hardware_mode.setEnabled(False)
                    self.img_display_setting.video_mode.setChecked(False)
                    self.img_display_setting.video_mode.setEnabled(True)
                    self.camera_setting.apply_button.setEnabled(False)
                    self.camera_setting.apply_button.setEnabled(False)
                    self.camera_setting.camera_further_setting.gain_value.setEnabled(False)
                    self.camera_setting.camera_further_setting.exposure_time.setEnabled(False)
                    self.camera_setting.camera_further_setting.shutter_time.setEnabled(False)

                self.worker = Worker()
                self.thread = QThread()
                self.worker.moveToThread(self.thread)
                self.worker.sig_video_mode_img.connect(self.update_main_plot_win)
                self.worker.sig_hardware_mode_img.connect(self.update_image_queue)
                # control worker:
                self.sig_abort_workers.connect(self.worker.abort)
                self.thread.started.connect(self.worker.work)
                self.thread.start()  # this will emit 'started' and start thread's event loop
            print("camera is in new mode")

    def start_exp(self):
        """
        start basis experiment include capturing images, more operations can be
        added here or use a script file to control instrument accurately.
        :return:
        """
        if settings.instrument_params["Camera"]["index"] is not None:

            self.start_exp_action.setEnabled(False)

            self.fileLoadImgAction.setEnabled(False)
            self.fileSaveImgAction.setEnabled(False)

            self.img_display_setting.video_mode.setEnabled(True)
            self.img_display_setting.hardware_mode.setEnabled(True)

            self.clear_img_stack_action.setEnabled(False)
            self.clear_main_win_action.setEnabled(False)

            self.worker = Worker()
            self.thread = QThread()
            self.worker.moveToThread(self.thread)
            self.worker.sig_video_mode_img.connect(self.update_main_plot_win)
            self.worker.sig_hardware_mode_img.connect(self.update_image_queue)
            # control worker:
            self.sig_abort_workers.connect(self.worker.abort)
            self.thread.started.connect(self.worker.work)
            self.thread.start()  # this will emit 'started' and start thread's event loop

            # finish camera index setting, then can't change camera index during experiment,
            # if want to change camera index, then stop experiment
            self.camera_setting.cb.setEnabled(False)
            self.camera_setting.further_setting.setEnabled(True)
            self.camera_setting.apply_button.setEnabled(True)
            settings.widget_params["Image Display Setting"]["imgSource"] = "camera"
            self.img_display_setting.video_mode.setChecked(True)
            self.img_display_setting.video_mode.setEnabled(False)
            settings.widget_params["Image Display Setting"]["mode"] = 0
            self.acquiring = True
            self.stop_exp_action.setEnabled(True)
        else:
            print("select a camera for further experiment")

    def stop_exp(self):
        """
        stop basis experiment include capturing images when image source is camera.
        :return:
        """
        self.stop_exp_action.setEnabled(False)
        if self.acquiring:
            self.sig_abort_workers.emit()
            self.thread.quit()  # this will quit **as soon as thread event loop unblocks**
            self.thread.wait()  # <- so you need to wait for it to *actually* quit

        self.acquiring = False
        self.start_exp_action.setEnabled(True)
        self.fileLoadImgAction.setEnabled(True)
        self.fileSaveImgAction.setEnabled(True)
        self.clear_img_stack_action.setEnabled(True)
        self.clear_main_win_action.setEnabled(True)
        self.camera_setting.cb.setEnabled(True)
        self.camera_setting.further_setting.setEnabled(False)

        self.img_display_setting.video_mode.setChecked(False)
        self.img_display_setting.hardware_mode.setChecked(False)
        self.img_display_setting.video_mode.setEnabled(False)
        self.img_display_setting.hardware_mode.setEnabled(False)

    def connect_slot2signal(self):

        # image display widget
        # all parameters' signal are connected to global parameters.

        self.img_display_setting.video_mode.stateChanged.connect(
            lambda: self.change_camera_mode(self.img_display_setting.video_mode)
        )
        self.img_display_setting.hardware_mode.stateChanged.connect(
            lambda: self.change_camera_mode(self.img_display_setting.hardware_mode)
        )

        # image stack widget
        for i in range(settings.widget_params["Image Display Setting"]["img_stack_num"]):
            plot_win = self.img_queue.plot_wins.get()
            plot_win.img_dict.connect(self.plot_main_window.img_plot)
            self.img_queue.plot_wins.put(plot_win)
        # plot main window widget
        self.plot_main_window.atom_number.connect(self.result_dock.change_atom_num)

        # analyse data widget
        self.img_analyse_setting.roi.stateChanged.connect(
            lambda: self.plot_main_window.add_roi(self.img_analyse_setting.roi, self.img_analyse_setting.cross_axes)
        )
        self.img_analyse_setting.cross_axes.stateChanged.connect(
            lambda: self.plot_main_window.add_cross_axes(self.img_analyse_setting.cross_axes)
        )

        # camera setting widget
        self.camera_setting.apply_button.clicked.connect(self.camera_setting.camera_further_setting.change_exposure)
        self.camera_setting.apply_button.clicked.connect(self.camera_setting.camera_further_setting.change_gain)
        self.camera_setting.apply_button.clicked.connect(self.camera_setting.camera_further_setting.change_shutter)
        self.camera_setting.apply_button.clicked.connect(self.change_camera_params)

    def clear_img_stack(self):
        """
        clear image stack
        :return:
        """
        if self.acquiring and settings.widget_params["Image Display Setting"]["mode"] == 0:
            print("video mode can't clear image stack")
            return
        # make sure that queue isn't changing when using qsize()
        for i in range(settings.widget_params["Image Display Setting"]["img_stack_num"]):
            plot_win = self.img_queue.plot_wins.get()
            plot_win.clear_win()
            self.img_queue.plot_wins.put(plot_win)

    def clear_main_win(self):
        """
              clear main windows
              :return:
              """
        if self.acquiring and settings.widget_params["Image Display Setting"]["mode"] == 0:
            print("video mode can't clear main window")
            return
        self.plot_main_window.clear_win()

    ### LOAD CUSTOM SETTING FOR INSTRUMENT CONNECT AND PARAMETERS ###

    def file_save_imgs(self):
        """
        save image stack's images to disk
        :return:
        """
        fpath = IOHelper.get_config_setting('DATA_PATH')
        fpath = Path(fpath)
        dir_path = fpath.joinpath(str(datetime.datetime.now()).split('.')[0].replace(' ', '-').replace(':', '_'))
        print("save images to {}".format(dir_path))
        if not dir_path.exists():
            dir_path.mkdir()
        for i in range(settings.widget_params["Image Display Setting"]["img_stack_num"]):
            plot_win = self.img_queue.plot_wins.get()
            if plot_win.video.image is not None:
                img_data = np.array(plot_win.video.image)
                # load image name by path
                img_name = (plot_win.img_label.text()).split('.')[0].replace(' ', '-').replace(':', '_')
                img_data = Image.fromarray(img_data)
                img_data.save(r"{}\{}.png".format(dir_path, img_name))
            self.img_queue.plot_wins.put(plot_win)
        print("images have saved.")

    def file_load_imgs(self):
        """
        Load previous image to stack.
        :return:
        """
        self.load_img2stack()

    def load_img2stack(self):
        """
        load images to image queue, with image name and data
        """
        settings.widget_params["Image Display Setting"]["imgSource"] = "disk"
        fpath = IOHelper.get_config_setting('DATA_PATH')
        img_fpath = QFileDialog.getExistingDirectory(self, "Open File", fpath)
        img_file = Path(img_fpath)
        img_paths = list(img_file.glob('*.png'))
        for win_index in range(settings.widget_params["Image Display Setting"]["img_stack_num"]):
            if win_index == len(img_paths):
                break
            plot_win = self.img_queue.plot_wins.get()
            plot_win.img_plot(self.load_img_dict(img_paths[win_index]))
            self.img_queue.plot_wins.put(plot_win)

    ### MISCELLANY ###

    def load_img_dict(self, img_path):
        img_data = np.array(Image.open(img_path))
        # load image name by path
        img_name = img_path.stem
        img = {
            'img_name': img_name,
            'img_data': img_data
        }
        return img

    def update_console(self, stri):
        MAX_LINES = 50
        stri = str(stri)
        new_text = self.prompt_dock.console_text() + '\n' + stri
        line_list = new_text.splitlines()
        N_lines = min(MAX_LINES, len(line_list))
        # limit output lines
        new_text = '\n'.join(line_list[-N_lines:])
        self.prompt_dock.console_text(new_text)
        self.prompt_dock.automatic_scroll()

    def update_main_plot_win(self, img_dict):
        """
        Updates the main plot window at regular intervals. It designs for video mode
        """
        # take the newest image in the queue
        if img_dict is None:
            return
        self.plot_main_window.img_plot(img_dict)

    def update_image_queue(self, img_dict):
        plot_win = self.img_queue.plot_wins.get()
        plot_win.img_plot(img_dict)
        self.img_queue.plot_wins.put(plot_win)
        print("update image queue")


class Worker(QObject):
    """
    Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
    """

    sig_video_mode_img = pyqtSignal(dict)
    sig_hardware_mode_img = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.camera = Chameleon()
        self.camera.initializeCamera(settings.instrument_params["Camera"]["index"])
        self.camera.setAcquisitionMode(settings.widget_params["Image Display Setting"]["mode"])

        self.camera.setExposure(settings.instrument_params["Camera"]["exposure time"])
        self.camera.setShutter(settings.instrument_params["Camera"]["shutter time"])
        self.camera.setGain(settings.instrument_params["Camera"]["gain value"])
        # set a low grab timeout to avoid crash when retrieve image.
        self.camera.set_grab_timeout(grab_timeout=10)
        self.__abort = False

    @pyqtSlot()
    def work(self):
        print("camera start work")
        self.camera.startAcquisition()
        while True:
            # check if we need to abort the loop; need to process events to receive signals;
            app.processEvents()  # this could cause change to self.__abort
            if self.__abort:
                break

            img_data = self.camera.retrieveOneImg()  # retrieve image from camera buffer
            if img_data is None:
                continue
            else:
                timestamp = datetime.datetime.now()
                if settings.widget_params["Image Display Setting"]["mode"] == 2:
                    self.sig_hardware_mode_img.emit({'img_name': str(timestamp), 'img_data': Helper.split_list(img_data)})
                else:
                    self.sig_video_mode_img.emit({'img_name': str(timestamp), 'img_data': Helper.split_list(img_data)})
                    # set a appropriate refresh value
                    time.sleep(0.1)
        self.camera.stopCamera()

    def abort(self):
        self.__abort = True



def start_main_win():
    app = QApplication(sys.argv)
    # Force the style to be the same on all OSs:
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    app.setApplicationName("UALab")
    window = TestMainWindow()
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Force the style to be the same on all OSs:
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    app.setApplicationName("UALab")
    window = TestMainWindow()
    window.show()
    sys.exit(app.exec_())
