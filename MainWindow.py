# from Model.Instruments.Camera.Chameleon import Chameleon
from Model.Instruments.Camera.DummyCamera import DummyCamera
from Utilities.Helper import settings, Helper
from Utilities.Helper.Helper import thread_with_trace
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
from Widget.CustomWidget.CameraSettingWidget import CameraSettingWidget
# from Widget.CustomWidget.SLMSettingWidget import SLMSettingWidget

import numpy as np
import os
import sys
import logging
import logging.config
from PIL import Image
from queue import Queue
from pathlib import Path
import datetime
import time

#TODO: calculate thread has a problem, which causes the main thread to crash.
class TestMainWindow(QMainWindow):

    def __init__(self):
        super(TestMainWindow, self).__init__()
        # if self.config_file:
        #     if not os.path.exists(self.config_file):
        #         logging.error("The config file provided {} doesn't exist, {} will be used instead".format(self.config_file, CONFIG_FILE))
        #         self.config_file = CONFIG_FILE
        # else:
        #     if not os.path.exists(CONFIG_FILE):
        #         logging.warning("A {} file has been generated for you.".format(CONFIG_FILE))
        #         logging.warning("Please modify it to change the default script, settings, data locations and enter debug mode.")
        #         IOHelper.create_config_file()
        #     self.config_file = CONFIG_FILE
        #
        # config_file_ok = False
        #
        # while not config_file_ok:
        #     try:
        #         self.DEBUG = IOHelper.get_debug_setting(config_file_path=self.config_file)
        #         config_file_ok = True
        #     except IOError:
        #         logging.error("The config file provided {} doesn't "
        #                       "have the right format, {} will be used instead.".format(self.config_file, CONFIG_FILE))
        #         if not os.path.exists(CONFIG_FILE):
        #             logging.warning("A {} file has been generated for you.".format(
        #                 CONFIG_FILE))
        #             logging.warning("Please modify it to change the default \
        #                 script, settings and data locations, or to enter debug mode.")
        #
        #             IOHelper.create_config_file()
        #         self.config_file = CONFIG_FILE
        # print("Configuration loaded from : {}".format(self.config_file))

        ### MENUS AND TOOLBARS ###
        self.fileMenu = self.menuBar().addMenu("File")
        self.plotMenu = self.menuBar().addMenu("Plot")
        self.windowMenu = self.menuBar().addMenu("Window")
        self.optionMenu = self.menuBar().addMenu("Options")
        self.loggingSubMenu = self.optionMenu.addMenu("Logger output level")

        self.plotToolbar = self.addToolBar("Plot")
        self.expToolbar = self.addToolBar("Experiment")

        # experiment start/stop buttons
        self.start_exp_action = Helper.create_action(self, "Start Experiment", slot=self.start_exp,
                                                     shortcut=QKeySequence("F5"), icon="start")
        self.stop_exp_action = Helper.create_action(self, "Stop Experiment", slot=self.stop_exp,
                                                    shortcut=QKeySequence("F6"), icon="stop")
        self.stop_exp_action.setEnabled(False)

        # plot buttons
        self.roi_analysis_action = Helper.create_action(self, "roi analysis", slot=self.roi_analysis, icon="roi")
        self.cross_line_action = Helper.create_action(self, "cross line", slot=self.cross_line_analysis, icon="cross_line")
        self.cross_line_fitting_action = Helper.create_action(self, "cross line fitting", slot=self.cross_line_fitting, icon="cross_line_fitting")
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
        self.camera_setting = CameraSettingWidget()
        cameraSettingDockWidget = QDockWidget("Camera Setting", self)
        cameraSettingDockWidget.setObjectName("cameraSettingDockWidget")
        cameraSettingDockWidget.setAllowedAreas(Qt.RightDockWidgetArea)
        cameraSettingDockWidget.setWidget(self.camera_setting)
        self.addDockWidget(Qt.RightDockWidgetArea, cameraSettingDockWidget)
        self.windowMenu.addAction(cameraSettingDockWidget.toggleViewAction())

        # slm setting dock

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

        self.plotToolbar.addAction(self.roi_analysis_action)
        self.plotToolbar.addAction(self.cross_line_action)
        self.plotToolbar.addAction(self.cross_line_fitting_action)
        self.plotToolbar.addAction(self.clear_img_stack_action)
        self.plotToolbar.addAction(self.clear_main_win_action)

        ### FILE MENU SETUP ###
        # self.fileLoadSettingsAction = Helper.create_action(self,
        #                                                    "Load Instrument Settings",
        #                                                    slot=self.file_load_settings,
        #                                                    shortcut=QKeySequence.Open,
        #                                                    icon=None,
        #                                                    tip="Load instrument settings from file")

        self.fileLoadImgAction = Helper.create_action(self,
                                                           "Load Previous Images",
                                                           slot=self.file_load_imgs,
                                                           shortcut=None,
                                                           icon=None,
                                                           tip="Load previous images to image stack from file")

       # TODO: add load/save configuration file action

       #  self.fileSaveSettingsAction = Helper.create_action(self,
       #                                                     "Save Instrument Settings",
       #                                                     slot=self.file_save_settings,
       #                                                     shortcut=QKeySequence.SaveAs,
       #                                                     icon=None,
       #                                                     tip="Save the current instrument settings")

        self.fileSaveImgAction = Helper.create_action(self,
                                                       "Save Image Data",
                                                       slot=self.file_save_imgs,
                                                       shortcut=None,
                                                       icon=None,
                                                       tip="Save image stack's images")

        # self.fileMenu.addAction(self.fileLoadSettingsAction)
        self.fileMenu.addAction(self.fileLoadImgAction)
        # self.fileMenu.addAction(self.fileSaveSettingsAction)
        self.fileMenu.addAction(self.fileSaveImgAction)

        ### PLOT MENU ###
        # queue for data communication in multi thread
        self.q = Queue(maxsize=settings.widget_params["Image Display Setting"]["img_queue_size"])
        # plot main window
        self.pmw = Queue(1)
        # atom number result window
        self.arw = Queue(1)

        self.acquiring = False
        # image stack update flag
        self.img_stack_update = False
        # thread 1 for acquiring image from camera to queue
        self.t1 = None
        # thread 2 for update image stack from queue when camera mode is in software mode and hardware mode
        self.t2 = None
        # thread 3 for calculate atom number and fitting data or more
        self.t3 = None
        # refresh timer connect to plot main window when camera is in video mode
        self.refreshTimer = QTimer()
        self.refreshTimer.start(1000)  # In milliseconds
        self.connect_slot2signal()
        self.setWindowIcon(QIcon('images/icon/UALab.png'))
        self.show()

    def update_main_plot_win(self):
        """
        Updates the main plot window at regular intervals. It designs for video mode
        """
        # take the newest image in the queue
        img_dict = None
        while not self.q.empty():
            img_dict = self.q.get()
        if img_dict is None:
            return
        self.plot_main_window.img.setImage(img_dict['img_data'])
        self.plot_main_window.img_label.setText(img_dict['img_name'])
        settings.imgData['MainImg'] = img_dict['img_data']
        self.plot_main_window.data = img_dict['img_data']
        self.plot_main_window.data_shape = self.plot_main_window.img.shape

    def change_camera_params(self, label, value):
        if self.acquiring:
            self.t1.kill()
            self.t1.join()
            # while self.t1.isAlive():
            #     pass
            self.camera.stopAcquisition()
            # change the camera exposure time
            if label == "exposure time":
                self.camera.setExposure(value.value())
            elif label == "shutter time":
                self.camera.setShutter(value.value())
            elif label == "gain":
                self.camera.setGain(value.value())

            self.t1 = thread_with_trace(target=run_camera, args=(self.camera, self.q))
            self.t1.start()

    def change_camera_mode(self, mode):
        if self.acquiring:
            if mode.isChecked():
                self.t1.kill()
                self.t1.join()
                # while self.t1.isAlive():
                #     print("wait for kill thread")
                #     pass
                self.camera.stopAcquisition()
                if mode.text() == 'video mode':
                    self.img_display_setting.software_mode.setChecked(False)
                    self.img_display_setting.hardware_mode.setChecked(False)
                    self.camera.setAcquisitionMode(0)
                    # refresh timer connect to plot main window to update image in video mode
                    self.refreshTimer.timeout.connect(self.update_main_plot_win)
                    if self.img_stack_update:
                        self.t2.kill()
                        self.t2.join()

                elif mode.text() == 'software mode':
                    self.img_display_setting.video_mode.setChecked(False)
                    self.img_display_setting.hardware_mode.setChecked(False)
                    self.camera.setAcquisitionMode(1)
                    # disconnect refresh timer when camera isn't in video mode
                    self.refreshTimer.timeout.disconnect(self.update_main_plot_win)
                    # start image stack update thread
                    if not self.img_stack_update:
                        self.t2 = thread_with_trace(target=run_img_stack, args=(self.img_queue.plot_wins, self.q))
                        self.t2.start()

                elif mode.text() == 'hardware mode':
                    self.img_display_setting.video_mode.setChecked(False)
                    self.img_display_setting.software_mode.setChecked(False)
                    self.camera.setAcquisitionMode(2)
                    self.refreshTimer.timeout.disconnect(self.update_main_plot_win)
                    if not self.img_stack_update:
                        self.t2 = thread_with_trace(target=run_img_stack, args=(self.img_queue.plot_wins, self.q))
                        self.t2.start()
                self.t1 = thread_with_trace(target=run_camera, args=(self.camera, self.q))
                self.t1.start()

    def start_exp(self):
        """
        start basis experiment include capturing images, more operations can be
        added here or use a script file to control instrument accurately.
        :return:
        """
        if settings.widget_params["Image Display Setting"]["imgSource"] == "camera":
            if self.acquiring:
                print("Experiment is running,  don't start it again !!!")
                return
            else:
                # initialize camera
                self.init_camera()
                # initialize camera thread to capture images
                self.t1 = thread_with_trace(target=run_camera, args=(self.camera,  self.q))
                self.t1.start()
                print("camera thread start ")
                self.acquiring = True
                if settings.widget_params["Image Display Setting"]["mode"] != "video mode":
                    self.t2 = thread_with_trace(target=run_img_stack, args=(self.img_queue.plot_wins, self.q))
                    self.t2.start()
                    self.img_stack_update = True
                else:
                    # just connect when mode is video mode
                    self.refreshTimer.timeout.connect(self.update_main_plot_win)
        elif settings.widget_params["Image Display Setting"]["imgSource"] == "disk":
            print("load image from disk")
            self.load_img2stack()
        self.stop_exp_action.setEnabled(True)
        self.start_exp_action.setEnabled(False)

    def stop_exp(self):
        """
        stop basis experiment include capturing images when image source is camera.
        :return:
        """
        if settings.widget_params["Image Display Setting"]["imgSource"] == "camera":
            if self.acquiring:
                self.t1.kill()
                self.t1.join()
            if self.img_stack_update:
                self.t2.kill()
                self.t2.join()
            self.camera.stopAcquisition()
            self.acquiring = False
            self.img_stack_update = False
        else:
            print("stop experiment.")
        self.stop_exp_action.setEnabled(False)
        self.start_exp_action.setEnabled(True)

    def connect_slot2signal(self):

        # image display widget
        # all parameters' signal are connected to global parameters.

        self.img_display_setting.video_mode.toggled.connect(
            lambda: self.change_camera_mode(self.img_display_setting.video_mode)
        )
        self.img_display_setting.software_mode.toggled.connect(
            lambda: self.change_camera_mode(self.img_display_setting.software_mode)
        )
        self.img_display_setting.hardware_mode.toggled.connect(
            lambda: self.change_camera_mode(self.img_display_setting.hardware_mode)
        )

        # image stack widget
        for i in range(self.img_queue.plot_wins.qsize()):
            plot_win = self.img_queue.plot_wins.get()
            plot_win.img_dict.connect(self.plot_main_window.img_plot)
            self.img_queue.plot_wins.put(plot_win)
        # plot main window widget
        # TODO: calculate module will get result in another thread, which like image stack update thread.
        # self.plot_main_window.roiChange.connect(self.roi_and_cs_analysis)
        # self.plot_main_window.crossSectionChange.connect(self.roi_and_cs_analysis)

        # analyse data widget
        self.img_analyse_setting.roi.stateChanged.connect(
            lambda: self.plot_main_window.add_roi(self.img_analyse_setting.roi, self.img_analyse_setting.crossHair)
        )
        self.img_analyse_setting.crossHair.stateChanged.connect(
            lambda: self.plot_main_window.add_cross_line(self.img_analyse_setting.crossHair, self.img_analyse_setting.roi)
        )

        # self.img_analyse_setting.calAtom.stateChanged.connect(lambda: self.roi_and_cs_analysis(0))
        # self.img_analyse_setting.fitting.stateChanged.connect(lambda: self.roi_and_cs_analysis(1))

        # camera setting widget
        self.camera_setting.exposure_time.valueChanged.connect(
            lambda: self.change_camera_params("exposure time", self.camera_setting.exposure_time)
        )
        self.camera_setting.shutter_time.valueChanged.connect(
            lambda: self.change_camera_params("shutter time", self.camera_setting.shutter_time)
        )
        self.camera_setting.gain_value.valueChanged.connect(
            lambda: self.change_camera_params("gain", self.camera_setting.gain_value)
        )

    def roi_analysis(self):
        self.img_analyse_setting.roi.setCheckState(2)
        # self.plot_main_window.add_roi(self.img_analyse_setting.roi)

    def cross_line_analysis(self):
        self.img_analyse_setting.crossHair.setCheckeState(2)
        # self.plot_main_window.add_cross_hair(self.img_analyse_setting.crossHair)

    def cross_line_fitting(self):
        self.img_analyse_setting.fitting.setCheckeState(2)


    def clear_img_stack(self):
        """
        clear image stack
        :return:
        """
        if settings.widget_params["Image Display Setting"]["mode"] == 0:
            print("video mode can't clear image stack")
            return

        if self.t2 is not None:
            if self.t2.isAlive():
                # clear image stack when data flow is finished, not in update image stack
                return
        # make sure that queue isn't changing when using qsize()
        for i in range(self.img_queue.plot_wins.qsize()):
            plot_win = self.img_queue.plot_wins.get()
            plot_win.clear_win()
            self.img_queue.plot_wins.put(plot_win)

    def clear_main_win(self):
        """
              clear main windows
              :return:
              """
        if settings.widget_params["Image Display Setting"]["mode"] == 0:
            print("video mode can't clear main window")
            return
        self.plot_main_window.clear_win()

    ### LOAD CUSTOM SETTING FOR INSTRUMENT CONNECT AND PARAMETERS ###
    def file_save_settings(self):
        """
            save the settings for the instruments and plot window into a file
            the settings are instrument names, parameters for the instrument and
            which axis to select for plotting, colors, markers, line styles and user
            defined parameters for the window.
        """
        widget_setting_fpath = IOHelper.get_config_setting('WIDGET_SETTING')
        instrument_setting_fpath = IOHelper.get_config_setting('INSTRUMENT_SETTING')
        # save widget parameter
        pass

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
        for i in range(self.img_queue.plot_wins.qsize()):
            plot_win = self.img_queue.plot_wins.get()
            if plot_win.video.image is not None:
                img_data = np.array(plot_win.video.image)
                # load image name by path
                img_name = (plot_win.img_label.text()).split('.')[0].replace(' ', '-').replace(':', '_')
                img_data = Image.fromarray(img_data)
                img_data.save(r"{}\{}.png".format(dir_path, img_name))
            self.img_queue.plot_wins.put(plot_win)
        print("images have saved.")

    def file_load_settings(self):
        """
            load the settings for the instruments and plot window
            the settings are instrument names, connection ports, parameters
            for the instrument and which axis to select for plotting, colors,
            markers, line styles and user defined parameters for the window
        """
        widget_setting_fpath = IOHelper.get_config_setting('WIDGET_SETTING')
        instrument_setting_fpath = IOHelper.get_config_setting('INSTRUMENT_SETTING')
        # load latest widget setting, or use the default config file.
        pass

    def file_load_imgs(self):
        """
        Load previous image to stack.
        :return:
        """
        # fpath = IOHelper.get_config_setting('DATA_PATH')
        self.load_img2stack()

    def load_img2stack(self):
        """
        load images to image queue, with image name and data
        """
        fpath = IOHelper.get_config_setting('DATA_PATH')
        img_fpath = QFileDialog.getExistingDirectory(self, "Open File", fpath)
        img_file = Path(img_fpath)
        for img_path in img_file.glob('*.png'):
            # load image data
            img_data = np.array(Image.open(img_path))
            # load image name by path
            img_name = img_path.stem
            img = {
                'img_name': img_name,
                'img_data': img_data
            }
            if self.q.full():
                self.q.get()
            self.q.put(img)
        print(self.q.qsize())
        # load image to image stack
        while not self.q.empty():
            img_dict = self.q.get()
            plot_win = self.img_queue.plot_wins.get()
            plot_win.img_plot(img_dict)
            self.img_queue.plot_wins.put(plot_win)

    ### MISCELLANY ###
    def init_camera(self):
        """
        read config from config file, and initialize camera.
        :return:
        """
        # self.camera = Chameleon()
        self.camera = DummyCamera()
        self.camera.initializeCamera()
        self.camera.setAcquisitionMode(0)
        print("Initializing camera")

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

    # def roi_and_cs_analysis(self, flag):
    #     if self.pmw.empty():
    #         self.pmw.put(self.plot_main_window)
    #     if self.arw.empty():
    #         self.arw.put(self.result_dock)
    #     if flag == 0:
    #         # kill the calculate thread first
    #         if self.t3 is not None:
    #             if self.t3.isAlive():
    #                 self.t3.kill()
    #                 self.t3.join()
    #         # check if roi has already in main window
    #         if self.img_analyse_setting.roi.isChecked():
    #             if self.img_analyse_setting.calAtom.isChecked():
    #                 self.t3 = thread_with_trace(target=run_calculate, args=(self.pmw, self.arw, self.plot_main_window.roi_range_dict, self.plot_main_window.cross_section_dict,  flag))
    #                 self.t3.start()
    #             else:
    #                 self.img_analyse_setting.calAtom.setCheckState(0)
    #
    #         # without roi, can't trigger calAltom checkbox
    #         else:
    #             self.img_analyse_setting.calAtom.setCheckState(0)
    #     elif flag == 1:
    #         if self.t3 is not None:
    #             if self.t3.isAlive():
    #                 self.t3.kill()
    #                 self.t3.join()
    #         if self.img_analyse_setting.crossHair.isChecked():
    #             if self.img_analyse_setting.fitting.isChecked():
    #                 self.t3 = thread_with_trace(target=run_calculate, args=(self.pmw, self.arw, self.plot_main_window.roi_range_dict, self.plot_main_window.cross_section_dict, flag))
    #                 self.t3.start()
    #             else:
    #                 # without cross line in main window, can't fitting cross line data
    #                 self.img_analyse_setting.fitting.setCheckState(0)
    #         else:
    #             self.img_analyse_setting.fitting.setCheckState(0)
    #




