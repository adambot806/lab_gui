"""
    UUTrack.View.Camera.workerThread
    ================================

    Thread that acquires continuously data until a variable is changed. This enables to acquire at any frame rate without freezing the GUI or overloading it with data being acquired too fast.

"""


from PyQt5.QtCore import QThread, pyqtSignal


class workThread(QThread):
    """Thread for acquiring from the camera. If the exposure time is long, this is
    needed to avoid freezing the GUI.
    """

    capture_image = pyqtSignal(object,object)

    def __init__(self, camera):
        super(QThread,self).__init__()
        # self._session = _session
        self.camera = camera
        self.origin = None
        self.keep_acquiring = True

    def __del__(self):
        self.wait()

    def run(self):
        """ Triggers the Monitor to acquire a new Image.
        the QThread defined .start() method is a special method that sets up the thread and
        calls our implementation of the run() method.
        """
        first = True
        while self.keep_acquiring:
            if self.origin == 'snap':
                self.keep_acquiring = False
            if first:
                self.camera.setAcquisitionMode(self.camera.MODE_CONTINUOUS)
                self.camera.triggerCamera()  # Triggers the camera only once
                first = False
            img = self.camera.readCamera()

            self.capture_image.emit(img, self.origin)
        self.camera.stopAcq()
        return
