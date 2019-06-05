class cameraBase():

    VIDEO_MODE = 0
    SOFTWARE_TRIGGER = 1
    HARDWARE_TRIGGER = 2

    def __init__(self, camera):
        self.camera = camera
        self.running = False


    def initializeCamera(self):
        """
        Initializes the camera.
        """
        return True


    def setCameraConfiguration(self):
        return True


    def setImageConfiguration(self):
        return True


    def setAcquisitionMode(self, mode):
        """
        Set the readout mode of the camera: Single or continuous.
        :param int mode: One of self.MODE_CONTINUOUS, self.MODE_SINGLE_SHOT
        :return:
        """
        self.mode = mode


    def triggerModeSet(self, trigger_mode_setting):

        pass


    def setShutter(self, shutterValue):
        return self.getShutter()


    def setExposure(self, exposureVale):
        return self.getExposure()


    def setGain(self, gainValue):
        return self.getGain()


    def getAcquisitionMode(self):
        """
        Returns the acquisition mode, either continuous or single shot.
        """
        return self.mode


    def getShutter(self):
        return True


    def getGain(self):
        return True


    def getExposure(self):
        """
        Gets the exposure time of the camera.
        """
        return True


    def startAcquisition(self):
        pass


    def retrieveOneImg(self):
        pass


    def retrieveImages(self):
        pass


    def stopAcquisition(self):
        pass


    def stopCamera(self):
        pass


