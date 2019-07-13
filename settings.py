
def inintParams():
    global params, ImgData
    params = {
        "Image Display Setting": {
            "bkgStatus": False,
            "pfStatus": False,
            "magStatus": False,
            "imgSource": "disk",
            "mode": "single mode",
            "magValue": 2,
            "pfMin": 20,
            "pfMax": 200
        },
        "Analyse Data Setting": {
            "roiStatus": False,
            "crossHStatus": False,
            "calAtomStatus": False,
            "fittingStatus": False,
            "ToPwr": 10,
            "Detu": 100,
            "Dia": 100,
            "roiRange": [],
            "AtomNum": 0,
            "cursorPos": [],
            "fittingData": {
                "horizontalAxes": [],
                "verticalAxes": []
                           }
        },
        "Miscellanea": {
            "MagStatus": False,
            "MagFactor": 1,
            "CCDPixelSize": 25,
            "tmpfactor": 1,
            "GSFittingStatue": False,
            "ROILength": 100,
            "NCountStatus": False,
            "NCountsfitting": False,
            "MotionRPStatus": False,
            "exposureTime": 1,
            "MOTBeamOD": 0,
            "MOTDetuning": 0,
            "MotPower": 0,


        }
    }
    ImgData = {
        "FluorescenceImg": [],
        "bkgImg": [],
        "ABSImg": {
            "WO": [],
            "WI": [],
            "BKG": [],
            "PIC": []
        }
    }

    print("Initialize parameters finished")