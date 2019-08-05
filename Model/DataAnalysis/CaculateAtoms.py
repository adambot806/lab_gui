import numpy as np
from scipy.optimize import curve_fit

def crosseSectionDraw(MagStatus, MagFactor, CCDPixelSize, CursorPos, tmpfactor, GSFittingStatue,ROILength, img):
    """
    This part program is to calculate the ratio of intensity between
    the img with atoms and img without atoms

    :param MagStatus:
    :param MagFactor:
    :param CCDPixelSize:
    :param CursorPos:
    :param tmpfactor:
    :param GSFittingStatue:
    :param ROILength:
    :param img:
    :return:
    """
    h = []
    v = []
    # judge whether it needs to be magnified
    if MagStatus:
        # define: size at atom plane / size at ccd plane
        Magnification = MagFactor
    else:
        Magnification = 1

    # the relation between position and the number of photons in cursor cross line
    x1_begin = - CursorPos[1]
    x1_end = np.shape(img)[1] - CursorPos[1]
    x1_range = np.arange(x1_begin,x1_end)*CCDPixelSize[0]*Magnification*1e-3
    y1_range = img[CursorPos[0],:]
    y1_range = y1_range*tmpfactor
    h.append([x1_range,y1_range])

    # plot (x1,y1) as the horizontal figure

    x2_begin = - CursorPos[0]
    x2_end = np.shape(img)[0] - CursorPos[0]
    x2_range = np.arange(x2_begin,x2_end)*CCDPixelSize[1]*Magnification*1e-3
    y2_range = img[:,CursorPos[1]]
    y2_range = y2_range*tmpfactor
    v.append([y2_range,x2_range])

    # plot (y2, x2) as the vertical figure

    # Cross Section Gaussian Fitting
    if GSFittingStatue:
        line_width = 2
        x1_data = np.arange(CursorPos[1] - round(ROILength/2),CursorPos[1]+round(ROILength/2))
        y1_data = np.mean(img[CursorPos[0]-line_width:CursorPos[0]+line_width, x1_data],0)
        x1 = np.linspace(1,1000,np.shape(img)[1])
        XF = curve_fit(GaussianFunc, x1_data, y1_data)
        x1 = (x1 - CursorPos[1]) * CCDPixelSize[0] * Magnification * 1e-3
        y1 = GaussianFunc(x1, *XF)
        h.append([x1,y1])

        # plot((x1-CursorPos[1])*CCDPixelSize[0]*Magnification*1e-3), y1) # horizontal figure

        x2_data = np.arange(CursorPos[0] - round(ROILength/2),CursorPos[1]+round(ROILength/2))
        y2_data = np.mean(img[x2_data, CursorPos[1]-line_width:CursorPos[1]+line_width],0)
        x2 = np.linspace(1,1000,np.shape(img)[0])
        YF = curve_fit(GaussianFunc, x2_data, y2_data)
        y2 = GaussianFunc(x2, *YF)
        x2 = (x2-CursorPos[0])*CCDPixelSize[1]*Magnification*1e-3
        v.append([y2,x2])

        # plot(y2, (x2-CursorPos[0])*CCDPixelSize[1]*Magnification*1e-3) # vertical figure

        total = np.sum(np.sum(img[CursorPos[0] - round(ROILength / 2) : CursorPos[0] + round(ROILength / 2),
                              CursorPos[1] - round(ROILength / 2): CursorPos[1] + round(ROILength / 2)]))

        NCountsfitting = np.abs(2 * np.pi * (XF[0] * YF[0]) ** 0.5 * XF[2] * YF[2])
    return h, v



def GaussianFunc(x,a, b, c, d):
    return a*np.exp(-(x-b)**2)/2/c+d

def GSFitting(x, y, xx):
    popt, pcov = curve_fit(GaussianFunc, x, y)
    print(popt)
    return GaussianFunc(xx, *popt)





def calculaetOpticalDensity(tmpWI, tmpWO, tmpBG, AbsPowerRatioStatus, MotionRPStatus, ButtonLastPos, ROIlength):
    if AbsPowerRatioStatus == 1: # choose PFC then the OD value will be multiplied by Power correction factor
        if not MotionRPStatus:  # when don't choose motionRP,ROI length is default setting
            # left up; take the clicked cursor position as middle point (y,x) relative to left up corner(as origin)
            first_pos = [ButtonLastPos[0] - round(ROIlength/2), ButtonLastPos[1] - round(ROIlength/2)]
            # right down
            second_pos = first_pos[0] + ROIlength
        # four corner area outside of ROI
        PowerRationFactor = np.sum(np.sum(tmpWO[0:first_pos[0],second_pos[0]:np.shape(tmpWI)[0]]),
                                          tmpWO[0:first_pos[1],second_pos[1]:np.shape(tmpWI)[1]]) / \
                            np.sum(np.sum(tmpWI[0:first_pos[0], second_pos[0]:np.shape(tmpWI)[0]]),
                                          tmpWI[0:first_pos[1], second_pos[1]:np.shape(tmpWI)[1]])
    else:
        PowerRationFactor = 1

    # element-wise division
    img = PowerRationFactor*(tmpWI - tmpBG) / (tmpWO - tmpBG)

    # use more efficient way to restrict image value
    for ii in range(1, np.shape(img)[0]):
        for jj in range(1, np.shape(img)[1]):
            if img[ii, jj] >= 1 or img[ii, jj] <= 0:
                img[ii, jj] = 1

            # check whether image value is inf

    # OD_means
    img = -np.log(img)

    # save image

