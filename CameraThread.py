
from PyQt5.QtCore import QThread, pyqtSignal


class workThread(QThread):
    """
    Thread for acquiring from the camera. If the exposure time is long, this is
    needed to avoid freezing the GUI.
    """

    capture_image = pyqtSignal(object)

    def __init__(self, camera):
        super(QThread,self).__init__()
        self.camera = camera
        self.mode = 'video_mode'
        self.keep_acquiring = True

    def __del__(self):
        self.wait()

    def run(self):
        """
        Triggers the Monitor to acquire a new Image.
        the QThread defined .start() method is a special method that sets up the thread and
        calls our implementation of the run() method.
        """
        first = True
        if self.mode == 'video_mode':
            self.camera.setAcquisitionMode(self.camera.VIDEO_MODE)
        elif self.mode == 'software_trigger':
            self.camera.setAcquisitionMode(self.camera.SOFTWARE_TRIGGER)
        elif self.mode == 'hardware_trigger':
            self.camera.setAcquisitionMode(self.camera.HARDWARE_TRIGGER)
        else:
            print("origin wrong!!")
        while self.keep_acquiring:
            if first:
                self.camera.startAcquisition()        # start acquisition means start capture img to camera buffer
                first = False
            img = self.camera.retrieveOneImg()        # retrieve image from camera buffer
            self.capture_image.emit(img)
        self.camera.stopAcquisition()
        self.camera.stopCamera()
        return


