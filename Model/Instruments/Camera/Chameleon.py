from .BaseCamera import cameraBase
import PyCapture2




class Chameleon(cameraBase):

    VIDEO_MODE = 0
    SOFTWARE_TRIGGER = 1
    HARDWARE_TRIGGER = 2



    def __init__(self):
        super(cameraBase,self).__init__()
        # bus manager
        self.bus = PyCapture2.BusManager()
        self.camera = PyCapture2.Camera()

        self.running = False
        self.readyCapture = False
        self.mode = self.VIDEO_MODE



    def initializeCamera(self):
        """ Initializes the camera.
        """
        if not self.bus.getNumOfCameras():
            print('No cameras detected')
            exit()

        # get camera guid to control it
        guid = self.bus.getCameraFromIndex(0)

        self.camera.connect(guid)


    def setCameraConfiguration(self, camera_setting):
        """
        setting the base parameters for the camera, include exposure time, gain...
        :param camera_setting: a setting dict
        :return:
        """
        # self.camera.setConfiguration(camera_setting)
        return True


    def setImageConfiguration(self,image_setting):
        """
        setting specific image format

        :param image_setting:
        :return:
        """

        return True


    def setAcquisitionMode(self, mode):
        """
        Set  mode that capture image to camera buffer.
        Parameters
        mode : int

        """
        if self.running == True:
            print("Can't reset camera mode when camera is free running!!")
            return
        self.mode = mode

        if mode == self.VIDEO_MODE:
            trigger_mode_setting = {
                'onOff': False,
                'mode': 0,
                'parameter': 0,
                'source': 0
            }
            self.triggerModeSet(trigger_mode_setting)
        elif mode == self.SOFTWARE_TRIGGER:
            trigger_mode_setting = {
                'onOff': True,
                'mode': 0,
                'parameter': 0,
                'source': 7
            }
            self.triggerModeSet(trigger_mode_setting)
        elif mode == self.HARDWARE_TRIGGER:
            trigger_mode_setting = {
                'onOff': True,
                'mode': 0,
                'parameter': 0,
                'source': 0,
                'polarity': 1
            }
            self.triggerModeSet(trigger_mode_setting)

            self.readyCapture = True

        return self.getAcquisitionMode()


    def setShutter(self, shutterValue):

        shutter = PyCapture2.Property()
        shutter.type = PyCapture2.PROPERTY_TYPE.SHUTTER
        shutter.onOff = True
        shutter.autoManualMode = False
        shutter.absControl = True
        shutter.absValue = shutterValue
        self.camera.setProperty(shutter)


    def setExposure(self, exposureVale):
        exposure = PyCapture2.Property()
        exposure.type = PyCapture2.PROPERTY_TYPE.EXPOSURE
        exposure.onOff = True
        exposure.autoManualMode = False
        exposure.absControl = True
        exposure.absValue = exposureVale
        self.camera.setProperty(exposure)


    def setGain(self, gainValue):
        gain = PyCapture2.Property()
        gain.type = PyCapture2.PROPERTY_TYPE.GAIN
        gain.onOff = True
        gain.autoManualMode = False
        gain.absControl = True
        gain.absValue = gainValue
        self.camera.setProperty(gain)


    def startAcquisition(self):
        """
        Start capture images to camera buffer with different situation depend on acquisition mode.
        """
        if self.readyCapture:
            self.running = True
            self.camera.startCapture()
        else:
            print("Not ready for capture image")


    def retrieveOneImg(self):
        """
        retrieve a image
        """
        try:
            image = self.camera.retrieveBuffer()
            return image
        except PyCapture2.Fc2error as fc2Err:

            print('Error retrieving buffer : %s' % fc2Err)

    def retrieveImages(self):
        """
        Retrieve images from camera buffer.
        :return:
        """

        if self.getAcquisitionMode() == self.VIDEO_MODE:
            self.video_mode_capture()
        elif self.getAcquisitionMode() == self.SOFTWARE_TRIGGER:
            self.software_trigger_capture()
        elif self.getAcquisitionMode() == self.HARDWARE_TRIGGER:
            self.hardware_trigger_capture()


    def stopAcquisition(self):
        self.running = False
        self.camera.stopCapture()

    def stopCamera(self):
        """Stops the acquisition and closes the connection with the camera.
        """
        try:
            #Closing the camera
            self.stopAcquisition()
            self.readyCapture = False
            self.camera.disconnect()

        except:
            #Monitor failed to close
            return False


    def getAcquisitionMode(self):
        """Returns the acquisition mode, either continuous or single shot.
        """
        return self.mode


    # Helper function for setting trigger mode
    def triggerModeSet(self, trigger_mode_setting):
        """

        :param trigger_mode_setting={'onOff':True,'mode':0,'parameter':0,'source':7} ==> Using software trigger
        :return:
        """
        trigger_mode = self.camera.getTriggerMode()
        trigger_mode.onOff = trigger_mode_setting['onOff']
        trigger_mode.mode = trigger_mode_setting['mode']
        trigger_mode.parameter = trigger_mode_setting['parameter']
        trigger_mode.source = trigger_mode_setting['source']
        if trigger_mode_setting.get('Polarity'):
            trigger_mode.polarity = trigger_mode_setting['polarity']

        self.camera.setTriggerMode(trigger_mode)

        self.readyCapture = True


    # Helper function for software trigger
    def poll_for_trigger_ready(self):
        software_trigger = 0x62C
        while True:
            reg_val = self.camera.readRegister(software_trigger)
            if not reg_val:
                break



    # Helper function for specific mode capture images
    # TODO：capture one image and emit to LabGui main thread

    def video_mode_capture(self):
        if self.running:
            img = self.retrieveOneImg()

    def software_trigger_capture(self):

       if self.running:
            self.poll_for_trigger_ready()
            img = self.retrieveOneImg()

            self.camera.fireSoftwareTrigger()

    def hardware_trigger_capture(self):
        if self.running:
            img = self.retrieveOneImg()





if __name__ == "__main__":
    # camParam = {}
    # imgParam = {}
    cam = Chameleon()
    cam.initializeCamera()
    # if need to specially configure the camera, then uncomment next 2 lines, or use the default setting.
    # cam.setCameraConfiguration(camParam)
    # cam.setImageConfiguration(imgParam)
    cam.setAcquisitionMode(0)
    cam.startAcquisition()
    # for simple test, just invoke retrieveOneImage(), retrieveImages() is not finished yet
    img = cam.retrieveOneImg()

    cam.stopAcquisition()
    cam.stopCamera()

