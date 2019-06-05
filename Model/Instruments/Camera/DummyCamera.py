from Model.Instruments.Camera.BaseCamera import cameraBase
import numpy as np


class DummyCamera(cameraBase):
    """
    dummy camera is used for debug
    """

    VIDEO_MODE = 0

    def __init__(self):
        super(cameraBase,self).__init__()

        self.running = False
        self.readyCapture = False
        self.mode = self.VIDEO_MODE
        self.shutter = -1
        self.exposure = -1
        self.gain = -1



    def initializeCamera(self):
        """ Initializes the camera.

        :return:
        """
        print("Initialize camera")


    def setAcquisitionMode(self, mode):
        """
        Set  mode that capture image to camera buffer.
        Parameters
        mode : int

        """
        self.mode = mode
        self.readyCapture = True
        return self.getAcquisitionMode()



    def setShutter(self, shutterValue):
        self.shutter = shutterValue



    def setExposure(self, exposureVale):
        self.exposure = exposureVale



    def setGain(self, gainValue):
       self.gain = gainValue


    def startAcquisition(self):
        """
        Start capture images to camera buffer.
        """
        if self.readyCapture:
            self.running = True
        else:
            print("Not ready for capture image")


    def retrieveOneImg(self):
        """
        retrieve a image
        """

        image = np.random.rand(100,100)
        return image


    def retrieveImages(self):
        """
        Retrieve images from camera buffer.
        :return:
        """

        self.video_mode_capture()




    def stopAcquisition(self):
        self.running = False

    def stopCamera(self):
        """Stops the acquisition and closes the connection with the camera.
        """
        try:
            self.stopAcquisition()
            self.readyCapture = False

        except:
            return False


    def video_mode_capture(self):
        if self.running:
            img = self.retrieveOneImg()






if __name__ == "__main__":

    cam = DummyCamera()
    cam.initializeCamera()
    cam.setAcquisitionMode(0)
    cam.startAcquisition()
    img = cam.retrieveOneImg()
    print(img)
    cam.stopAcquisition()
    cam.stopCamera()

