from Model.Instruments.Camera.BaseCamera import cameraBase
import numpy as np
from PIL import Image
import datetime
import time


class DummyCamera(cameraBase):
    """
    dummy camera is used for debug
    """

    VIDEO_MODE = 0

    def __init__(self):
        super(cameraBase, self).__init__()

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

    def getShutter(self):
        return self.shutter

    def setExposure(self, exposureVale):
        self.exposure = exposureVale

    def getExposure(self):
        return self.exposure

    def setGain(self, gainValue):
       self.gain = gainValue

    def getGain(self):
        return self.gain

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
        retrieve a image name and image data
        """
        time.sleep(0.5)
        image_data = Image.open(r'C:\Users\LingfengZ\Documents\GitHub\lab_gui\Debug\images\20190713_213618OD\1.png')
        # image_name = datetime.datetime.now()

        return image_data

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

  # Helper function for software trigger
    def poll_for_trigger_ready(self):
        time.sleep(.3)  # for debug

    def fire_software_trigger(self):
        time.sleep(.2) # for debug






if __name__ == "__main__":

    cam = DummyCamera()
    cam.initializeCamera()
    cam.setAcquisitionMode(0)
    cam.startAcquisition()
    img = cam.retrieveOneImg()
    cam.stopAcquisition()
    cam.stopCamera()

