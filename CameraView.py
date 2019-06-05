import sys
import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout,QPushButton,QVBoxLayout,QDockWidget,QFileDialog

from Model.Instruments.Camera import PcCamera
from CameraThread import workThread

class cameraViewer(QMainWindow):
    """Main window for the view camera.
    """
    def __init__(self,camera, slm=None,parent=None):
        super(cameraViewer,self).__init__()

        self.camera = camera
        self.parent = parent
        self.slm = slm
        self.setWindowTitle('Camera Viewer')
        self.viewerWidget = viewerWidget()
        self.setCentralWidget(self.viewerWidget)

        self.viewerWidget.startButton.clicked.connect(self.startCamera)
        self.viewerWidget.stopButton.clicked.connect(self.startCamera)
        self.viewerWidget.captureButton.clicked.connect(self.captureImg)

        # camera setting
        self.acquiring = False
        self.tempImage = []

        self.refreshTimer = QTimer()
        self.refreshTimer.start(100) # In milliseconds
        self.refreshTimer.timeout.connect(self.updateGUI)

        self.show()




    def startCamera(self):
        """Starts a continuous acquisition of the camera.
        """
        # self.emit(QtCore.SIGNAL('stopMainAcquisition'))
        if self.acquiring:
            self.stopCamera()
        else:
            self.acquiring = True
            self.workerThread = workThread(self.camera)
            self.workerThread.mode = 'video_mode'
            self.workerThread.capture_image.connect(self.getData)
            # self.connect(self.workerThread,QtCore.SIGNAL('image'),self.getData)
            self.workerThread.start()

    def stopCamera(self):
        """Stops the acquisition.
        """
        if self.acquiring:
            self.workerThread.keep_acquiring = False
            self.acquiring = False

    def captureImg(self):
        if self.acquiring:
            if self.tempImage is not None:
                if len(self.tempImage) >= 1:
                    self.viewerWidget.img.setImage(self.tempImage)


        pass
    def getData(self,data):
        """Gets the data that is being gathered by the working thread.
        """
        self.tempImage = data

    def updateGUI(self):
        """Updates the GUI at regular intervals.
        """
        if self.tempImage is not None:
                self.viewerWidget.img.setImage(self.tempImage)

    def closeViewer(self):
        """What to do when the viewer is triggered to close from outside.
        """
        self.stopCamera()
        self.close()

    def closeEvent(self,evnt):
        """Triggered at closing. If it is running as main window or not.
        """
        if self.parent == None:
            # self.emit(QtCore.SIGNAL('closeAll'))
            self.camera.stopCamera()
            self.workerThread.terminate()
            self.close()
        else:
            self.closeViewer()

class viewerWidget(QWidget):
    """Widget for holding the GUI elements of the viewer.
    """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.layout = QVBoxLayout(self)

        self.viewport = GraphicsLayoutWidget()
        self.video_view = self.viewport.addViewBox(enableMenu=True)
        self.img_view = self.viewport.addViewBox(enableMenu=True)
        self.video = pg.ImageItem()
        self.img = pg.ImageItem()
        self.video_view.addItem(self.video)
        self.img_view.addItem(self.img)

        self.buttons = QHBoxLayout()
        self.startButton = QPushButton('Start')
        self.stopButton = QPushButton('Stop')
        self.captureButton = QPushButton('Capture')
        self.buttons.addWidget(self.startButton)
        self.buttons.addWidget(self.stopButton)
        self.buttons.addWidget(self.captureButton)

        self.setLayout(self.layout)
        self.layout.addWidget(self.viewport)
        self.layout.addLayout(self.buttons)










def test_camera_viwer():
    app = QApplication(sys.argv)
    pcmera = PcCamera.PcCamera()
    pcmera.initializeCamera()
    cam = cameraViewer(pcmera)
    sys.exit(app.exec_())

if __name__ == "__main__":
    test_camera_viwer()

