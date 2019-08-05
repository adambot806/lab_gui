import numpy as np
import time
from .BaseCamera  import cameraBase
import PyCapture2


class Chameleon(cameraBase):
    VIDEO_MODE = 0
    SOFTWARE_TRIGGER = 1
    HARDWARE_TRIGGER = 2

    def __init__(self):
        super(cameraBase, self).__init__()
        # bus manager
        self.bus = PyCapture2.BusManager()
        self.camera = PyCapture2.Camera()

        self.running = False
        self.readyCapture = False
        self.mode = self.VIDEO_MODE

    def initializeCamera(self):
        """ Initializes the camera.

        :return:
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
        :param camera_setting:
        :return:
        """
        # self.camera.setConfiguration(camera_setting)
        return True

    def setImageConfiguration(self, image_setting):
        """

        :param image_setting:
        :return:
        """

        return True

    def enable_embedded_timestamp(self, enable_timestamp):
        embedded_info = self.camera.getEmbeddedImageInfo()
        if embedded_info.available.timestamp:
            self.camera.setEmbeddedImageInfo(timestamp=enable_timestamp)

    def setAcquisitionMode(self, mode):
        """
        Set  mode that capture image to camera buffer.
        Parameters
        mode : int

        """
        if self.running == True:
            self.stopAcquisition()
            self.readyCapture = False

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

    def setShutter(self, shutterValue):
        """
        Shutter times are scaled by the divider of the basic frame rate.
        For example, dividing the frame rate by two(e.g.15FPS to7.5FPS)
        causes the maximum shutter time to double(e.g.66ms to 133ms).
        :param shutterValue:  int(ms)
        :return:
        """
        if self.running:
            self.stopAcquisition()
            self.readyCapture = False
        shutter = PyCapture2.Property()
        shutter.type = PyCapture2.PROPERTY_TYPE.SHUTTER
        shutter.onOff = True
        shutter.autoManualMode = False
        shutter.absControl = True
        shutter.absValue = shutterValue
        self.camera.setProperty(shutter)
        self.readyCapture = True
        # self.startAcquisition()

    def getShutter(self):
        return self.camera.getProperty(PyCapture2.PROPERTY_TYPE.SHUTTER).absValue

    def setExposure(self, exposureVale):
        if self.running:
            self.stopAcquisition()
            self.readyCapture = False
        exposure = PyCapture2.Property()
        exposure.type = PyCapture2.PROPERTY_TYPE.EXPOSURE
        exposure.onOff = True
        exposure.autoManualMode = False
        exposure.absControl = True
        exposure.absValue = exposureVale
        self.camera.setProperty(exposure)
        self.readyCapture = True
        # self.startAcquisition()

    def getExposure(self):
        return self.camera.getProperty(PyCapture2.PROPERTY_TYPE.EXPOSURE)

    def setGain(self, gainValue):
        """

        :param gainValue:
        :return:
        """
        if self.running:
            self.stopAcquisition()
            self.readyCapture = False
        gain = PyCapture2.Property()
        gain.type = PyCapture2.PROPERTY_TYPE.GAIN
        gain.onOff = True
        gain.autoManualMode = False
        gain.absControl = True
        gain.absValue = gainValue
        self.camera.setProperty(gain)
        self.readyCapture = True
        # self.startAcquisition()

    def startAcquisition(self):
        """
        Start capture images to camera buffer with different situation depend on acquisition mode.
        """
        if self.readyCapture:
            self.running = True
            if self.mode == self.SOFTWARE_TRIGGER:
                self.poll_for_trigger_ready()
                self.camera.setConfiguration(grabTimeout=5000)
            self.camera.startCapture()
        else:
            print("Not ready for capture image")

    def retrieveOneImg(self):
        """
        retrieve a image
        """
        try:
            img_data = self.camera.retrieveBuffer()
            return img_data
        except PyCapture2.Fc2error as fc2Err:

            print('Error retrieving buffer : %s' % fc2Err)
            return None

    def stopAcquisition(self):
        """
        stop capture image
        :return:
        """
        self.running = False
        self.camera.stopCapture()

    def stopCamera(self):
        """Stops the acquisition and closes the connection with the camera.
        """
        try:
            # Closing the camera

            self.stopAcquisition()
            self.readyCapture = False
            self.camera.disconnect()

        except:
            # Monitor failed to close
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
        if trigger_mode_setting.get('polarity'):
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

    def fire_software_trigger(self):
        software_trigger = 0x62C
        fire_val = 0x80000000  # write 1 to Bit 0, Set software trigger
        self.camera.writeRegister(software_trigger, fire_val)


if __name__ == "__main__":
    camParam = {}
    imgParam = {}
    cam = Chameleon()
    cam.initializeCamera()

    cam.setCameraConfiguration(camParam)
    cam.setImageConfiguration(imgParam)
    cam.setAcquisitionMode(0)
    cam.startAcquisition()

    cam.stopAcquisition()
    cam.stopCamera()

