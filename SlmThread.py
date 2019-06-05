
from PyQt5.QtCore import QThread, pyqtSignal


class workThread(QThread):
    """
    Thread for control slm to avoid freezing the GUI.
    """

    capture_image = pyqtSignal(object)

    def __init__(self, camera):
        super(QThread,self).__init__()


    def __del__(self):
        self.wait()

    def run(self):
        """
        Triggers the Monitor to acquire a new Image.
        the QThread defined .start() method is a special method that sets up the thread and
        calls our implementation of the run() method.
        """
        return