def run_camera(camera, q):
    # camera.enable_embedded_timestamp(True)
    camera.startAcquisition()  # start acquisition means start capture img to camera buffer
    while True:
        img_data = None
        # prev_timestamp = None
        time.sleep(0.5)  # for debug

        # video mode and hardware trigger
        if camera.mode == 0 or camera.mode == 2:
            img_data = camera.retrieveOneImg()  # retrieve image from camera buffer
        # software trigger
        elif camera.mode == 1:
            camera.poll_for_trigger_ready()
            # input('Press the Enter key to initiate a software trigger\n')
            img_data = camera.retrieveOneImg()
            camera.fire_software_trigger()

        if img_data is None:
            continue
        else:
            # timestamp = img_data.getTimeStamp()
            # TODO: need to take the image's real timestamp
            timestamp = datetime.datetime.now()
            # if prev_timestamp:
            #     diff = (timestamp.cycleSeconds - prev_timestamp.cycleSeconds) * 8000 + (timestamp.cycleCount - prev_timestamp.cycleCount)
            #     print('Timestamp [ %d %d ] - %d' % (timestamp.cycleSeconds, timestamp.cycleCount, diff))
            # prev_timestamp = timestamp
            # video mode need to keep image up to date, another mode need keep all images
            if camera.mode == 0:
                # design for video mode, always keep queue size lower than 3
                while q.qsize() > 2:
                    _ = q.get()
            q.put({'img_name': str(timestamp), 'img_data': np.array(img_data)})  # for dummy camera
            # q.put({'img_name': str(timestamp), 'img_data': Helper.split_list(img_data)})  # for Chameleon