def calculateAtom(MgFactor, MagStatus, CCDPlSize, MotPower, MOTBeamOD, MOTDetuning, tmpfactor, exposureTime, NCountStatus, NCountsfitting, MotionRPStatus, ButtonLastPos, ROIlength, img):
    if not MotionRPStatus:
        first_pos = [ButtonLastPos[0] - round(ROIlength / 2), ButtonLastPos[1] - round(ROIlength / 2)]
        second_pos = first_pos[0] + ROIlength

    ROIImg = img[first_pos[0]:second_pos[0], first_pos[1]:second_pos[1]]
    TotalPhotons = round(tmpfactor * np.sum(np.sum(ROIImg)))

    ROInumPx = np.shape(ROIImg)[0] * np.shape(ROIImg)[1]
    quantumeff = 0.56
    # fluorescence img atoms
    if NCountStatus == 1:
        kbol = 1.38 * 1e-23                                                 # Boltzmann constant
        c0 = 2.997 * 1e8                                                    # Light speed
        hbar = 1.03 * 1e-34
        LensR = (25.4 / 2 * 25.4 / 4) ** 0.5 / 2 * 1e-3              # Lens Radius
        LensD = 260 * 1e-3                                            # Lens distance from MOT
        TotTrans = 0.9                                                      # Lens transmission
        LensEff = (LensR / LensD / 2) ** 2 * TotTrans
        Wavelength = 555.8 * 1e-9                                   # Pumping wavelength
        DecayRate = 2 * 3.14 * 0.18 * 1e6                                   # Transition decay rate
        PhotonE = 2 * 3.14 * hbar * c0 / Wavelength
        SatI0 = PhotonE * DecayRate / (1.5 * Wavelength ** 2 / 3.14) / 2
        SatPara = 1000 * MotPower / 3 / (3.14 * (MOTBeamOD / 2) ** 2) / SatI0
        SatFactor = 6 * SatPara / 2 / (1 + 6 * SatPara + 4 * (2 * 3.14 * MOTDetuning / DecayRate * 1e6) ** 2)
        ScatterRate = DecayRate * SatFactor
        MOTCounts = 1 / LensEff / (ScatterRate * exposureTime * 1e-3) * TotalPhotons / quantumeff
        MOTCountsfitting = 1 / LensEff / (ScatterRate * exposureTime * 1e-3) * NCountsfitting / quantumeff


        AtomROITot = MOTCounts
        AtomROIPX = MOTCounts / ROInumPx
        ElectronROI = TotalPhotons
        AtomROITotFit = MOTCountsfitting

    # absorption img atoms
    elif NCountStatus == 2:
        lamda = 399 * 1e-9
        sigma = 3 * lamda ** 2 / 2 / np.pi
        pixelArea = CCDPlSize[0] * CCDPlSize[1] * 1e-12

        if MagStatus:
            Magnification = MgFactor
        else:
            Magnification = 1

        ABSCounts = pixelArea / sigma * TotalPhotons * Magnification ** 2
        ABSCountsFitting = pixelArea / sigma * NCountsfitting * Magnification ** 2


        # data need to be displayed
        AtomROITot = ABSCounts
        AtomROIPX = ABSCounts / ROInumPx
        ElectronROI = TotalPhotons
        AtomROITotFit = ABSCountsFitting

    return [AtomROITot, AtomROIPX, ElectronROI, AtomROITotFit]



def helper_func(PhotonRangeStatus, img, PhotonRange, loadStatus, BKGStatus, BackgroundData):
    if PhotonRangeStatus:
        # element-wise multiply
        img = heaviside(img-PhotonRange[0]) * heaviside(PhotonRange[1]-img) * img

    # subtract background if use the subtract bg function
    if loadStatus and BKGStatus:
        img = img - BackgroundData

def heaviside(img):
    pass


if __name__ == "__main__":
    xdata = np.linspace(0,4,100)
    y = GaussianFunc(xdata,*[2.5,1.3,0.5,1])
    ydata = y


    y = GSFitting(xdata,ydata,xdata)
    print(np.sum(np.square(y-ydata)))