def run_img_stack(plot_wins,  imgs):
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

#
# def run_calculate(plot_main_win,  atom_num_result, roi_range_dict, cross_section_dict, flag):
#     """
#         process roi or cross section thread
#        :param plot_main_win:
#        :param atom_num_result:
#        :param roi_range_dict:
#        :param cross_section_dict:
#        :param flag:
#        :return:
#        """
#     roi_range = None
#     cs = None
#     pmw = plot_main_win.get()
#     arw = atom_num_result.get()
#     while True:
#         # roi analysis
#         if flag == 0:
#             while not roi_range_dict.empty():
#                 # get the newest roi
#                 roi_range =roi_range_dict.get()
#                 # using roi to calculate
#             if roi_range is not None:
#                 # TODO: build calculate atom module
#                 OD = np.sum(pmw.data[roi_range["pos"][1]-roi_range["size"][0]:roi_range["pos"][1],
#                          roi_range["pos"][0]:roi_range["pos"][0]+roi_range["size"][1]])
#                 arw.change_atom_num(OD)
#
#         # cross section analysis
#         if flag == 1:
#             while not cross_section_dict.empty():
#                 cs = cross_section_dict.get()
#             if cs is not None:
#                 # cross section fitting
#                 # TODO: build fitting function in Model/DataAnalysis
#                 h_data, v_data = cs['h_data'], cs['v_data']
#                 pmw.h_axes.setData(h_data)
#                 pmw.v_axes.setData(v_data)



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
    start_main_win()
